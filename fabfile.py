import os
import sys

from fabric.decorators import task
from fabric.state import env

from django_fabric import App


# This is to make fabric able to read our django settings
sys.path.append(os.path.dirname(__file__))

env.user = 'itdagene'
env.hosts = ['itdagene.no']

site = App(
    project_paths={
        'prod': '/home/itdagene/itdagene',
    },
    project_package='itdagene',
    restart_command='touch /etc/uwsgi/apps-enabled/itdagene.ini'
    requirements = {
        'prod': 'requirements-prod.txt'
    }
)

deploy_dev = task(site.deploy_dev)
deploy_prod = task(site.deploy_prod)
clone_prod_data = task(site.clone_prod_data)
test = task(site.test)
