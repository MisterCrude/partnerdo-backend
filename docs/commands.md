# Useful commands

## Create app

### Virtualenv

- `$ python3 -m venv .env`
- `$ pip install -r requirements.txt`
- `$ pip freeze > requirements.txt`
- `$ source .env/bin/actiate`
- `$ deactivate`

### Pipenv

- `pipenv install`
- `pipenv shell`
- `pipenv lock`
- `pipenv install <package-name>`
- `pipenv install <package-name> --dev`
- `pipenv uninstall <package-name>`
- `pipenv uninstall --all`
- `pipenv --where`
- `pipenv --venv`
- `exit`

## Django setup

- `$ django-admin startproject <project_name>`
- `$ django-admin startproject <project_name> .` in current dir
- `$ python manage.py startapp <app_name>`
- `cmd + p` and type `>select interpreter`, then find `.env/bin/python`
- `$ python manage.py makemigrations [<app_name>]`
- `$ python manage.py migrate`

### Manage app

- `$ python manage.py makemigrations [<app_name>]`
- `$ python manage.py migrate [<app_name>]`
- `$ python manage.py createsuperuser`
- `$ python manage.py shell`
- `$ export PYTHONDONTWRITEBYTECODE=1`
- `$ docker system prune -a`

### Django extentions

- `$ python manage.py runserver_plus`
- `$ python manage.py show_urls`
- `$ python manage.py graph_models -a -g -o models_diagram.png` (with Pygraphviz)

### DB Seed

- `$ python manage.py seed <app_name> [--number=<nuber_of_seeds>]`
