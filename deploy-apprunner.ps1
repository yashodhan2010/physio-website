# AWS App Runner Deployment Script
# Optimized for physio website deployment

param(
    [string]$Region = "us-east-1",
    [string]$ServiceName = "physio-website",
    [switch]$CreateService,
    [switch]$UpdateService
)

$ErrorActionPreference = "Stop"

Write-Host "🏃‍♂️ AWS App Runner Deployment for Physio Website" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# Check prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow

# Check AWS CLI
try {
    $awsVersion = aws --version
    Write-Host "✅ AWS CLI: $awsVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ AWS CLI not found. Install from https://aws.amazon.com/cli/" -ForegroundColor Red
    exit 1
}

# Check Docker
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker not found. Install Docker Desktop" -ForegroundColor Red
    exit 1
}

# Check .env file
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "📋 Create .env with these variables:" -ForegroundColor Yellow
    Write-Host "  MAIL_USERNAME=your.email@gmail.com" -ForegroundColor Cyan
    Write-Host "  MAIL_PASSWORD=your-app-password" -ForegroundColor Cyan
    Write-Host "  SECRET_KEY=your-secret-key" -ForegroundColor Cyan
    exit 1
}

# Get AWS account info
$AWS_ACCOUNT_ID = aws sts get-caller-identity --query Account --output text
$ECR_REPOSITORY = "$ServiceName-prod"
$ECR_URI = "$AWS_ACCOUNT_ID.dkr.ecr.$Region.amazonaws.com/$ECR_REPOSITORY"
$IMAGE_TAG = "latest"

Write-Host "📋 Deployment Details:" -ForegroundColor Cyan
Write-Host "  Account ID: $AWS_ACCOUNT_ID" -ForegroundColor White
Write-Host "  Region: $Region" -ForegroundColor White
Write-Host "  ECR Repository: $ECR_REPOSITORY" -ForegroundColor White
Write-Host "  Service Name: $ServiceName" -ForegroundColor White

# Step 1: Create ECR repository if it doesn't exist
Write-Host "🏗️ Setting up ECR repository..." -ForegroundColor Yellow
try {
    aws ecr describe-repositories --repository-names $ECR_REPOSITORY --region $Region | Out-Null
    Write-Host "✅ ECR repository exists" -ForegroundColor Green
} catch {
    Write-Host "📦 Creating ECR repository..." -ForegroundColor Yellow
    aws ecr create-repository --repository-name $ECR_REPOSITORY --region $Region | Out-Null
    Write-Host "✅ ECR repository created" -ForegroundColor Green
}

# Step 2: Build Docker image
Write-Host "🐳 Building Docker image..." -ForegroundColor Yellow
docker build -t $ECR_REPOSITORY .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Docker image built successfully" -ForegroundColor Green

# Step 3: Login to ECR
Write-Host "🔐 Logging into ECR..." -ForegroundColor Yellow
aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin $ECR_URI
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ECR login failed!" -ForegroundColor Red
    exit 1
}

# Step 4: Tag and push image
Write-Host "⬆️ Pushing image to ECR..." -ForegroundColor Yellow
docker tag "$ECR_REPOSITORY:$IMAGE_TAG" "$ECR_URI:$IMAGE_TAG"
docker push "$ECR_URI:$IMAGE_TAG"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker push failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Image pushed successfully" -ForegroundColor Green

# Step 5: Create App Runner configuration
$appRunnerConfig = @"
{
  "ServiceName": "$ServiceName",
  "SourceConfiguration": {
    "ImageRepository": {
      "ImageIdentifier": "$ECR_URI:$IMAGE_TAG",
      "ImageConfiguration": {
        "Port": "5000",
        "RuntimeEnvironmentVariables": {
          "FLASK_ENV": "production"
        }
      },
      "ImageRepositoryType": "ECR",
      "AutoDeploymentsEnabled": true
    }
  },
  "InstanceConfiguration": {
    "Cpu": "0.25 vCPU",
    "Memory": "0.5 GB"
  },
  "HealthCheckConfiguration": {
    "Protocol": "HTTP",
    "Path": "/",
    "IntervalSeconds": 20,
    "TimeoutSeconds": 10,
    "HealthyThresholdCount": 1,
    "UnhealthyThresholdCount": 5
  }
}
"@

$appRunnerConfig | Out-File -FilePath "apprunner-config.json" -Encoding UTF8

# Step 6: Deploy to App Runner
if ($CreateService) {
    Write-Host "🚀 Creating App Runner service..." -ForegroundColor Yellow
    try {
        $serviceArn = aws apprunner create-service --cli-input-json file://apprunner-config.json --query "Service.ServiceArn" --output text
        Write-Host "✅ App Runner service created!" -ForegroundColor Green
        Write-Host "🔗 Service ARN: $serviceArn" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ Failed to create App Runner service" -ForegroundColor Red
        Write-Host "💡 Service might already exist. Try -UpdateService instead" -ForegroundColor Yellow
    }
} elseif ($UpdateService) {
    Write-Host "🔄 Updating App Runner service..." -ForegroundColor Yellow
    try {
        $serviceArn = aws apprunner list-services --query "ServiceSummaryList[?ServiceName=='$ServiceName'].ServiceArn" --output text
        if ($serviceArn) {
            aws apprunner update-service --service-arn $serviceArn --source-configuration "ImageRepository={ImageIdentifier=$ECR_URI:$IMAGE_TAG,ImageConfiguration={Port=5000,RuntimeEnvironmentVariables={FLASK_ENV=production}},ImageRepositoryType=ECR}"
            Write-Host "✅ App Runner service updated!" -ForegroundColor Green
        } else {
            Write-Host "❌ Service '$ServiceName' not found" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Failed to update App Runner service" -ForegroundColor Red
    }
} else {
    Write-Host "📋 Image ready for deployment!" -ForegroundColor Green
    Write-Host "🔗 ECR Image: $ECR_URI:$IMAGE_TAG" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🚀 Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Run with -CreateService to create new service" -ForegroundColor Cyan
    Write-Host "  2. Run with -UpdateService to update existing service" -ForegroundColor Cyan
    Write-Host "  3. Or create manually in AWS Console:" -ForegroundColor Cyan
    Write-Host "     https://console.aws.amazon.com/apprunner/" -ForegroundColor Blue
}

# Cleanup
Remove-Item "apprunner-config.json" -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "🎉 Deployment completed!" -ForegroundColor Green
Write-Host "📋 Don't forget to set environment variables in App Runner console:" -ForegroundColor Yellow
Write-Host "  • MAIL_USERNAME" -ForegroundColor Cyan
Write-Host "  • MAIL_PASSWORD" -ForegroundColor Cyan  
Write-Host "  • SECRET_KEY" -ForegroundColor Cyan
Write-Host "  • GOOGLE_ADS_CONVERSION_ID (optional)" -ForegroundColor Cyan