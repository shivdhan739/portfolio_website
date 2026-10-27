@echo off
REM Double-click this file. It sets everything up and starts the website.
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo [1/5] Creating virtual environment...
    py -m venv venv || python -m venv venv
)

echo [2/5] Installing packages...
"venv\Scripts\python.exe" -m pip install --upgrade pip
"venv\Scripts\python.exe" -m pip install -r requirements-local.txt

if not exist ".env" (
    echo Creating .env from .env.example - open it and fill your passwords.
    copy ".env.example" ".env"
)

echo [3/5] Checking project...
"venv\Scripts\python.exe" manage.py check > error_log.txt 2>&1
if errorlevel 1 (
    echo.
    echo ===== ERROR FOUND. Details are saved in error_log.txt - send that file to Claude =====
    type error_log.txt
    pause
    exit /b 1
)

echo [4/5] Preparing database...
"venv\Scripts\python.exe" manage.py migrate

echo [5/5] Starting website: http://127.0.0.1:8000
"venv\Scripts\python.exe" manage.py runserver
pause
