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


## Ting som kan gå galt

### Jeg får IOError feil

Dette skjer mest sannsynlig fordi du ikke har en JPEG-encoder installert. PIL har ikke
innebygd støtte for JPEG, så det må installeres separat. På OS X kan dette gjøres vha.
[Homebrew](http://brew.sh/) (du bruker Homebrew, sant?). Etter at du har sourcet venv:

    pip uninstall PIL
    brew install jpeg
    pip install PIL
