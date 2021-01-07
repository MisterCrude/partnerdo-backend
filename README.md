# Backend-end _partnerdo.pl_

### Install

#### _For virtualenv_

- `$ python3 -m venv .env`
- `$ pip install -r requirements.txt`
- `$ pip freeze > requirements.txt`
- `$ source .env/bin/actiate`
- `$ deactivate`

#### _For pipenv (in using)_

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

### Setup

- `$ django-admin startproject <project_name>`
- `$ python manage.py startapp <app_name>`
- `cmd + p` and type `>select interpreter`, then find `.env/bin/python`
- `$ python manage.py makemigrations [<app_name>]`
- `$ python manage.py migrate`

### Manage project

- `$ python manage.py makemigrations [<app_name>]`
- `$ python manage.py migrate [<app_name>]`
- `$ python manage.py createsuperuser`
- `$ python manage.py shell`
- `$ export PYTHONDONTWRITEBYTECODE=1`

### Run project

#### _Without docker_

- `$ make run`

#### _With docker_

- `$ make up`
- `$ make login`
- `$ make run` (no need to activate pipenv because docker plays role of scoped environment)

### Deployment

- `$ python manage.py check --deploy`

### DB Seed

- `$ python manage.py seed <app_name> [--number=<nuber_of_seeds>]`

### Documentation

- [Tools](docs/tools.md)
- [Application architecture](docs/application.md)
- [Development](docs/development.md)
- [Deployment](docs/deployment.md)
- [Testing](docs/testing.md)
