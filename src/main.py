from flask import Flask, request, jsonify, render_template, session, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

app = Flask(__name__, static_folder='../static', static_url_path='')
app.secret_key = 'your-secret-key-here'

# CORS configuration
CORS(app, origins=['*'], supports_credentials=True)

# Database configuration
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///wave_house.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    client = db.relationship('Client', backref=db.backref('bookings', lazy=True))

class BlockedSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Email configuration
GMAIL_EMAIL = os.environ.get('GMAIL_EMAIL', 'letswork@wavehousela.com')
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD', 'rkyu btcu xqfn rbsx')

def send_email(to_email, subject, html_content):
    """Send HTML email using Gmail SMTP"""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = GMAIL_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def get_booking_confirmation_email(booking, client):
    """Generate booking confirmation email HTML"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #1a1a1a; color: #ffffff; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: #2a2a2a; border-radius: 10px; padding: 30px; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .logo {{ color: #00CED1; font-size: 28px; font-weight: bold; }}
            .booking-details {{ background-color: #3a3a3a; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .detail-row {{ margin: 10px 0; }}
            .label {{ color: #00CED1; font-weight: bold; }}
            .footer {{ text-align: center; margin-top: 30px; color: #888; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🎵 WAVE HOUSE</div>
                <h2>Booking Confirmation</h2>
            </div>
            
            <div class="booking-details">
                <div class="detail-row"><span class="label">Client:</span> {client.name}</div>
                <div class="detail-row"><span class="label">Email:</span> {client.email}</div>
                <div class="detail-row"><span class="label">Phone:</span> {client.phone}</div>
                <div class="detail-row"><span class="label">Service:</span> {booking.service_type}</div>
                <div class="detail-row"><span class="label">Date:</span> {booking.date}</div>
                <div class="detail-row"><span class="label">Time:</span> {booking.start_time} - {booking.end_time}</div>
                <div class="detail-row"><span class="label">Status:</span> {booking.status.title()}</div>
                {f'<div class="detail-row"><span class="label">Notes:</span> {booking.notes}</div>' if booking.notes else ''}
            </div>
            
            <div class="footer">
                <p>Thank you for choosing Wave House Recording Studio!</p>
                <p>Contact us: letswork@wavehousela.com</p>
            </div>
        </div>
    </body>
    </html>
    """

