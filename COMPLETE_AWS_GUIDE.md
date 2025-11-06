# 🚀 Complete AWS Hosting Guide for Your Physiotherapy Website

## ✅ Your website is ready! Here are 3 ways to host it on AWS:

---

## 🥇 **METHOD 1: AWS Elastic Beanstalk (RECOMMENDED)**
*Easiest and fastest deployment - Perfect for beginners*

### **Step 1: Install Required Tools**

1. **Install AWS CLI:**
   - Download from: https://aws.amazon.com/cli/
   - Or run: `winget install Amazon.AWSCLI`

2. **Install EB CLI:**
   ```powershell
   pip install awsebcli
   ```

### **Step 2: Setup AWS Account**

1. **Create AWS Account:** https://aws.amazon.com/
2. **Create IAM User:**
   - Go to AWS Console > IAM > Users > Create User
   - Give it "AdministratorAccess" policy (for now)
   - Save the Access Key ID and Secret Access Key

3. **Configure AWS CLI:**
   ```powershell
   aws configure
   ```
   Enter:
   - AWS Access Key ID: [Your access key]
   - AWS Secret Access Key: [Your secret key]  
   - Default region: us-east-1
   - Default output format: json

### **Step 3: Deploy Your Website**

1. **Initialize EB Application:**
   ```powershell
   eb init physio-website --platform python-3.11 --region us-east-1
   ```

2. **Create Environment:**
   ```powershell
   eb create production --cname physio-website-prod
   ```
   *(This takes 5-10 minutes)*

3. **Set Environment Variables:**
   ```powershell
   eb setenv SECRET_KEY=your-super-secret-production-key-123 MAIL_USERNAME=your-email@gmail.com MAIL_PASSWORD=your-gmail-app-password MAIL_DEFAULT_SENDER=your-email@gmail.com
   ```

4. **Deploy:**
   ```powershell
   eb deploy
   ```

5. **Open Your Live Website:**
   ```powershell
   eb open
   ```

**🎉 Your website is now live!** 
URL will be: `https://physio-website-prod.us-east-1.elasticbeanstalk.com`

**💰 Cost: $5-15/month** for small traffic

---

## 🥈 **METHOD 2: Docker on AWS App Runner** 
*Modern containerized deployment*

### **Step 1: Build Docker Image**
```powershell
docker build -t physio-website .
```

### **Step 2: Push to AWS ECR**
```powershell
# Create ECR repository
aws ecr create-repository --repository-name physio-website --region us-east-1

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin [YOUR-ACCOUNT-ID].dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag physio-website:latest [YOUR-ACCOUNT-ID].dkr.ecr.us-east-1.amazonaws.com/physio-website:latest
docker push [YOUR-ACCOUNT-ID].dkr.ecr.us-east-1.amazonaws.com/physio-website:latest
```

### **Step 3: Create App Runner Service**
1. Go to AWS Console > App Runner > Create Service
2. Choose "Container registry" > ECR
3. Select your image
4. Configure auto-scaling (start with 1 instance)
5. Deploy!

**💰 Cost: $3-10/month** for small traffic

---

## 🥉 **METHOD 3: Full Infrastructure (CloudFormation)**
*Complete control with load balancers, auto-scaling*

### **Deploy Infrastructure:**
```powershell
aws cloudformation create-stack \
  --stack-name physio-website \
  --template-body file://aws-cloudformation.yml \
  --parameters ParameterKey=KeyPairName,ParameterValue=your-key-pair \
               ParameterKey=DomainName,ParameterValue=yourdomain.com \
  --capabilities CAPABILITY_IAM
```

**💰 Cost: $15-50/month** (includes load balancer, multiple instances)

---

## 🌐 **Setting Up Your Domain Name**

### **Option A: Register New Domain**
1. Go to AWS Route 53 > Register Domain
2. Search and register your domain (e.g., physiowell.com)

### **Option B: Use Existing Domain**
1. Update nameservers to AWS Route 53
2. Create hosted zone in Route 53
3. Add A record pointing to your website

