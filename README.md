# CodeAlpha_Evix — Local development

Quick notes to run the project locally for development and tests.

Prereqs
- Python 3.8+
- Create a virtualenv and install requirements:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run migrations and server:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Run tests:

```powershell
python manage.py test
```

Environment
- Use `DATABASE_URL` env var for Postgres in production (e.g. `postgres://user:pass@host:5432/dbname`).
- Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and `DJANGO_ALLOWED_HOSTS` in production.
