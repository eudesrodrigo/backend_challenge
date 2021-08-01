FROM ubuntu:20.04
RUN add-apt-repository universe & apt-get update && apt-get -y install libpq-dev gcc python3-pip && pip3 install psycopg2
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . /api/
# FROM python:3.9.5-slim-buster AS app

EXPOSE 8000

ARG DEBUG="false"
ENV DEBUG="${DEBUG}" \
    PYTHONUNBUFFERED="true" \
    PYTHONPATH="." \
    PATH="${PATH}:/home/python/.local/bin" 

# ADD requirements.txt .
# RUN python -m pip install -r requirements.txt