# itDAGENE [![CircleCI](https://circleci.com/gh/itdagene-ntnu/itdagene.svg?style=svg&circle-token=abcfbea6689e5baef8a1fbb7fa6eb822efdd5bfb)](https://circleci.com/gh/itdagene-ntnu/itdagene)

![itDAGENE](itdagene/assets/img/logoQuiz.png)

This is the code base for http://www.itdagene.no. It is a standard django project, and uses Celery for async tasks.

## TL;DR
- Runs Django
- Using postgres as the database
- Using Celery (with redis-broker) for async tasks
- CircleCI for continuous integration


## Setup

First make sure that you have the following software installed on your system:

- Python 3.6
- Node.js and yarn
- bower (install globally with yarn/npm)
- [docker] together with [docker-compose]

Setup python environment
```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements/base.txt
$ docker-compose up -d # This starts the databse & redis

```


Install other dependencies:

```bash
$ bower install
$ npm install

$ make # make clean to clean
$ make local-dev
```

## Migrations

In order to setup a new environment you have to create a superuser

```bash
$ python manage.py migrate
$ python manage.py createsuperuser
```

#### Model changes

Have you changed a model? Then you have to make and apply migrations:

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

## Starting the server

```bash
$ source venv/bin/activate
$ python manage.py migrate
$ python manage.py runserver
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
$ # Fix isort errors
$ isort -rc itdagene
$ # Verify the result with tox
$ tox -e isort
$ # Verify PEP 8 style
$ tox -e flake8
```

## Misc

You **may** have to install these
```bash
$ sudo apt-get install libpq-dev python-dev redis-server zlib1g-dev libjpeg-dev python-pip postgresql postgresql-contrib
$ sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/
$ sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
$ sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/
```

### Nice reads

- [Terminal intro](https://www.digitalocean.com/community/tutorials/an-introduction-to-the-linux-terminal)
- [Django intro](https://www.djangoproject.com/start/)
- [Intro to celery](http://docs.celeryproject.org/en/latest/getting-started/introduction.html)
- [Why docker](https://www.docker.com/what-container)

[docker]: https://www.docker.com/community-edition
[docker-compose]: https://docs.docker.com/compose/overview/
[PEP 8]: https://www.python.org/dev/peps/pep-0008/
[isort]: https://github.com/timothycrosley/isort
