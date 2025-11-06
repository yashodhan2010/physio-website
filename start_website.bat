@echo off
echo Starting PhysioWell Website (Development Mode)...
echo Using app_simple.py for local development
echo.

REM Navigate to project directory
cd /d "c:\Users\Yashodhan\OneDrive\Documents\Websites\physio-website"

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the application
echo Website starting at http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app_simple.py

pause