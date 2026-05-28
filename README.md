# Study Time Tracker

Study Time Tracker is a Django-based web application that helps students track their study sessions, compete with friends through leaderboards, and monitor daily study progress.

The application provides a clean and responsive interface focused on productivity and consistency.

---

## Features

* Study Timer (Start / Stop)
* Daily Leaderboard
* Study History Tracking
* User Authentication
* Responsive and Minimal UI
* Real-time Study Session Tracking

---

## Live Demo

Live Website:

https://muhammad0221.pythonanywhere.com

---

## Screenshots

> Add screenshots of your application here.

### Dashboard

<img width="1842" height="1028" alt="image" src="https://github.com/user-attachments/assets/0433acd2-ad2a-4457-82eb-4a71ca272c5c" />

### Leaderboard

<img width="1837" height="1025" alt="image" src="https://github.com/user-attachments/assets/590702d5-38e2-4146-a3ba-5cebe7928676" />

### Study Timer

<img width="1840" height="1015" alt="image" src="https://github.com/user-attachments/assets/ea0dc4e1-1a8a-4237-85b9-8b006f501c40" />

---

## Tech Stack

* Django 5.x
* Python
* Gunicorn
* Whitenoise
* HTML/CSS
* Vanilla JavaScript
* SQLite

---

## Installation & Local Setup

### Clone Repository

```bash
git clone https://github.com/muhammad-abdul-rehman1/study-time.git
cd study-time
```

---

### Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / Mac

```bash
python -m venv venv
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Apply Database Migrations

```bash
python manage.py migrate
```

---

### Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

---

### Run Development Server

```bash
python manage.py runserver
```

Visit:

```text
http://127.0.0.1:8000
```

---

## Deployment

The application is currently deployed on PythonAnywhere.

### PythonAnywhere Deployment

1. Upload project to PythonAnywhere
2. Create virtual environment
3. Install requirements
4. Configure WSGI file
5. Run migrations
6. Collect static files

### Collect Static Files

```bash
python manage.py collectstatic
```

---

## Project Structure

```bash
study-time/
├── config/
├── tracker/
├── templates/
├── static/
├── media/
├── db.sqlite3
├── manage.py
└── requirements.txt
```

---

## Future Improvements

* Friends System
* Study Goals
* Weekly Analytics
* Dark Mode
* Mobile App Version
* Pomodoro Timer
* Notifications & Reminders

---

## Author

Muhammad Abdul Rehman

GitHub:
https://github.com/muhammad-abdul-rehman1

---


