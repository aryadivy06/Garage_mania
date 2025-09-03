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


✨ Features


👤 For Users
✅ Register & login securely.
✅ Add and manage their vehicles (Bike, Car, Scooter, etc.).
✅ Book services (Car Wash, AC Repair, Suspension, etc.) at registered garages.
✅ Get email notifications when booking is confirmed or status is updated.
✅ View booking history with status (Pending, In Progress, Completed, Cancelled).

🛠️ For Service Providers (Garages)
🏢 Register garage with details (name, phone, services offered, etc.).
📋 View all service requests in a Garage Dashboard.
🔄 Update service status (Pending → In Progress → Completed/Cancelled).
📊 Track monthly statistics (Completed services, Pending requests, Unique customers).
📧 Receive email notifications when a new booking is made.

🛠️ Tech Stack
Backend: Django 5.x (Python 3.11)
Frontend: HTML5, CSS3, JavaScript (Vanilla + Django Templates)
Database: SQLite (development)

Email Service: Django’s built-in email backend (configured with SMTP, e.g., Gmail)
Version Control: Git + GitHub
Deployment Ready: WSGI (can be deployed on PythonAnywhere, Heroku, etc.)

📧 Email Notifications
We have configured Django’s EmailMessage to send notifications:
✉️ To service providers → when a user books a service.
✉️ To users → when the garage updates the booking status.



📌 SMTP is used (e.g., Gmail). Credentials are stored in settings.py:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'


How It Works

User Signup/Login
Users register with details & add vehicles.

Garage Signup
Garages register with business info and available services.

Book Service
User selects garage → selects service → chooses vehicle → confirms booking.

Notifications
Garage receives email when a new service is booked.
User gets an email when garage updates the status.

Garage Dashboard
Shows service requests (Pending/In Progress).
Allows updating status.
Displays service history and monthly statistics.



Project Structure

Garage_mania/
│── Garage_Mania/          # Virtual Environment
│── Online_garage/         # Django Project
│   ├── settings.py        # Project settings
│   ├── urls.py            # URL mappings
│   ├── wsgi.py / asgi.py  # For deployment
│
│── Garage/                # Main App
│   ├── models.py          # User, Vehicle, Garage, Booking models
│   ├── views.py           # Business logic
│   ├── templates/         # HTML templates
│   ├── static/            # CSS, JS, Images
│
│── db.sqlite3             # Default DB
│── manage.py              # Django CLI
│── requirements.txt       # Dependencies
│── README.md              # Documentation
│── .gitignore             # Git ignore file
