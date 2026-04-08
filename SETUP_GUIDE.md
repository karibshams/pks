# Karib Shams Portfolio — Setup & Deployment Guide

## PROJECT STRUCTURE
```
karib_portfolio/
├── karib_portfolio/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── portfolio/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   │   └── portfolio/
│   │       └── index.html
│   └── static/
│       ├── css/
│       │   └── main.css
│       ├── js/
│       │   └── main.js
│       └── img/
│           ├── karib.jpg          ← ADD YOUR PHOTO HERE
│           └── avatar_placeholder.svg
├── manage.py
└── requirements.txt
```

---

## STEP 1 — INSTALL DJANGO LOCALLY

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install Django
pip install -r requirements.txt
```

---

## STEP 2 — ADD YOUR PROFILE PHOTO

1. Name your photo file exactly: `karib.jpg`
2. Place it in: `portfolio/static/img/karib.jpg`
3. Recommended: crop to a square (500×500px or larger), face centered

---

## STEP 3 — INITIALIZE DATABASE & RUN LOCALLY

```bash
cd karib_portfolio

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user (optional, to view feedback/chat)
python manage.py createsuperuser

# Collect static files (needed for deployment)
python manage.py collectstatic

# Run the development server
python manage.py runserver
```

Open browser → http://127.0.0.1:8000

Admin panel → http://127.0.0.1:8000/admin

---

## STEP 4 — VS CODE SETUP

1. Open the `karib_portfolio/` folder in VS Code
2. Install Python extension (ms-python.python)
3. Press `Ctrl+Shift+P` → "Python: Select Interpreter" → choose your venv
4. Open terminal: `Ctrl+`` ` and run `python manage.py runserver`
5. Use Live Server extension won't work here — use the Django server directly

---

## STEP 5 — DEPLOY ON PYTHONANYWHERE (Free Tier)

### A. Create Account
1. Go to https://www.pythonanywhere.com → Sign up (free)
2. Choose username — this becomes: `yourusername.pythonanywhere.com`

### B. Upload Files
1. Go to **Files** tab in PythonAnywhere dashboard
2. Create folder: `/home/yourusername/karib_portfolio/`
3. Upload all project files using the file manager
   OR use the Bash console:
   ```bash
   # In PythonAnywhere Bash console:
   git clone https://github.com/YOUR_GITHUB_REPO.git karib_portfolio
   ```

### C. Set Up Virtual Environment
In PythonAnywhere Bash console:
```bash
cd ~
mkvirtualenv --python=python3.10 karib_env
workon karib_env
pip install django
```

### D. Configure Web App
1. Go to **Web** tab → **Add a new web app**
2. Choose: **Manual configuration** → **Python 3.10**
3. Set:
   - **Source code**: `/home/yourusername/karib_portfolio`
   - **Working directory**: `/home/yourusername/karib_portfolio`
   - **Virtualenv**: `/home/yourusername/.virtualenvs/karib_env`

### E. Edit WSGI File
Click the WSGI configuration file link. Replace ALL content with:
```python
import os
import sys

path = '/home/yourusername/karib_portfolio'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'karib_portfolio.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
Replace `yourusername` with your actual PythonAnywhere username.

### F. Static Files
In the **Web** tab → **Static files** section, add:
- URL: `/static/`
- Directory: `/home/yourusername/karib_portfolio/staticfiles`

Then in Bash console:
```bash
cd ~/karib_portfolio
workon karib_env
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
```

### G. Update settings.py for Production
Edit `karib_portfolio/settings.py`:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']
```

### H. Reload & Go Live
1. Click **Reload** in the Web tab
2. Visit: `https://yourusername.pythonanywhere.com`

---

## FEATURES INCLUDED

- ✅ Neural Network animated canvas background
- ✅ Custom glowing cursor
- ✅ Typing effect hero section
- ✅ Animated counter stats
- ✅ Scroll reveal animations
- ✅ AI Quiz mini-game (7 questions)
- ✅ Real-time AI Chat simulation (Django backend)
- ✅ Feedback form with database storage
- ✅ File upload simulation
- ✅ Responsive mobile layout
- ✅ Admin dashboard for feedback & chat logs
- ✅ All CV data: projects, publications, experience, education

---

## ADMIN PANEL
Visit `/admin` to:
- View all submitted feedback
- See all chat messages
- Manage content

---

## CUSTOMIZATION
- Update personal data in `portfolio/views.py` → `PORTFOLIO_DATA` dict
- Add/change colors in `portfolio/static/css/main.css` → `:root` variables
- Add more quiz questions in `portfolio/static/js/main.js` → `quizData` array
- Add AI chat replies in `portfolio/views.py` → `AI_REPLIES` list
