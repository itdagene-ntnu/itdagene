itDAGENE
========
|circle|


This is the code base for http://www.itdagene.no. It is a standard django project, and uses Celery for async tasks

Installation
------------

First make sure that you have the following software installed on your system:

  * Python 2.7
  * Virtualenv for Python 2.7
  * NodeJS 4.2 or greater
  * npm for NodeJS (Version 2.x!)
  * bower (install globally with npm)

Change directory into the root folder of the project.
Create a virtualenv by typing the following command::


    virtualenv venv


If you name your virtualenv somethingelse, remember to add it to gitignore. "env" is already ignored.

Activate the environment with::

    . venv/bin/activate


Install these libraries and make symlinks::

    sudo apt-get install libpq-dev python-dev redis-server zlib1g-dev libjpeg-dev python-pip postgresql postgresql-contrib
    sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/
    sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
    sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/


Install the python packages with pip::

    pip install -r requirements/base.txt
Install packages::
 
    bower install
    npm install
Install dependencies with make, and create a local settings file for development::

    make
    make local-dev
To compile css from stylus every second, run::

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

Testing
~~~~~~~
Let the test setup use PostgreSQL. First locate the Postgres config file::

    locate pg_hba.conf
It should return something like '/etc/postgresql/9.3/main/pg_hba.conf'.
Open the file with your favourite text editor (For example vi or vim). You should get something like this::

    # ... Text ...
    local   all             postgres                                peer
    
    # TYPE  DATABASE        USER            ADDRESS                 METHOD
    
    # "local" is for Unix domain socket connections only
    local   all             all                                     peer
    # IPv4 local connections:
    host    all             all             127.0.0.1/32            md5
    # IPv6 local connections:
    host    all             all             ::1/128                 md5
    # ... Text ...
Change METHOD for the Unix domain socket connection from 'peer' to 'trust'::

    # ... Text ...
    local   all             postgres                                peer
    
    # TYPE  DATABASE        USER            ADDRESS                 METHOD
    
    # "local" is for Unix domain socket connections only
    local   all             all                                     trust
    # IPv4 local connections:
    host    all             all             127.0.0.1/32            md5
    # IPv6 local connections:
    host    all             all             ::1/128                 md5
Save and exit.
Install the following packages with pip::

    pip install tox isort coverage
Run::

    isort -rc itdagene
To run all tests from now on; run::

    tox

.. |circle| image:: https://circleci.com/gh/itdagene-ntnu/itdagene.svg?style=svg&circle-token=abcfbea6689e5baef8a1fbb7fa6eb822efdd5bfb
    :target: https://circleci.com/gh/itdagene-ntnu/itdagene
