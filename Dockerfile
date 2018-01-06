FROM node:8 as builder
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN echo '{ "allow_root": true }' > /root/.bowerrc # Shitty bower
RUN set -e \
    && npm install -g bower \
    && bower --allow-root install \
    && npm install \
    && make

FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY --from=builder /code/ .

RUN set -e \
    && apk add --no-cache postgresql-dev build-base jpeg-dev git \
    && pip install --no-cache -r requirements/prod.txt \
    && python manage.py collectstatic


