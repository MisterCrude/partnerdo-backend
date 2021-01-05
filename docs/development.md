# Development

In local environment application works inside 3 separate docker containers. For Django app, for redis and for postgres. Postgres and Django have persist data by volume

## First run

### 1. Create pipenv for VSC interpreter (optional step)

- `$ pipenv shell`
- `$ pipenv install`
- `cmd` + `p` and type `> python: Select interpreter`
- select interpreter enerated by pipenv

### 2. Build containers and run

- `$ make up`
- `$ docker-compose down -v` stop containers and remove volume for db
- `$ make up`
- `$ make login`
- `$ make start`
- `$ make run`

## Run

- `$ make up`
- `$ make login`
- `$ make run`
