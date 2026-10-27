@echo off
REM Double-click once to create your /admin login.
cd /d "%~dp0"
"venv\Scripts\python.exe" manage.py createsuperuser
pause
