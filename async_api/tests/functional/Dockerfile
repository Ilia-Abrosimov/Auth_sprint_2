FROM python:3.9

RUN mkdir -p /app/tests/functional
WORKDIR /app/tests/functional
COPY requirements.txt /app

RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY . .

WORKDIR /app
RUN touch ./tests/__init__.py
RUN touch ./tests/functional/__init__.py
