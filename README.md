# Wave House Recording Studio Booking System

A professional booking system for Wave House Recording Studio in Los Angeles, featuring a React frontend and Flask backend with admin dashboard capabilities.

## 🎵 Features

### Public Website
- **Professional Landing Page** - Modern, responsive design with Wave House branding
- **Service Booking** - Three service types: Studio Access, Engineer Request, Mixing
- **Real-time Availability** - Check available time slots before booking
- **Contact Information** - Easy access to studio contact details

### Booking System
- **Online Booking Form** - Complete booking process with client information
- **Email Notifications** - Automatic confirmations to clients and admin
- **Database Storage** - Secure storage of all booking and client data
- **Time Slot Management** - Prevent double bookings and conflicts

### Admin Dashboard
- **Secure Login** - Password-protected admin access (password: admin123)
- **Booking Management** - View, confirm, cancel bookings
- **Statistics Dashboard** - Real-time booking statistics and metrics
- **Client Management** - Track client information and booking history

## 🛠️ Tech Stack

- **Frontend**: React 18 with Vite
- **Backend**: Flask (Python)
- **Database**: PostgreSQL (production) / SQLite (development)
- **Styling**: Custom CSS with responsive design
- **Email**: Gmail SMTP integration
- **Deployment**: Railway

## 📁 Project Structure

```
wave-house-booking-system/
├── src/
│   └── main.py              # Flask backend with all routes
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Styling
│   │   ├── index.css        # Global styles
│   │   └── main.jsx         # React entry point
│   ├── index.html           # HTML template
│   ├── package.json         # Frontend dependencies
│   └── vite.config.js       # Vite configuration
├── requirements.txt         # Python dependencies
├── package.json            # Root package configuration
├── Procfile                # Railway deployment configuration
└── .env.example            # Environment variables template
```

## 🚀 Deployment to Railway

### 1. Create Railway Project
1. Go to [Railway.app](https://railway.app)
2. Click "New Project"
3. Connect your GitHub repository
4. Select this repository

### 2. Configure Environment Variables
In Railway dashboard, add these environment variables:

```
DATABASE_URL=postgresql://... (Railway provides this automatically)
GMAIL_EMAIL=letswork@wavehousela.com
GMAIL_APP_PASSWORD=rkyu btcu xqfn rbsx
SECRET_KEY=your_secret_key_here
```

### 3. Deploy
Railway will automatically:
- Install Python dependencies from `requirements.txt`
- Build the React frontend
- Start the Flask backend
- Provide a public URL

## 📧 Email Configuration

The system uses Gmail SMTP for sending emails. To set up:

1. **Gmail App Password**: Use the existing app password: `rkyu btcu xqfn rbsx`
2. **Email Address**: `letswork@wavehousela.com`

Emails are sent for:
- Booking confirmations to clients
- New booking notifications to admin
- Professional HTML templates with Wave House branding

## 🔐 Admin Access

- **URL**: `[your-domain]/admin`
- **Password**: `admin123`

Admin features:
- View all bookings with status
- Real-time statistics dashboard
- Client management
- Booking confirmation/cancellation

## 🎨 Design Features

- **Dark Theme**: Professional black/dark gray color scheme
- **Cyan Accents**: #00CED1 brand color throughout
- **Responsive Design**: Mobile-friendly layout
- **Professional Typography**: Clean, readable fonts
- **Wave House Branding**: Consistent visual identity

## 📱 Mobile Compatibility

The website is fully responsive and optimized for:
- Desktop computers
- Tablets
- Mobile phones
- Touch interactions

## 🔧 Local Development

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Setup
1. **Clone repository**
   ```bash
   git clone [your-repo-url]
   cd wave-house-booking-system
   ```

2. **Backend setup**
   ```bash
   pip install -r requirements.txt
   python src/main.py
   ```

3. **Frontend setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access locally**
   - Frontend: http://localhost:3001
   - Backend: http://localhost:5000
   - Admin: http://localhost:5000/admin

## 📊 Database Schema

### Tables
- **clients**: Client information (name, email, phone)
- **bookings**: Booking details (service, date, time, status)
- **blocked_slots**: Admin-blocked time slots

### Relationships
- One client can have multiple bookings
- Bookings reference client information
- Blocked slots prevent booking conflicts

## 🎯 Service Types

1. **Studio Access** - $150/hour
   - Full access to recording studio
   - Professional equipment included

2. **Engineer Request** - $200/hour
   - Professional engineer assistance
   - Technical support and guidance

3. **Mixing** - $300/song
   - Professional mixing services
   - High-quality audio production

## 📞 Contact Information

- **Email**: letswork@wavehousela.com
- **Phone**: (555) 123-4567
- **Address**: 123 Music Row, Los Angeles, CA 90028

## 🔄 Updates and Maintenance

To update the system:
1. Make changes to the code
2. Push to GitHub
3. Railway automatically redeploys
4. Test the updated system

## 🆘 Support

For technical issues or questions:
- Check Railway deployment logs
- Verify environment variables are set
- Ensure database connection is working
- Test email configuration

---

**Built with ❤️ for Wave House Recording Studio**

