FROM python:3.11-bullseye

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --upgrade pip setuptools gunicorn

RUN pip install -r requirements.txt

COPY . .
