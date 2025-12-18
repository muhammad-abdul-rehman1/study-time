@echo off
echo Starting Study Time Tracker...
".\venv\Scripts\python.exe" manage.py migrate
".\venv\Scripts\python.exe" manage.py runserver
pause