### **Add SSL Certificate (HTTPS)**
```powershell
# Request SSL certificate
aws acm request-certificate \
  --domain-name yourdomain.com \
  --subject-alternative-names www.yourdomain.com \
  --validation-method DNS
```

---

## 📧 **Email Configuration for Contact Forms**

### **Gmail Setup:**
1. **Enable 2FA** on your Gmail account
2. **Create App Password:**
   - Go to Google Account Settings > Security
   - Turn on 2-factor authentication
   - Generate App Password for "Mail"
3. **Use this password** in your environment variables

### **Environment Variables for Production:**
```powershell
eb setenv SECRET_KEY=super-secret-production-key-change-this \
         MAIL_USERNAME=your-email@gmail.com \
         MAIL_PASSWORD=your-16-char-app-password \
         MAIL_DEFAULT_SENDER=your-email@gmail.com \
         GA_TRACKING_ID=G-XXXXXXXXXX \
         GOOGLE_ADS_CONVERSION_ID=AW-XXXXXXXXX
```

---

## 📈 **Google Ads Setup**

### **Step 1: Create Google Ads Account**
1. Go to https://ads.google.com/
2. Create account and billing setup

### **Step 2: Set Up Conversion Tracking**
1. Go to Tools & Settings > Conversions
2. Create "Contact Form Submission" conversion
3. Create "Appointment Booking" conversion
4. Get your conversion IDs and labels

### **Step 3: Update Tracking Codes**
1. In your templates, replace:
   - `GA_TRACKING_ID` with your Google Analytics ID
   - `AW-CONVERSION_ID` with your Google Ads conversion ID
   - `CONTACT_LABEL` and `APPOINTMENT_LABEL` with your labels

---

## 🔧 **Customization Before Going Live**

### **Update Your Information:**
1. **Company Name:** Replace "PhysioWell" with your clinic name
2. **Contact Details:** Update phone, email, address in all templates
3. **Services:** Edit `/templates/services.html` with your offerings  
4. **About Page:** Update `/templates/about.html` with your team info
5. **Photos:** Add your clinic photos to `/static/images/`

### **Branding:**
1. **Colors:** Update CSS variables in `/static/css/style.css`
2. **Logo:** Replace the text logo with your clinic logo
3. **Content:** Customize all placeholder content

---

## 📊 **Monitoring & Maintenance**

### **Check Website Health:**
```powershell
# Check EB health
eb health

# View logs
eb logs --all

# Update application
eb deploy
```

### **Cost Monitoring:**
1. Set up billing alerts in AWS Console
2. Use AWS Cost Explorer to track spending
3. Consider reserved instances for cost savings

---

## 🆘 **Troubleshooting**

### **Common Issues:**

1. **Application won't start:**
   ```powershell
   eb logs --all
   ```
   - Check Python version compatibility
   - Verify all dependencies in requirements.txt

2. **Email not working:**
   - Verify Gmail app password is correct
   - Check AWS security groups allow outbound SMTP

3. **High costs:**
   - Start with t3.micro instances
   - Use auto-scaling to handle traffic spikes
   - Monitor with CloudWatch

### **Useful Commands:**
```powershell
# Check status
eb status

# SSH to instance (if needed)
eb ssh

# Update environment variables
eb setenv KEY=value

# Scale application
eb scale 2

# Terminate environment (to save costs)
eb terminate production
```

---

## 🎯 **Next Steps After Deployment**

1. **Test all forms** on the live website
2. **Set up Google Analytics** and Google Ads campaigns
3. **Submit to Google Search Console** for SEO
4. **Create backup schedule** for your website
5. **Monitor performance** and costs

---

## 💡 **Pro Tips**

1. **Start with Elastic Beanstalk** - it's the easiest
2. **Use t3.micro instances** to keep costs low initially
3. **Set up billing alerts** to avoid surprises
4. **Test everything** on the staging environment first
5. **Keep your AWS credentials secure**

**Your professional physiotherapy website is ready for the world! 🌍**

Need help? The AWS documentation is excellent, and their support is responsive for any issues.