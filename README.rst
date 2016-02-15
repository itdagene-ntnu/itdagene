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


If you name your virtualenv something, remember to add it to gitignore. "env" is already ignored.

Activate the environment with::

    . /env/bin/activate


To install psocopg2 we require some additional libraries::

    sudo apt-get install libpq-dev python-dev redis-server


Install the python packages with pip::

    sudo pip install -r requirements/base.txt
Install dependencies with make, and create a local settings file for development::

    make install
    make local-dev
If you get an error saying it can't find "node", install nodejs-legacy via apt-get.

Setting up the database
~~~~~~~~~~~~~~~~~~~~~~~
We use Postgreql for our database.

After having done all of the above::

    sudo apt-get install python-pip postgresql postgresql-contrib
Then, run the following commands::

    sudo su - postgres
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
    python manage.py runserver
.. |frigg| image:: https://ci.frigg.io/badges/itdagene-ntnu/itdagene/
    :target: https://ci.frigg.io/itdagene-ntnu/itdagene/last/

.. |coverage| image:: https://ci.frigg.io/badges/coverage/itdagene-ntnu/itdagene/
    :target: https://ci.frigg.io/itdagene-ntnu/itdagene/last/
