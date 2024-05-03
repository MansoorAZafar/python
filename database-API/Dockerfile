FROM python:3.11-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y pkg-config
RUN pip3 install -r requirements.txt

COPY . .
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]