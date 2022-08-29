FROM python:3.10

WORKDIR /opt/etl

COPY preload.sh preload.sh
COPY requirements.txt requirements.txt
COPY ./es/movies.json movies.json
COPY ./es/genres.json genres.json
COPY ./es/persons.json persons.json


RUN  pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY . .
