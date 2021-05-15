FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install pipenv

RUN mkdir /code/
WORKDIR /code/

# TODO: remove --dev for production 
# --dev — Install both develop and default packages from Pipfile
# --system — Install all without environment
COPY Pipfile* /code/
RUN pipenv install --dev --system
# psycopg2-binary installed by pip because pipenv didn't support this package 
RUN pip install psycopg2-binary

ADD . /code/

# Use this for production
#
# FROM python:3
# RUN mkdir /code
# WORKDIR /code
# ADD requirements.txt /code/
# RUN pip install --no-cache-dir -r requirements.txt
# ADD requirements_tests.txt /code/
# RUN pip install --no-cache-dir -r requirements_tests.txt
# ADD . /code/