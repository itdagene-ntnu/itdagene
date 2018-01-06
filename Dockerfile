FROM python:3.6-alpine as builder
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN set -e \
    && python -m venv venv \
    && source venv/bin/activate \
    && apk add --no-cache postgresql-dev build-base jpeg-dev \
    && pip install --no-cache -r requirements/base.txt

FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY --from=builder /code/ .

RUN set -e \
    && source venv/bin/activate \
    && apk add --no-cache jpeg-dev git

