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
        'prod': '/home/itdagene/itdagene/',
    },
    project_package='itdagene',
    restart_command='sudo service itdagene restart',
    requirements={
        'prod': 'requirements-prod.txt'
    }
)

deploy = task(site.deploy)