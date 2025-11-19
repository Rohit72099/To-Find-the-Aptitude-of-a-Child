# KidAptitude - Deployment Guide for Render

## Quick Deploy to Render

### 1. **Prerequisites**
- GitHub account with your repo pushed
- Render account (https://render.com)
- PostgreSQL database (optional but recommended)

### 2. **Setup on Render Dashboard**

#### Step A: Create a Web Service
1. Go to **Render Dashboard** → Click **New +** → Select **Web Service**
2. Connect your GitHub repo (`Rohit72099/To-Find-the-Aptitude-of-a-Child`)
3. Fill in:
   - **Name**: `kidapt-app` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn kidapt.wsgi:application`
   - **Plan**: Free (or Starter)
4. Click **Create Web Service**

#### Step B: Set Environment Variables
In the **Environment** section, add these variables:

```
DEBUG=False
SECRET_KEY=<generate-a-strong-key-using-python-secrets>
ALLOWED_HOSTS=your-app.onrender.com,yourdomain.com
```

To generate a strong SECRET_KEY in Python:
```python
import secrets
print(secrets.token_urlsafe(50))
```

#### Step C: Attach PostgreSQL (Recommended)
1. In Render Dashboard, go to **Databases** → **New +** → **PostgreSQL**
2. Choose a name and plan (Free tier available)
3. Create the database
4. Render will automatically set `DATABASE_URL` environment variable

Your app will now use PostgreSQL automatically (local dev still uses SQLite).

### 3. **Deploy**
- After setting env vars, click **Deploy** (or push a new commit to GitHub for auto-deploy)
- Watch the build logs → confirm "Build successful 🎉"
- Visit your app URL: `https://your-app.onrender.com`

### 4. **Post-Deploy Setup**
Once deployed, run migrations and create a superuser:

```bash
# SSH into Render (via dashboard) or use Render Shell:
python manage.py migrate
python manage.py createsuperuser
```

Or add to your `Procfile` to auto-run on deploy:
```
release: python manage.py migrate
web: gunicorn kidapt.wsgi:application
```

### 5. **Access Your App**
- Main site: `https://your-app.onrender.com`
- Admin: `https://your-app.onrender.com/admin/` (use your superuser credentials)
- API: `https://your-app.onrender.com/api/`

## Troubleshooting

**Error: `gunicorn: command not found`**
- Ensure `gunicorn>=20.1.0` is in `requirements.txt` ✓

**Error: `ModuleNotFoundError: No module named 'dj_database_url'`**
- Ensure `dj-database-url>=3.0` is in `requirements.txt` ✓

**Static files not loading**
- WhiteNoise is configured (see `kidapt/settings.py`)
- Run: `python manage.py collectstatic --noinput` locally to test

**Database issues**
- Set `DATABASE_URL` environment variable on Render
- App auto-switches from SQLite → PostgreSQL if `DATABASE_URL` is set ✓

**Debug mode showing errors**
- Ensure `DEBUG=False` on Render (production)
- Check logs in Render dashboard for detailed errors

## Local Development

To test locally before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Copy .env.example to .env and set DEBUG=True, SECRET_KEY, etc.
cp .env.example .env

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start dev server
python manage.py runserver
```

## Useful Links
- Render Docs: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/5.2/howto/deployment/
