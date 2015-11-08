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

    sudo apt-get install libpq-dev python-dev


Install the python packages with pip::

    sudo pip install -r requirements/base.txt


Install dependencies with make::

    make install


If you get an error saying it can't find "node", install nodejs-legacy via apt-get. 








.. |frigg| image:: https://ci.frigg.io/badges/itdagene-ntnu/itdagene/
    :target: https://ci.frigg.io/itdagene-ntnu/itdagene/last/

.. |coverage| image:: https://ci.frigg.io/badges/coverage/itdagene-ntnu/itdagene/
    :target: https://ci.frigg.io/itdagene-ntnu/itdagene/last/
