# itDAGENE [![CircleCI](https://circleci.com/gh/itdagene-ntnu/itdagene.svg?style=svg&circle-token=abcfbea6689e5baef8a1fbb7fa6eb822efdd5bfb)](https://circleci.com/gh/itdagene-ntnu/itdagene)

> Codebase for http://www.itdagene.no

![itDAGENE](itdagene/assets/img/logoQuiz.png)


## TL;DR
- Runs python3.6 with Django
- Postgres as main database
- Celery (with redis-broker) for async tasks
- CircleCI for continuous integration
- yarn and webpack for javascript

## Setup

First make sure that you have the following software installed on your system:

- Python 3.6
- Node.js and yarn
- [docker] together with [docker-compose]

Setup python environment
```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements/base.txt
$ echo "from itdagene.settings.dev import *" > itdagene/settings/local.py 
$ docker-compose up -d # This starts the databse & redis
```

Install other dependencies:

```bash
$ yarn
$ yarn build
```

## Starting the app

```bash
$ docker-compose up -d
$ source venv/bin/activate
$ python manage.py runserver
```

## Migrations

In order to setup a new dev environment you have to create a superuser. Every time there are new migrations, you have to apply them. If you don't, the `runserver` command will give you a warning.

```bash
$ python manage.py migrate
$ python manage.py createsuperuser
```

#### Model changes

Have you changed a model? Then you have to make and apply migrations. Migrations should always be committed to the repo in the same commit/PR as the model change.

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

## Testing
In order to execute the tests, you have to install `tox`. The tests are always run in the continuous integration server, and no code that doesn't pass all the tests (including linting) should not be merged into the master branch.

```bash
$ pip install tox
$ tox
```

### Code style
We enforce the style guide [PEP 8] with flake8, and [isort] for import sorting. (Soon yapf for formatting). All 

```bash
$ isort -rc itdagene # Fix isort errors
$ tox -e isort       # Verify the result with tox
$ tox -e flake8      # Verify PEP 8 style
```

## Celery

```bash
$ celery worker -A itdagene # worker
$ celery beat -A itdagene   # beat
$ celery flower -A itdagene --address="127.0.0.1" --port=5555 # flower
```

## Misc

### Nice reads

- [Terminal intro](https://www.digitalocean.com/community/tutorials/an-introduction-to-the-linux-terminal)
- [Django intro](https://www.djangoproject.com/start/)
- [Intro to celery](http://docs.celeryproject.org/en/latest/getting-started/introduction.html)
- [Why docker](https://www.docker.com/what-container)

### Deps

You **may** have to install these
```bash
$ sudo apt-get install libpq-dev python-dev redis-server zlib1g-dev libjpeg-dev python-pip postgresql postgresql-contrib
$ sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/
$ sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
$ sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/
```


[docker]: https://www.docker.com/community-edition
[docker-compose]: https://docs.docker.com/compose/overview/
[PEP 8]: https://www.python.org/dev/peps/pep-0008/
[isort]: https://github.com/timothycrosley/isort
