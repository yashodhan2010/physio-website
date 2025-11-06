# Physiotherapy Website - Complete Setup & Deployment Guide

## 🏥 Project Overview
A professional physiotherapy website built with Flask, featuring contact forms, appointment booking, and Google Ads integration.

## 📁 Project Structure
```
physio-website/
├── app_simple.py          # Main Flask application (recommended)
├── application.py         # AWS Elastic Beanstalk version
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── .env                  # Environment variables (add your credentials)
├── .env.example          # Template for environment variables
├── .gitignore           # Git ignore file
├── static/              # CSS, JS, images
├── templates/           # HTML templates
└── venv/               # Virtual environment
```

## 🚀 Quick Start

### 1. Local Development
```powershell
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the website
python app_simple.py
```
Visit: http://127.0.0.1:5000

### 2. Production Scripts
- `start_website.bat` - Windows batch script
- `start_website.ps1` - PowerShell script with error handling

## 🔐 Environment Configuration

### Required Environment Variables (.env file):
```properties
# Flask
SECRET_KEY=your-secret-key-here
FLASK_ENV=production

# Gmail (for contact forms)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password

# Google Analytics & Ads
GA_TRACKING_ID=G-XXXXXXXXXX
GOOGLE_ADS_CONVERSION_ID=AW-XXXXXXXXX
```

### Setting Up Gmail App Password:
1. Go to https://myaccount.google.com/apppasswords
2. Generate app password for "Mail"
3. Use the 16-character password in MAIL_PASSWORD

### Setting Up Google Ads:
1. Create conversion actions in Google Ads
2. Copy your Conversion ID (AW-XXXXXXXXX format)
3. Add tracking labels for contact forms and appointments

## 🌐 AWS Deployment Options

### Option 1: AWS App Runner (Recommended)
```powershell
# 1. Build Docker image
docker build -t physio-website .

# 2. Push to ECR
aws ecr create-repository --repository-name physio-website
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker tag physio-website:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/physio-website:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/physio-website:latest

# 3. Create App Runner service via AWS Console
```

### Option 2: AWS Elastic Beanstalk
```powershell
# Install EB CLI
pip install awsebcli

# Initialize and deploy
eb init physio-website
eb create physio-website-env
eb deploy
```

### Option 3: Docker on EC2
1. Launch EC2 instance
2. Install Docker
3. Pull and run your container

## 💰 Cost Estimates
- **App Runner**: ~$7-15/month
- **Elastic Beanstalk**: ~$10-25/month
- **EC2 t3.micro**: ~$8-12/month

## 🔧 Troubleshooting

### Common Issues:
1. **Flask-Mail errors**: Use built-in smtplib (already implemented)
2. **Virtual environment**: Always activate before running
3. **Port conflicts**: Change port in app_simple.py if needed
4. **Email not sending**: Check Gmail app password and 2FA settings

### Development Tips:
- Use `app_simple.py` for local development
- Use `application.py` for AWS Elastic Beanstalk
- Test email functionality with real Gmail credentials
- Monitor logs for any errors

## 📞 Support Features
- **Contact Form**: Sends emails via Gmail SMTP
- **Appointment Booking**: Professional scheduling interface
- **Google Ads Tracking**: Conversion tracking on all forms
- **Responsive Design**: Works on all devices
- **SEO Optimized**: Professional healthcare SEO

## 🔒 Security Best Practices
- Never commit `.env` file to git
- Use strong secret keys in production
- Enable 2FA on Gmail account
- Use IAM roles for AWS credentials
- Regular security updates

---

**Need Help?** Check the Flask documentation or AWS documentation for specific deployment issues.