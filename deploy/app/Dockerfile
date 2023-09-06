FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /src

COPY ./deploy/app/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./deploy/app/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./app ./app