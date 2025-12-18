@echo off
echo ==========================================
echo Setting up Study Time for the first time...
echo ==========================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed! Please install Python 3.12+ and try again.
    pause
    exit /b
)

REM Create virtual environment if it fails
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv and install requirements
echo Installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

REM Run Migrations
echo Setting up database...
python manage.py migrate

echo.
echo ==========================================
echo Setup Complete! Starting server...
echo ==========================================
python manage.py runserver 8001
pause
