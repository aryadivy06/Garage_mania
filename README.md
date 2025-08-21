# Garage_mania

1. To create virtual environment in folder we using:
   python -m venv folder_name
2. To activate virtual environment:
   folder_name\Scripts\activate
3. To deactivate the virtual environment:
   deactivate
4. For installing Django in our virtual environment we use:
   pip install django
5. To start project in virtual environment:
   django-admin startproject project_name

These command will create a new django project in current directory
Resulting Structure:
python program/
│
├── Garage_Mania/         ← Virtual Environment
│   ├── Include/
│   ├── Lib/
│   ├── Scripts/
│   └── pyvenv.cfg
│
├── Online_garage/        ← Django Project folder
│   ├── __init__.py     // Makes a folder a python package
│   ├── settings.py     // This is for configuration file for your project controls settings like Installed apps, Middleware Databases.
│   ├── urls.py        // Controls which URL go to which views
│   ├── wsgi.py        // Stands for Web Server Gateway Interface used to deploy your django app on production server
│   └── asgi.py        // Similar to wsgi.py but for asynchronous support.
│
├── db.sqlite3            ← Django Database file
├── manage.py             ← Django entry point

       
6. After creating the project run:
   cd my_aps
   python manage.py runsever
   Then open http://127.0.0.1:8000 to check you connection is correct or not

7. App creation:
   python manage.py startapp Garage
   when we run manage.py with startapp then it will create a new folder with the name given and the resultant
   directory look like:
    myapp/
│── __init__.py
│── admin.py      # Register models for Django admin
│── apps.py       # App configuration
│── models.py     # Database tables (classes)
│── tests.py      # Unit tests
│── views.py      # Logic for handling requests
│── migrations/   # Database migration files



 
8. After running the startapp command you have to add the Garage app into Installed Apps.

  INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'garage_app',
]

9. There are two more folders which we create for our app
   I.  templates : This is for HTML files.
   II. static    : This is for static files like css, javascript , images.

   The final directory look like:
    python program/
│
├── Garage_Mania/         ← Virtual Environment
│   ├── Include/
│   ├── Lib/
│   ├── Scripts/
│   └── pyvenv.cfg
│
├── Online_garage/        ← Django Project folder
│   ├── __init__.py    
│   ├── settings.py     
│   ├── urls.py        
│   ├── wsgi.py        
│   └── asgi.py        
│──Garage/
|   │── __init__.py
|   │── templates
|   │── static    
|   │── admin.py      
|   │── apps.py      
|   │── models.py    
|   │── tests.py     
|   │── views.py      
|   │── migrations/
├── db.sqlite3            ← Django Database file
├── manage.py             ← Django entry point


