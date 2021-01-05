# Manage
start:
	python manage.py migrate
	python manage.py createsuperuser
	python manage.py runserver

run:
	python manage.py runserver 0.0.0.0:8000

activate:
	pipenv shell

seed:
	python manage.py seed ${app} --number=100


# Tools
MIGRATIONS_DIR:=migrations
CACHE_DIR:=__pycache__
COMPOSE = docker-compose -f docker-compose.yml

rmmigrations:
	find . -type d -name "${MIGRATIONS_DIR}" -exec rm -rf {} +

clean:
	find . -type d -name "${CACHE_DIR}" -exec rm -rf {} +

reset:
	find . -type d -name "${MIGRATIONS_DIR}" -exec rm -rf {} +
	find . -type d -name "${CACHE_DIR}" -exec rm -rf {} +
	rm -R "db.sqlite3"
	touch "db.sqlite3"
	python manage.py migrate
	python manage.py createsuperuser
	python manage.py runserver

up: 
	${COMPOSE} up

login: 
	docker exec -it partnerdo-backend_web_1 bash