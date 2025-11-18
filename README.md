# KidAptitude — Backend Prototype

This repository contains a minimal Django REST backend scaffold for the KidAptitude project.

Features included in this scaffold:
- Django + Django REST Framework API
- JWT auth (SimpleJWT) and registration endpoint
- `users` app with `ParentProfile` and `ChildProfile`
- `assessments` app with `Assessment`, `Section`, `Question`, `Result`, and basic `Response`
- API endpoints to start a session, submit answers, complete a session (naive scoring) and fetch results
- Basic pytest test, Dockerfile and `docker-compose.yml` for local development

Quick start (development):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Run tests:

```powershell
pytest -q
```

Notes:
- This is a minimal, opinionated scaffold to implement the brief's backend. It uses SQLite by default for convenience; switch to Postgres in `kidapt/settings.py` for production readiness.
- The scoring engine is intentionally simple and pluggable — extend `assessments` app's `ScoringRule` and `complete_assessment` view to support T-scores, percentiles, or IRT.
