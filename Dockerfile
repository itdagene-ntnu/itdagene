FROM node:13 as builder
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN set -e \
    && yarn \
    && yarn build \
    && rm node_modules -r

FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY --from=builder /code/ .

RUN set -e \
    && echo 'SECRET_KEY="secret"' > itdagene/settings/local.py \
    && apk add --no-cache postgresql-dev build-base jpeg-dev git zlib-dev libffi-dev \
    && pip install --no-cache -r requirements/prod.txt \
    && apk del build-base \
    && python manage.py collectstatic \
    && rm itdagene/settings/local.py
