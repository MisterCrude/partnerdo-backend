# Backend-end _partnerdo.pl_

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
- `$ python manage.py syncdb`
- `$ export PYTHONDONTWRITEBYTECODE=1`

### Run project

- `$ python manage.py runserver`

### DB Seed

- `$ python manage.py seed <app_name> [--number=<nuber_of_seeds>]`

### Documentation

- [Tools](docs/tools.md)
- [Application architecture](docs/application.md)
- [Development](docs/development.md)
- [Deployment](docs/deployment.md)
- [Testing](docs/testing.md)
