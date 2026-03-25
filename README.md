# django-CRM

A Django CRM-style app for managing customer records with authentication (register, login, CRUD).

## Stack

- **Django 5.1** — web framework  
- **PostgreSQL** in production (via env vars); **SQLite** for local dev when DB vars are omitted  
- **WhiteNoise** — static files in production  
- **Gunicorn** — WSGI server (e.g. Render)  
- **python-dotenv** — optional `.env` for local settings  

## Local setup

From the project root (folder that contains `manage.py`):

1. **Create and activate a virtual environment** (recommended)

   ```bash
   python -m venv .venv
   ```

   Windows (PowerShell):

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   On **Python 3.14**, some packages (for example `psycopg2-binary`, `numpy`) may not install from wheels yet. Use **Python 3.12 or 3.11** for a smooth full install, or install only what you need for local runs (Django, `python-dotenv`, `whitenoise`, `pymysql`, etc.).

3. **Environment file**

   Copy `.env.example` to `.env` and fill in values. At minimum set **`SECRET_KEY`**. For local debugging, set **`DEBUG=True`** in `.env` (this project reads `DEBUG` only from `.env`, not from the shell).

4. **Database**

   ```bash
   python manage.py migrate
   ```

5. **Run the development server**

   ```bash
   python manage.py runserver
   ```

   Open **http://127.0.0.1:8000/** in your browser. Create an account via **Register**, or use **`python manage.py createsuperuser`** for admin access at **`/admin/`**.

## Deployment

After the app is installed and environment variables are configured (database, `SECRET_KEY`, `ALLOWED_HOSTS`, etc.), run these from the project root:

1. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```

2. **Collect static files for production**

   ```bash
   python manage.py collectstatic --noinput
   ```

   Static files are collected into `STATIC_ROOT` (used with WhiteNoise). `--noinput` avoids prompts and fits automated deploys (e.g. Render).

Run both whenever you deploy a new version or after pulling migrations or static-asset changes.

On **Render** (or similar), set the **start command** to run Gunicorn (see `Procfile`), bind to **`$PORT`**, and configure environment variables to match production (PostgreSQL, `SECRET_KEY`, etc.). See `dcrm/settings.py` and `.env.example` for variable names.

## Configuration reference

- **`.env.example`** — documents supported environment variables and local `.env` usage.  
- **`Procfile`** — example `web` process for Gunicorn.  
- **`.gitignore`** — do not commit `.env`, `db.sqlite3`, `.venv/`, or `staticfiles/`.
