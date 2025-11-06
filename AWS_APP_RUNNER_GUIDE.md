# AWS App Runner Deployment Guide

## 🏃‍♂️ Why AWS App Runner is Perfect for Your Physio Website

- **Simple**: No server management needed
- **Cost-effective**: ~$7-15/month for typical traffic
- **Auto-scaling**: Handles traffic spikes automatically
- **HTTPS**: SSL certificate included
- **Custom domains**: Easy to add your own domain

## 🚀 Quick Deployment Steps

### **1. Build and Push to ECR**
```powershell
# Run the automated deployment script
.\deploy-production.ps1 -Platform aws-apprunner
```

### **2. Create App Runner Service**
1. Go to [AWS App Runner Console](https://console.aws.amazon.com/apprunner/)
2. Click "Create service"
3. Choose "Container registry" → "Amazon ECR"
4. Select your repository: `physio-website-prod`
5. Use these settings:

## ⚙️ App Runner Configuration

### **Container Settings:**
- **Port**: `5000`
- **Start command**: `gunicorn --bind 0.0.0.0:5000 --workers 2 application:app`
- **Environment**: `production`

### **Instance Configuration:**
- **CPU**: 0.25 vCPU (or 0.5 vCPU for better performance)
- **Memory**: 0.5 GB (or 1 GB for better performance)
- **Auto scaling**: 1-10 instances

### **Environment Variables:**
```
FLASK_ENV=production
MAIL_USERNAME=your.email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
SECRET_KEY=your-strong-secret-key
GOOGLE_ADS_CONVERSION_ID=AW-123456789
GA_TRACKING_ID=G-ABCDEFGHIJ
```

## 🔐 Security Best Practices

### **Environment Variables in App Runner:**
1. In App Runner console → Service → Configuration
2. Add environment variables securely
3. Never put credentials in Docker image

### **Required Environment Variables:**
- ✅ `FLASK_ENV=production`
- ✅ `MAIL_USERNAME` (your Gmail)
- ✅ `MAIL_PASSWORD` (Gmail app password)
- ✅ `SECRET_KEY` (generate strong random key)
- 📊 `GOOGLE_ADS_CONVERSION_ID` (optional)
- 📊 `GA_TRACKING_ID` (optional)

## 💰 Cost Estimation

### **Basic Configuration:**
- **0.25 vCPU + 0.5 GB**: ~$7/month
- **Custom domain**: Free
- **HTTPS certificate**: Free
- **Data transfer**: ~$1-3/month

### **High-performance Configuration:**
- **0.5 vCPU + 1 GB**: ~$14/month
- Better for higher traffic

## 🌐 Custom Domain Setup

1. **In App Runner Console:**
   - Go to your service → Custom domains
   - Add your domain (e.g., `physiowell.com`)

2. **In your DNS provider:**
   - Add CNAME record pointing to App Runner URL
   - HTTPS certificate auto-generated

## 📊 Monitoring & Logs

### **CloudWatch Integration:**
- Automatic logging to CloudWatch
- Monitor performance metrics
- Set up alarms for errors

### **Health Checks:**
- App Runner automatically monitors `/` endpoint
- Restarts unhealthy instances
- Built-in load balancing

## 🔄 Continuous Deployment

### **Option 1: Manual Updates**
```powershell
# Push new image and update service
.\deploy-production.ps1 -Platform aws-apprunner
```

### **Option 2: Auto-deploy from GitHub**
- Connect App Runner to your GitHub repo
- Auto-deploys on push to main branch
- No manual ECR pushes needed

## 🚨 Troubleshooting

### **Common Issues:**
1. **Service won't start**: Check environment variables
2. **502 errors**: Verify port 5000 in configuration
3. **Email not working**: Verify Gmail app password
4. **Slow performance**: Increase CPU/memory allocation

### **Debugging:**
```powershell
# Check App Runner service logs
aws logs tail /aws/apprunner/physio-website/application --follow
```

## ✅ Deployment Checklist

- [ ] AWS CLI configured
- [ ] `.env` file with production credentials
- [ ] Docker image built and pushed to ECR
- [ ] App Runner service created
- [ ] Environment variables configured
- [ ] Custom domain added (optional)
- [ ] Contact form tested
- [ ] Google Ads tracking verified

---

**Next Step**: Run `.\deploy-production.ps1 -Platform aws-apprunner` to get started!