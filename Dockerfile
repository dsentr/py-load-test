FROM python:3.6.5

RUN apt-get update && apt-get install stress
RUN mkdir -p /usr/var/app
COPY main.py /usr/var/app
COPY requirements.txt /usr/var/app

RUN pip3 install -r /usr/var/app/requirements.txt

WORKDIR /usr/var/app

CMD gunicorn --bind 0.0.0.0:80 main:app

