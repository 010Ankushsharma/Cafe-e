# Render Deployment Guide - Cafe-e

## ✅ Files Ready for Deployment

Your project is now configured with:
- `wsgi.py` - Clean WSGI entry point for gunicorn
- `render.yaml` - Render blueprint configuration
- `requirements-prod.txt` - Production dependencies
- `.gitignore` - Excludes instance/ and database files

## 🚀 Step-by-Step Deployment

### 1. Push Changes to GitHub

```bash
git add wsgi.py render.yaml
git commit -m "Add WSGI entry point and fix Render deployment configuration"
git push origin master
```

### 2. Create Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect repository: `010Ankushsharma/Cafe-e`
4. Select branch: `master`

### 3. Configure Service (if not using render.yaml auto-detect)

**Name**: `cafe-order-manager`  
**Region**: Choose closest to users  
**Runtime**: `Python`  
**Build Command**: `pip install -r requirements-prod.txt`  
**Start Command**: `gunicorn 'wsgi:application'`  

### 4. Add Environment Variables

In Render dashboard → **Environment**, add:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | Click "Generate" |
| `PYTHON_VERSION` | `3.14.3` |

### 5. Create PostgreSQL Database

1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `cafe-db`
   - **Database Name**: `cafe_db`
   - **User**: `cafe_user`
   - **Region**: Same as web service
3. Click **"Create Database"**

### 6. Link Database to Web Service

1. Go to your web service settings
2. Scroll to **"Databases"** section
3. Click **"Add Database"**
4. Select `cafe-db`
5. Render automatically sets `DATABASE_URL` ✅

### 7. Deploy

1. Click **"Save Changes"**
2. Monitor build in **Logs** tab
3. Wait for status: **"Live"** 🎉

Your app URL will be: `https://cafe-order-manager.onrender.com`

---

## 🔧 Troubleshooting

### Module Import Errors
If you see `ModuleNotFoundError`:
- Verify `wsgi.py` exists in root directory
- Check start command is: `gunicorn 'wsgi:application'`

### Database Migration Errors
If tables aren't created:
1. Open **Shell** in Render dashboard
2. Run: `flask db upgrade`
3. Optional: `flask seed-db`

### App Crashes on Startup
Check logs for:
- Missing environment variables
- Database connection issues
- Port binding errors (should use PORT env var)

### 502 Bad Gateway
- App might be starting slowly (free tier spins down)
- Check logs for startup errors
- Wait 2-3 minutes after deployment

---

## 📊 Project Structure

```
Cafe-e/
├── wsgi.py              # ← WSGI entry point (NEW!)
├── render.yaml          # ← Render config
├── requirements-prod.txt
├── app.py               # Main app wrapper
├── app/                 # Application package
│   ├── __init__.py      # Flask factory
│   ├── models.py
│   ├── routes/
│   ├── static/
│   └── templates/
└── migrations/          # Database migrations
```

---

## 🎯 What Changed

1. **Created `wsgi.py`**: Clean entry point that avoids import confusion
2. **Updated `render.yaml`**: Changed start command to `gunicorn 'wsgi:application'`
3. **Kept existing structure**: No breaking changes to app code

---

## 📝 Post-Deployment Checklist

- [ ] Homepage loads successfully
- [ ] Menu page displays items
- [ ] Orders can be created
- [ ] Database migrations ran (`flask db upgrade`)
- [ ] Static files (CSS/JS) load correctly
- [ ] No errors in Render logs

---

**Ready to deploy!** Push the changes and follow the steps above. 🚀
