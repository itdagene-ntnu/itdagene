#itDAGENE goes django

[Nettopp fått tilgang? Les her](https://github.com/itdagene-ntnu/itdagene/wiki/Erfaringskriv)

##Installer
Klon repoet ned, gå inn i det i terminal

Kjør:

    python bootstrap.py
    bin/buildout

Dersom dette er en lokal installasjon kan du bare gå videre.
Hvis ikke må man endre settingsfil det gjøres i *bin/django* og *bin/django.wsgi*. Man
endrer da:

    'project.development'

til

    'project.dev-no-toolbar' #hvis det er en dev server
    'project.production'     #hvis det er en prod server

Deretter kan man sette opp databasen:

    bin/django syncdb
    bin/django migrate
    bin/django loaddata base_data.json

Hvis alt går som det skal så har du nå en itDAGENE-siden.

I motsetning til vanlig så må man nå kjøre bin/django istedet for python manage.py.
Det vil f.eks si hvis du vil kjøre serveren så bruk følgende:

    bin/django runserver