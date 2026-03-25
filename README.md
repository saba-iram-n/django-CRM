# django-CRM

## Deployment

After the app is installed and environment variables are configured (database, `SECRET_KEY`, `ALLOWED_HOSTS`, etc.), run these from the project root (the directory that contains `manage.py`):

1. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```

   Creates or updates tables to match the current Django models.

2. **Collect static files for production**

   ```bash
   python manage.py collectstatic --noinput
   ```

   Gathers static assets into `STATIC_ROOT` (used with WhiteNoise or your reverse proxy). The `--noinput` flag skips confirmation prompts, which suits automated deploys (e.g. Render build or release commands).

Run both whenever you deploy a new version or after pulling migrations or static-asset changes.