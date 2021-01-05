FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install pipenv

RUN mkdir /code/
WORKDIR /code/

COPY Pipfile* /code/
RUN pipenv install --system

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