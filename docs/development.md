# Development

In local environment application works inside 3 separate docker containers. For Django app, for redis and for postgres. Postgres and Django have persist data by volume

In docker container no need to run pipenv shell because OS used as enveroment. All dependencies installed directly here.

.venv creating only for VSC settings propose

## Setup

### 1. Create pipenv for VSC interpreter (optional step)

- `$ pipenv install --dev`
- `$ pipenv shell`
- `$ pipenv run pip install psycopg2-binary`
- `cmd` + `p` and type `> python: Select interpreter`
- select interpreter from .venv by pipenv

### 2. Build containers and run

- `$ make up`
- ? `$ docker-compose down -v` stop containers and remove volume for db
- ? `$ make up`
- `$ make login`
- `$ make setup`
- `$ make run`

## Run

- `$ make up`
- `$ make login`
- `$ make run`
