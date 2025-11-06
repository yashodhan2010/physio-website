# Physiotherapy Website

A professional physiotherapy website built with Flask, optimized for AWS App Runner deployment.

## 🏥 Features

- **Professional Design**: Modern, responsive healthcare website
- **Contact Forms**: Secure contact and appointment booking
- **Email Integration**: Gmail SMTP for form submissions
- **Google Ads Tracking**: Conversion tracking for marketing
- **AWS App Runner**: Simple, scalable deployment

## 🚀 Quick Start

### Local Development
```powershell
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
python app_simple.py
```

Visit: http://127.0.0.1:5000

### AWS App Runner Deployment
```powershell
# Deploy to AWS App Runner
.\deploy-apprunner.ps1 -CreateService
```

## 🔐 Configuration

Create `.env` file with your credentials:
```properties
MAIL_USERNAME=your.email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
SECRET_KEY=your-secret-key
GOOGLE_ADS_CONVERSION_ID=AW-123456789
```

## 📁 Project Structure

```
physio-website/
├── app_simple.py              # Development server
├── application.py             # Production server (App Runner)
├── Dockerfile                 # Container configuration
├── deploy-apprunner.ps1       # Deployment script
├── requirements.txt           # Python dependencies
├── .env                       # Your credentials (not in git)
├── static/                    # CSS, JS, images
└── templates/                 # HTML templates
```

## 💰 Cost Estimate

- **AWS App Runner**: ~$7-15/month
- **Custom Domain**: Free
- **HTTPS Certificate**: Free

## 📖 Documentation

- **[AWS App Runner Guide](AWS_APP_RUNNER_GUIDE.md)**: Complete deployment instructions
- **[Environment Template](apprunner-env-template.txt)**: Required environment variables

---

**Built for healthcare professionals** • **Mobile-optimized** • **Easy to deploy**