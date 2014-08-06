
from fabric.decorators import task
from fabric.state import env
from django_fabric import App

env.user = 'itdagene'
env.hosts = ['itdagene.abakus.no']

site = App(
    project_paths={
        'production': '/home/itdagene/itdagene'
    },
    urls={
        'production': 'http://itdagene.no'
    },
    restart_command={
        'production': 'service uwsgi restart'
    },
    project_package='itdagene',
    requirements={
        'production': 'requirements-prod.txt'
    }
)

deploy = task(site.deploy)
test = task(site.test)