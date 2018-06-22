FROM node:8 as builder
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN set -e \
    && yarn \
    && yarn build \
    && rm node_modules -r

FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY --from=builder /code/ .

RUN set -e \
    && apk add --no-cache postgresql-dev build-base jpeg-dev git zlib-dev \
    && pip install --no-cache -r requirements/prod.txt \
    && apk del build-base \
    && python manage.py collectstatic
