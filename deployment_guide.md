# How to Deploy "Study Time" to Render (Free)

This guide will show you how to put your website online so your friends can use it. We will use **Render.com** because it is free and easy for Django apps.

## Prerequisites
1.  **GitHub Account**: You need to upload your code to GitHub first.
2.  **Render Account**: Sign up at [dashboard.render.com](https://dashboard.render.com/).

---

## Step 1: Upload to GitHub
(If you haven't already)
1.  Go to [GitHub.com](https://github.com/new) and create a new repository name `study-time`.
2.  Open your terminal in the project folder and run:
    ```bash
    git init
    git add .
    git commit -m "Ready for deployment"
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/study-time.git
    git push -u origin main
    ```

---

## Step 2: Create Web Service on Render
1.  Go to your [Render Dashboard](https://dashboard.render.com/).
2.  Click **New +** and select **Web Service**.
3.  Connect your GitHub account and select your `study-time` repository.
4.  **Configure the service**:
    *   **Name**: `study-time` (or whatever you want)
    *   **Region**: Frankfurt (or closest to you)
    *   **Branch**: `main`
    *   **Root Directory**: (Leave blank)
    *   **Runtime**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt && python manage.py migrate`
    *   **Start Command**: `gunicorn config.wsgi`
    *   **Instance Type**: Free

5.  **Environment Variables** (Scroll down to "Advanced"):
    Click **Add Environment Variable** for each of these:
    *   `PYTHON_VERSION`: `3.12.8`
    *   `SECRET_KEY`: (Generate a random string, e.g., using `openssl rand -base64 32` or just mash your keyboard)
    *   `DEBUG`: `False`
    *   `What about Database?`: For the free tier, Render wipes the local database periodically. For a persistent database, you need to create a "PostgreSQL" service on Render (also free tier available) and paste the `DATABASE_URL` here.
        *   *For now, you can skip `DATABASE_URL` to just test if it runs, but data will be lost on restart.*
        *   *To fix data loss:* Create a **New > PostgreSQL**, copy the `Internal Database URL`, and add a `DATABASE_URL` variable in your Web Service.

6.  Click **Create Web Service**.

---

## Step 3: Update Google Login (Critical!)
Once your site is live, it will have a URL like `https://study-time.onrender.com`.

1.  Go back to **Google Cloud Console**.
2.  Edit your **Credentials**.
3.  Add your new **Authorized Redirect URIs**:
    *   `https://YOUR-APP-NAME.onrender.com/accounts/google/login/callback/`
4.  Save.
5.  Go to your deployed site's **Admin Panel** (`/admin`).
6.  Go to **Sites** and edit `example.com` to be your new domain (`study-time.onrender.com`).
7.  Go to **Social Applications** and make sure your Google app is connected to this site.

---

## Troubleshooting
*   **Server Error (500)**: Check the "Logs" tab in Render to see what went wrong.
*   **Google Error**: It's usually the Redirect URI mismatch. Check Step 3.