# Routes
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/submit-booking', methods=['POST'])
def submit_booking():
    try:
        data = request.get_json()
        
        # Create or get client
        client = Client.query.filter_by(email=data['email']).first()
        if not client:
            client = Client(
                name=data['name'],
                email=data['email'],
                phone=data['phone']
            )
            db.session.add(client)
            db.session.flush()
        
        # Create booking
        booking = Booking(
            client_id=client.id,
            service_type=data['serviceType'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            start_time=datetime.strptime(data['startTime'], '%H:%M').time(),
            end_time=datetime.strptime(data['endTime'], '%H:%M').time(),
            notes=data.get('notes', '')
        )
        
        db.session.add(booking)
        db.session.commit()
        
        # Send emails
        confirmation_html = get_booking_confirmation_email(booking, client)
        
        # Send to admin
        send_email(
            GMAIL_EMAIL,
            f"New Booking Request - {booking.service_type}",
            confirmation_html
        )
        
        # Send to client
        send_email(
            client.email,
            "Wave House Booking Confirmation",
            confirmation_html
        )
        
        return jsonify({
            'success': True,
            'message': 'Booking submitted successfully!',
            'booking_id': booking.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/availability', methods=['GET'])
def check_availability():
    try:
        date_str = request.args.get('date')
        if not date_str:
            return jsonify({'error': 'Date parameter required'}), 400
        
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Get existing bookings
        bookings = Booking.query.filter_by(date=date).all()
        
        # Get blocked slots
        blocked_slots = BlockedSlot.query.filter_by(date=date).all()
        
        # Create availability response
        unavailable_slots = []
        
        for booking in bookings:
            unavailable_slots.append({
                'start': booking.start_time.strftime('%H:%M'),
                'end': booking.end_time.strftime('%H:%M'),
                'type': 'booking'
            })
        
        for slot in blocked_slots:
            unavailable_slots.append({
                'start': slot.start_time.strftime('%H:%M'),
                'end': slot.end_time.strftime('%H:%M'),
                'type': 'blocked'
            })
        
        return jsonify({
            'date': date_str,
            'unavailable_slots': unavailable_slots
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin Routes
@app.route('/admin')
def admin_login():
    if 'admin_logged_in' in session:
        return admin_dashboard()
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Wave House Admin</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #1a1a1a; color: #fff; margin: 0; padding: 50px; }
            .login-container { max-width: 400px; margin: 0 auto; background-color: #2a2a2a; padding: 40px; border-radius: 10px; }
            .logo { text-align: center; color: #00CED1; font-size: 24px; font-weight: bold; margin-bottom: 30px; }
            input { width: 100%; padding: 12px; margin: 10px 0; background-color: #3a3a3a; border: 1px solid #555; color: #fff; border-radius: 5px; }
            button { width: 100%; padding: 12px; background-color: #00CED1; color: #000; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; }
            button:hover { background-color: #00B8CC; }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="logo">🎵 WAVE HOUSE ADMIN</div>
            <form method="POST" action="/admin/login">
                <input type="password" name="password" placeholder="Admin Password" required>
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    password = request.form.get('password')
    if password == 'admin123':
        session['admin_logged_in'] = True
        return redirect('/admin')
    else:
        return redirect('/admin')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect('/admin')

def admin_dashboard():
    # Get statistics
    total_bookings = Booking.query.count()
    pending_bookings = Booking.query.filter_by(status='pending').count()
    confirmed_bookings = Booking.query.filter_by(status='confirmed').count()
    blocked_slots_count = BlockedSlot.query.count()
    
    # Get recent bookings
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(10).all()
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Wave House Admin Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #1a1a1a; color: #fff; margin: 0; padding: 20px; }}
            .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }}
            .logo {{ color: #00CED1; font-size: 24px; font-weight: bold; }}
            .logout {{ background-color: #ff4444; color: #fff; padding: 8px 16px; text-decoration: none; border-radius: 5px; }}
            .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
            .stat-card {{ background-color: #2a2a2a; padding: 20px; border-radius: 10px; text-align: center; }}
            .stat-number {{ font-size: 32px; font-weight: bold; color: #00CED1; }}
            .stat-label {{ margin-top: 10px; color: #ccc; }}
            .section {{ background-color: #2a2a2a; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
            .section h3 {{ color: #00CED1; margin-top: 0; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #444; }}
            th {{ background-color: #3a3a3a; color: #00CED1; }}
            .status-pending {{ color: #ffa500; }}
            .status-confirmed {{ color: #00ff00; }}
            .status-cancelled {{ color: #ff4444; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">🎵 WAVE HOUSE ADMIN DASHBOARD</div>
            <a href="/admin/logout" class="logout">Logout</a>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{total_bookings}</div>
                <div class="stat-label">Total Bookings</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{pending_bookings}</div>
                <div class="stat-label">Pending</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{confirmed_bookings}</div>
                <div class="stat-label">Confirmed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{blocked_slots_count}</div>
                <div class="stat-label">Blocked Slots</div>
            </div>
        </div>
        
        <div class="section">
            <h3>Recent Bookings</h3>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Client</th>
                        <th>Service</th>
                        <th>Date</th>
                        <th>Time</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join([f'''
                    <tr>
                        <td>{booking.id}</td>
                        <td>{booking.client.name}</td>
                        <td>{booking.service_type}</td>
                        <td>{booking.date}</td>
                        <td>{booking.start_time} - {booking.end_time}</td>
                        <td class="status-{booking.status}">{booking.status.title()}</td>
                    </tr>
                    ''' for booking in recent_bookings])}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    '''

# Initialize database
@app.before_first_request
def create_tables():
    db.create_all()
    print("Database tables created successfully!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

