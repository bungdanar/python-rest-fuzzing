FROM python:3.11

RUN pip install --upgrade pip

RUN pip install pipenv

WORKDIR /app

COPY Pipfile* .

RUN pipenv install --system --deploy

RUN pip install gunicorn

COPY . .