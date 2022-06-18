FROM python:3.10.0a1-alpine3.12
COPY requirements.txt /app/requirements.txt

RUN set -ex \
    && pip install --upgrade pip \
    && pip install -r /app/requirements.txt

WORKDIR /app

ADD . .

EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "mypersonalplanner.wsgi:application"]