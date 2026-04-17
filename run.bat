@echo off
echo ========================================
echo    Cafe Management System
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Install requirements
echo Installing/Updating dependencies...
pip install -r requirements.txt --quiet
echo.

REM Run the application
echo Starting Cafe Management System...
echo.
echo Application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
echo Admin Login: admin@cafe.com / admin123
echo.
python app.py

pause
