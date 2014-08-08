
from fabric.decorators import task
from fabric.api import sudo, run
from fabric.context_managers import quiet
from fabric.state import env
from django_fabric import App

env.user = 'itdagene'
env.hosts = ['itdagene.abakus.no']

class Site(App):
    project_paths = {
        'production': '/home/itdagene/itdagene'
    }
    urls = {
        'production': 'http://itdagene.no'
    }
    restart_command = {
        'production': 'sudo service uwsgi restart'
    }
    project_package = 'itdagene'
    requirements = {
        'production': 'requirements-prod.txt'
    }

    def run(self, command):
        with quiet():
            if command in self.restart_command.values():
                return sudo(command)
            else:
                return run(command)



site = Site()

deploy = task(site.deploy)
test = task(site.test)