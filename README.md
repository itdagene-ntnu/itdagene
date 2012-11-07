#itDAGENE goes django

[Nettopp fått tilgang? Les her](https://github.com/itdagene-ntnu/itdagene/wiki/Erfaringskriv)

##Installer
Klon repoet ned, gå inn i det i terminal

Kjør:

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

Deretter kan man sette opp databasen:

    python manage.py syncdb
    python manage.py migrate

Hvis alt går som det skal så har du nå en itDAGENE-siden. Kjør utviklingserver med:

    python manage.py runserver
