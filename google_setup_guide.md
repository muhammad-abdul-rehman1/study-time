# How to Get Google OAuth Keys

To enable "Login with Google", you need to get a **Client ID** and **secret Key** from Google.

## Step 1: Create a Project
1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Click the project dropdown (top left) and select **"New Project"**.
3.  Name it `Study Time` and click **Create**.
4.  Select the project you just created.

## Step 2: Configure Consent Screen
1.  In the left sidebar, go to **APIs & Services > OAuth consent screen**.
2.  Select **External** user type and click **Create**.
3.  **App Information**:
    *   App name: `Study Time`
    *   User support email: (Your email)
    *   Developer contact information: (Your email)
4.  Click **Save and Continue** until you finish (you can skip scopes for now).

## Step 3: Create Credentials
1.  Go to **APIs & Services > Credentials**.
2.  Click **+ CREATE CREDENTIALS** (top) > **OAuth client ID**.
3.  **Application type**: Select **Web application**.
4.  **Name**: `Study Time Local`.
5.  **Authorized JavaScript origins**:
    *   Click **ADD URI**: `http://127.0.0.1:8000`
    *   Click **ADD URI**: `http://localhost:8000`
    *   *(If you use port 8001, add `http://127.0.0.1:8001` as well)*
6.  **Authorized redirect URIs**:
    *   Click **ADD URI**: `http://127.0.0.1:8000/accounts/google/login/callback/`
    *   Click **ADD URI**: `http://localhost:8000/accounts/google/login/callback/`
    *   *(If you use port 8001, change 8000 to 8001 in these links)*
7.  Click **Create**.

## Step 4: Add Keys to Django
1.  Copy the **Client ID** and **Client Secret** shown.
2.  Start your Django server: `run.bat` (or `python manage.py runserver`).
3.  Go to the Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).
4.  Login with your superuser account.
5.  Go to **Social Accounts > Social applications**.
6.  Click **Add social application**.
    *   **Provider**: Google
    *   **Name**: Study Time
    *   **Client id**: (Paste the ID)
    *   **Secret key**: (Paste the Secret)
    *   **Sites**: Move `example.com` from "Available" to "Chosen".
7.  Click **Save**.

**Done!** Now you can click "Login with Google" on the login page.
