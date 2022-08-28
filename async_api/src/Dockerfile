FROM python:3.9
RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src

RUN pip3 install --upgrade pip
RUN pip3 install -r /src/requirements.txt --no-cache-dir
RUN apt-get update && apt-get install -y netcat
COPY . .
CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:9000"]