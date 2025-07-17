# 🚀 Railway Deployment Instructions

Quick deployment guide for Wave House booking system.

## 📋 Prerequisites
- GitHub account
- Railway account ([railway.app](https://railway.app))
- This complete codebase

## 🚂 Deploy to Railway

### 1. Upload to GitHub
1. Create new repository: `wave-house-booking-system`
2. Upload all files from this directory
3. Make repository public

### 2. Connect to Railway
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your `wave-house-booking-system` repository
4. Click "Deploy Now"

### 3. Add Database
1. Click "New Service" → "Database" → "PostgreSQL"
2. Railway automatically provides `DATABASE_URL`

### 4. Set Environment Variables
In Railway dashboard, add these variables:

```
GMAIL_EMAIL=letswork@wavehousela.com
GMAIL_APP_PASSWORD=rkyu btcu xqfn rbsx
SECRET_KEY=wave-house-secret-key-2024
FLASK_ENV=production
```

### 5. Generate Domain
1. Go to "Settings" → "Domains"
2. Click "Generate Domain"
3. Get your public URL: `https://your-app.up.railway.app`

## ✅ Test Your Deployment

- **Website**: Visit your Railway URL
- **Booking**: Test form submissions
- **Admin**: Access `/admin` (password: admin123)
- **Email**: Check letswork@wavehousela.com for notifications

## 🔧 Troubleshooting

**Build Issues**: Check `requirements.txt` and `Procfile`  
**Database Issues**: Verify PostgreSQL service is running  
**Email Issues**: Confirm Gmail credentials are correct  

Your Wave House booking system should now be live! 🎵

