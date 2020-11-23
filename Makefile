install:
	pipenv install

activate:
	pipenv shell

add:
	pipenv install ${lib}
	pipenv check

addd:
	pipenv install ${lib} --dev
	pipenv check

rm:
	pipenv uninstall ${lib}

rma:
	pipenv uninstall --all

gr:
	pipenv graph 


# Manage

start:
	python manage.py migrate
	python manage.py createsuperuser
	python manage.py runserver

manage:
	python manage.py ${cmd}

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations ${app}

superuser:
	python manage.py createsuperuser

startapp:
	python manage.py startapp ${app}

run:
	python manage.py runserver

seed:
	python manage.py seed ${app} --number=100


# Deploy

check:
	python manage.py check --deploy


# Tools

MIGRATIONS_DIR:=migrations
CACHE_DIR:=__pycache__

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
	

git:
	gaa && gcmsg ${msg}