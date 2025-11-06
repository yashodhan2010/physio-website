# 🚀 How to Run Your Physiotherapy Website

## Quick Start (Choose one method):

### Method 1: Double-click to start
1. **Double-click** `start_website.bat` 
2. **Website opens at**: http://localhost:5000
3. **To stop**: Close the command window or press Ctrl+C

### Method 2: PowerShell
```powershell
# Navigate to project
cd "c:\Users\Yashodhan\OneDrive\Documents\Websites\physio-website"

# Activate environment
venv\Scripts\activate

# Start website
python app_simple.py
```

### Method 3: One-click PowerShell
1. Right-click `start_website.ps1` 
2. Select "Run with PowerShell"

## 🌐 Access Your Website:
- **Local**: http://127.0.0.1:5000
- **Network**: http://192.168.31.41:5000 (accessible from other devices on your network)

## 📱 Test on Mobile:
Your website is mobile-responsive! Test it by:
1. Connect your phone to the same WiFi
2. Open browser and go to: http://192.168.31.41:5000

## 🛑 How to Stop:
- Press `Ctrl+C` in the terminal/command prompt
- Or close the command window

## 🔧 Troubleshooting:

### If you get "Permission Denied" for PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### If port 5000 is busy:
```powershell
# Kill any running Python processes
Get-Process python | Stop-Process -Force

# Or change port in app_simple.py (line 113):
# app.run(debug=True, host='0.0.0.0', port=5001)
```

### If virtual environment not found:
```powershell
# Recreate virtual environment
python -m venv venv
venv\Scripts\activate
pip install flask python-dotenv
```

## 🚀 Ready for Production?
See `COMPLETE_AWS_GUIDE.md` for AWS deployment instructions.

---

**Your professional physiotherapy website is ready! 🏥✨**