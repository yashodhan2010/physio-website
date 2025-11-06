# 🔐 Secure Configuration Guide
# How to safely add your Gmail and AWS credentials

## ⚠️ IMPORTANT: Never commit sensitive credentials to Git!

This guide shows you how to securely configure your credentials without exposing them in your repository.

---

## 📧 Gmail Configuration (For Contact Forms)

### Step 1: Enable Gmail App Passwords

1. **Go to Google Account Settings**: https://myaccount.google.com/
2. **Security** → **2-Step Verification** (enable if not already)
3. **App Passwords** → **Select app: Mail** → **Generate**
4. **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

### Step 2: Update Your .env File

Edit the `.env` file in your project root:

```env
# Flask Configuration
SECRET_KEY=your-super-secret-production-key-change-this-to-something-random
FLASK_ENV=production

# Gmail Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=abcd efgh ijkl mnop
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Google Analytics & Ads (replace with your actual IDs)
GA_TRACKING_ID=G-XXXXXXXXXX
GOOGLE_ADS_CONVERSION_ID=AW-XXXXXXXXX
CONTACT_CONVERSION_LABEL=your_contact_label
APPOINTMENT_CONVERSION_LABEL=your_appointment_label
```

---

## ☁️ AWS Configuration (For Hosting)

### Method 1: AWS CLI Configuration (Recommended)

```powershell
# Install AWS CLI if not already installed
# Download from: https://aws.amazon.com/cli/

# Configure AWS credentials (will be stored securely)
aws configure

# Enter your credentials:
# AWS Access Key ID: AKIA...
# AWS Secret Access Key: your-secret-key
# Default region: us-east-1
# Default output format: json
```

### Method 2: Environment Variables (Alternative)

Add to your `.env` file:

```env
# AWS Configuration
AWS_ACCESS_KEY_ID=AKIA...your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_DEFAULT_REGION=us-east-1
```

---

## 🔒 Security Best Practices

### ✅ What's Protected by .gitignore:
- `.env` files (your credentials)
- `.aws/` directory (AWS credentials)
- `venv/` directory (virtual environment)
- `__pycache__/` (Python cache files)
- `.vscode/` (IDE settings)

### ✅ Safe to Commit:
- `.env.example` (template without real credentials)
- All code files (`.py`, `.html`, `.css`, `.js`)
- Configuration templates
- Documentation

---

## 🚀 Complete Setup Process

### 1. Configure Gmail:
```powershell
# Edit your .env file
notepad .env

# Add your Gmail credentials (see Gmail section above)
```

### 2. Configure AWS:
```powershell
# Option A: Use AWS CLI (recommended)
aws configure

# Option B: Add to .env file (see AWS section above)
```

### 3. Test Locally:
```powershell
# Activate environment
venv\Scripts\activate

# Run with real credentials
python app_simple.py
```

### 4. Test Contact Form:
1. Go to http://localhost:5000/contact
2. Fill out the form
3. Submit - you should receive an email!

---

## 🌐 Production Deployment

### For AWS Elastic Beanstalk:
```powershell
# Set environment variables (replaces .env file)
eb setenv SECRET_KEY=your-production-secret-key \
         MAIL_USERNAME=your-email@gmail.com \
         MAIL_PASSWORD=your-16-char-app-password \
         MAIL_DEFAULT_SENDER=your-email@gmail.com \
         GA_TRACKING_ID=G-XXXXXXXXXX \
         GOOGLE_ADS_CONVERSION_ID=AW-XXXXXXXXX
```

---

## 🔍 How to Get Your Google Ads IDs

### Google Analytics:
1. Go to https://analytics.google.com/
2. Create property for your website
3. Get your **Measurement ID** (starts with G-)

### Google Ads:
1. Go to https://ads.google.com/
2. **Tools & Settings** → **Conversions**
3. **Create Conversion Action**:
   - **Contact Form Submission**
   - **Appointment Booking**
4. Get your **Conversion ID** (starts with AW-) and **labels**

---

## 📋 Example .env File (Template)

```env
# Flask Configuration
SECRET_KEY=generate-a-random-secret-key-here
FLASK_ENV=production

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=yourname@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=yourname@gmail.com

# Google Analytics & Ads
GA_TRACKING_ID=G-XXXXXXXXXX
GOOGLE_ADS_CONVERSION_ID=AW-XXXXXXXXX
CONTACT_CONVERSION_LABEL=contact_form_submit
APPOINTMENT_CONVERSION_LABEL=appointment_booking

# AWS (optional - use aws configure instead)
# AWS_ACCESS_KEY_ID=AKIA...
# AWS_SECRET_ACCESS_KEY=...
# AWS_DEFAULT_REGION=us-east-1
```

---

## 🆘 Troubleshooting

### Gmail Issues:
- **"Less secure app access"**: Use App Passwords instead
- **"Authentication failed"**: Double-check app password
- **"SMTP timeout"**: Check firewall settings

### AWS Issues:
- **"Credentials not found"**: Run `aws configure`
- **"Permission denied"**: Check IAM permissions
- **"Region errors"**: Set correct region in config

### Environment Issues:
- **"Environment variable not found"**: Check `.env` file exists
- **"python-dotenv not found"**: Run `pip install python-dotenv`

---

## 🎯 Quick Test Commands

```powershell
# Test email configuration
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Email:', os.getenv('MAIL_USERNAME'))"

# Test AWS configuration
aws sts get-caller-identity

# Test website with real config
python app_simple.py
```

---

## ⚡ Ready to Go Live?

Once you have:
- ✅ Gmail app password configured
- ✅ AWS credentials set up
- ✅ Google Ads tracking IDs
- ✅ Tested locally

Follow the `COMPLETE_AWS_GUIDE.md` for deployment!

---

**🔒 Your credentials are now secure and ready for production! 🚀**