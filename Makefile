# Manage
start:
	python manage.py makemigrations userprofile proposal
	python manage.py migrate
	python manage.py createsuperuser

run:
	python manage.py runserver 0.0.0.0:8000

activate:
	pipenv shell

seed:
	python manage.py seed ${app} --number=100

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

# Tools
MIGRATIONS_DIR:=migrations
CACHE_DIR:=__pycache__
COMPOSE = docker-compose -f docker-compose.yml

rm-migrations:
	find . -type d -name "${MIGRATIONS_DIR}" -exec rm -rf {} +

rm-cache:
	find . -type d -name "${CACHE_DIR}" -exec rm -rf {} +

reset:
	find . -type d -name "${MIGRATIONS_DIR}" -exec rm -rf {} +
	docker stop $$(docker ps -a -q)
	docker rm $$(docker ps -a -q)
	rm -rf db_data
	rm -rf media/*
	docker system prune -a

up: 
	${COMPOSE} up

login: 
	docker exec -it partnerdo-backend_web_1 bash