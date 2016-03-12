itDAGENE
========
|frigg| |coverage|


This is the code base for http://www.itdagene.no. It is a standard django project, and uses Celery for async tasks

Installation
------------

First make sure that you have the following software installed on your system:

  * Python 2.7
  * Virtualenv for Python 2.7
  * NodeJS 4.2 or greater
  * npm for NodeJS
  * bower (install globally with npm)

Change directory into the root folder of the project.
Create a virtualenv by typing the following command::


    virtualenv env


If you name your virtualenv somethingelse, remember to add it to gitignore. "env" is already ignored.

Activate the environment with::

    . env/bin/activate


Install these libraries and make symlinks::

    sudo apt-get install libpq-dev python-dev redis-server zlib1g-dev libjpeg-dev python-pip postgresql postgresql-contrib
    sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/
    sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
    sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/


Install the python packages with pip::

    sudo pip install -r requirements/base.txt
Install dependencies with make, and create a local settings file for development::

    make
    make local-dev

To compile css from stylus every second, run:
    make watch-css

Setting up the database
~~~~~~~~~~~~~~~~~~~~~~~
We use Postgresql for our database.

After having installed the libraries above; run the following commands::

    sudo -su postgres
    psql
    CREATE DATABASE itdagene;
    CREATE USER itdagene WITH PASSWORD 'itdagene';
    ALTER ROLE itdagene SET client_encoding TO 'utf8';
    ALTER ROLE itdagene SET default_transaction_isolation TO 'read committed';
    ALTER ROLE itdagene SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE itdagene TO itdagene;
    \q
    exit
Apply migrations and start server by typing::

    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
.. |frigg| image:: https://ci.frigg.io/badges/itdagene-ntnu/itdagene/
    :target: https://ci.frigg.io/itdagene-ntnu/itdagene/last/

.. |coverage| image:: https://ci.frigg.io/badges/coverage/itdagene-ntnu/itdagene/
    :target: https://ci.frigg.io/itdagene-ntnu/itdagene/last/
