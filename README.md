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

<img width="1843" height="1035" alt="image" src="https://github.com/user-attachments/assets/c77b27ba-4446-43d1-bf36-9ea9e890420f" />


### Leaderboard

<img width="1842" height="1021" alt="image" src="https://github.com/user-attachments/assets/15322c61-dd12-4d86-abfc-16fc53b17c1d" />


### Study Timer

<img width="1847" height="1025" alt="image" src="https://github.com/user-attachments/assets/bce852cd-a596-43c9-a624-e7cf690309b3" />


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


