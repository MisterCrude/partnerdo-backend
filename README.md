### Install

- `$ python3 -m venv .env`
- `$ source .env/bin/actiate`
- `$ deactivate`

### Setup

- `$ pip install -r requirements.txt`
- `$ django-admin startproject <project_name>`
- `$ python manage.py startapp <app_name>`
- `$ pip freeze > requirements.txt`
- `cmd + p` and type `>select enterpreter`, then find `.env/bin/python`

### Manage project

- `$ python manage.py makemigrations [<app_name>]`
- `$ python manage.py migrate [<app_name>]`
- `$ python manage.py createsuperuser`
- `$ python manage.py shell`
- `$ export PYTHONDONTWRITEBYTECODE=1`

### Run project

- `$ python manage.py runserver`

### DB Seed

- `$ python manage.py seed <app_name> [--number=<nubber_of_seeds>]`

### Used tools

- [Django REST framework](https://www.django-rest-framework.org/)
- [django REST framework simplejwt.](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html)
- [Django rest multiple models](https://django-rest-multiple-models.readthedocs.io/en/latest/)

### Cookbooks

- [Django REST framework](https://books.agiliq.com/projects/django-api-polls-tutorial/en/latest/)
- [Django Admin](https://books.agiliq.com/projects/django-admin-cookbook/en/latest/)
- [ORM](https://books.agiliq.com/projects/django-orm-cookbook/en/)
- [Django](https://books.agiliq.com/projects/django-orm-cookbook/en/)

### Projects example

- [E-commerce](https://github.com/justdjango/django-react-ecommerce)
- [Recipe app API](https://github.com/LondonAppDeveloper/recipe-app-api)
- [Django design patterns](https://github.com/PacktPublishing/Django-Design-Patterns-and-Best-Practices-Second-Edition)

### Links

- [Murr project example](https://gitlab.com/Murrengan/murr)
- [Docker + Django + React + PostgreSQL](https://www.youtube.com/watch?v=hwHRI59iGlw&ab_channel=DjangoConUS)
