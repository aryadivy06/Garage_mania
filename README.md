Django Project Setup
1. Create Virtual Environment
python -m venv folder_name

2. Activate Virtual Environment

Windows:

folder_name\Scripts\activate


Linux/Mac:

source folder_name/bin/activate

3. Deactivate Virtual Environment
deactivate

4. Install Django
pip install django

5. Start Django Project
django-admin startproject project_name


This command will create a new Django project in the current directory.

📂 Resulting Structure After Creating Project
python program/
│
├── Garage_Mania/             ← Virtual Environment
│   ├── Include/
│   ├── Lib/
│   ├── Scripts/
│   └── pyvenv.cfg
│
├── Online_garage/            ← Django Project folder
│   ├── __init__.py           # Makes this folder a Python package
│   ├── settings.py           # Configuration file for project (apps, middleware, databases)
│   ├── urls.py               # Controls which URL goes to which view
│   ├── wsgi.py               # Web Server Gateway Interface (for deployment)
│   └── asgi.py               # Asynchronous Server Gateway Interface
│
├── db.sqlite3                ← Django Database file
└── manage.py                 ← Django entry point

6. Run Development Server
cd Online_garage
python manage.py runserver


Then open http://127.0.0.1:8000
 to check the connection.

📂 App Creation

To create an app:

python manage.py startapp Garage


This will create a new folder Garage/ with the following structure:

Garage/
│── __init__.py
│── admin.py         # Register models for Django admin
│── apps.py          # App configuration
│── models.py        # Database tables (classes)
│── tests.py         # Unit tests
│── views.py         # Logic for handling requests
│
└── migrations/      # Database migration files
    └── __init__.py

7. Add App to Installed Apps

Inside settings.py, add your app:

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Garage',   # your app
]

📂 Extra Folders for App

You should also create these folders inside your app:

templates/ → for HTML files

static/ → for static files (CSS, JavaScript, Images)

📂 Final Project Directory
python program/
│
├── Garage_Mania/             ← Virtual Environment
│   ├── Include/
│   ├── Lib/
│   ├── Scripts/
│   └── pyvenv.cfg
│
├── Online_garage/            ← Django Project folder
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── Garage/                   ← App folder
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── templates/
│   │   └── Garage/
│   │       └── home.html
│   └── static/
│       └── Garage/
│           ├── style.css
│           └── script.js
│
├── db.sqlite3                ← Django Database file
└── manage.py                 ← Django entry point
