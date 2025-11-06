# PowerShell script to start the physiotherapy website (Development Mode)
Write-Host "Starting PhysioWell Website (Development)..." -ForegroundColor Green
Write-Host "Using app_simple.py for local development" -ForegroundColor Cyan
Write-Host ""

# Navigate to project directory
Set-Location "c:\Users\Yashodhan\OneDrive\Documents\Websites\physio-website"

# Activate virtual environment
& "venv\Scripts\Activate.ps1"

# Start the application
Write-Host "Website starting at http://localhost:5000" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python app_simple.py