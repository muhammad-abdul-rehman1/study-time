# How to Deploy "Study Time" to Railway

This guide will show you how to put your website online so your friends can use it.

## Prerequisites
1.  **GitHub Account**: You need to upload your code to GitHub first.
2.  **Railway Account**: Sign up at [railway.app](https://railway.app/).

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

## Step 2: Deploy on Railway
1.  Go to [Railway Dashboard](https://railway.app/).
2.  Click **New Project** > **Deploy from GitHub repo**.
3.  Select your `study-time` repository.
4.  Railway will start building.
5.  Go to the **Variables** tab for your new service and add:
    *   `PYTHON_VERSION`: `3.12.8`
    *   `SECRET_KEY`: `XYZ` (or any random text)
    *   `DEBUG`: `False`
6.  Go to **Settings** > **Networking** to generate a Domain (e.g., `study-time-production.up.railway.app`).

---

## Step 3: Add a Database (Important!)
If you don't do this, your users will be deleted every time the server restarts.

1.  In the Railway Project verification (the big map view), click **New** (or right-click blank space).
2.  Select **Database** > **PostgreSQL**.
3.  Wait for it to initialize.
4.  **That's it!** Railway automatically connects it to your app.

---

## Step 4: Update Google Login (Critical!)
**This is why you are seeing "Error 400: redirect_uri_mismatch".**

1.  Copy your new Railway Domain (e.g., `https://study-time-production.up.railway.app`).
2.  Go back to **Google Cloud Console**.
3.  Edit your **Credentials**.
4.  Add your new **Authorized Redirect URIs**:
    *   `https://YOUR-RAILWAY-DOMAIN.up.railway.app/accounts/google/login/callback/`
5.  **Save**.

**Wait 1 minute, and try again on the live site.**
