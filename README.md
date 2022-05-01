# Django Guide

## Django Tips & Tricks

- `pip install django==<version>` - installs specified version of django
- `django-admin --version` - returns the installed version of django
- `django-admin startproject <project name> .` - creates a django folder in the current working directory.
- `python manage.py runserver <port number>` - starts the django app on specified port number
- django application by default runs on port no 8000, `http://localhost:8000`
- `db.sqlite3` file will be created automatically for the first time when we run the `python manage.py runserver` command.
- `return HttpResponse(<response>, status=<code>)` - we can also pass status code along with response to HttpResponse method.
- we can directly specify `templates` folder in `TEMPLATE` list for `DIRS` key as a list, instead of specifying absolute path using os module
- `{% extends "base.html" %}` - extends a html component
- `{% include "footer.html" %}` - includes a html component
- `python manage.py makemigrations` - generates pseudo sqlcode/object under migration folder within app
- `python manage.py sqlmigrate <appname> <filename>` - generates sql code from pseudo code/object
- `python manage.py migrates` - creates a sql tables in db.

## Django Static files

- configure static file using the below code snippet

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR/'static'
STATICFILES_DIRs = [
    'greatkart/static
]
```

- `python manage.py collectstatic` - collects/copies static files to static folder under root directory under admin folder
- `{% static '<path to file>' %}` - to access a static file in django.

## Django Most used import statements

- `from django.http import HttpResponse`

## Extra Tips

- `which python` - returns the location of python in Mac/Linux Systems
- `where python` - returns the location of python in windows Machines

## Self Queries and Doubts

- specifying directly `templates` under DIRS in TEMPLATES list instead of abs path using os.path.join() method
- why admin folder is getting created while using `python manage.py collectstatic` and contents of admin are different from input
