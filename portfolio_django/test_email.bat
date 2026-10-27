@echo off
REM Sends a test email to check your Gmail / Brevo settings.
cd /d "%~dp0"
"venv\Scripts\python.exe" manage.py test_email
pause
