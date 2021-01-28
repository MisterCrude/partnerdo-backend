# Development

In local environment application works inside 3 separate docker containers. For Django app, for redis and for postgres. Postgres and Django have persist data by volume

In docker container no need to run pipenv shell because local inveromet is OS creted in container. All dependencies installed directly here.

Pipenv only needed for linked to VSC workspece

## Setup


### 1. Create pipenv for VSC interpreter (optional step)

- `$ pipenv shell`
- `$ pipenv install`
- `cmd` + `p` and type `> python: Select interpreter`
- select interpreter enerated by pipenv

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
