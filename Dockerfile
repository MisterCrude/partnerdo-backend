FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install pipenv

RUN mkdir /code/
WORKDIR /code/

# TODO: remove --dev for production 
# --dev — Install both develop and default packages from Pipfile
# --system — Use the system pip command rather than the one from your virtualenv
COPY Pipfile* /code/
RUN pipenv install --system --dev

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