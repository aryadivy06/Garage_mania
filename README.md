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
   project_name
   |-manage.py
   |-project_name
       |- __init__.py
       |- setting.py
       |- urls.py
       |- wsgi.py
       
6. After creating the project run:
   cd my_aps
   python manage.py runsever
   Then open http://127.0.0.1:8000 to check you connection is correct or not
   
