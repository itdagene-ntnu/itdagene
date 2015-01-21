#itDAGENE

[Nettopp fått tilgang? Les her](https://github.com/itdagene-ntnu/itdagene/wiki)

##Avhengigheter

Vi bruker nodejs og npm. Dette må installeres.
Vi bruker [bower](http://bower.io) for å holde styr på statiske filer. Installeres med npm:

    $ npm install -g bower

##Installer
Klon repoet ned, gå inn i det i terminal

Kjør:

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ npm install
    $ bower install
    $ make all

Fiks settings/local.py:
    Eksempel ligger i settings/local_example.py

Deretter kan man sette opp databasen:

    $ python manage.py migrate

Hvis alt går som det skal så har du nå en itDAGENE-side. Kjør utviklingserver med:

    $ python manage.py runserver


Lytte på endringer når man utvikler på frontenden:

    $ make watch
