# Study Time Tracker

A simple Django app to track study time and compete with friends.

## Features
- Study Timer (Start/Stop)
- Daily Leaderboard
- Study History
- Responsive and minimal UI

## Setup Locally
1. Clone the repo.
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```
6. Run server:
   ```bash
   python manage.py runserver
   ```
7. Visit http://127.0.0.1:8000

## Deployment (Railway/Render)
1. Fork this repo.
2. Connect to Railway/Render.
3. Set Environment Variable `SECRET_KEY` and `DATABASE_URL` (if strictly required, though `dj_database_url` defaults to sqlite if missing, production usually provides PostgreSQL).
4. Build command: `pip install -r requirements.txt && python manage.py migrate`
5. Start command: `gunicorn config.wsgi`

## Tech Stack
- Django 5.x
- Gunicorn
- Whitenoise
- Vanilla JS/CSS
