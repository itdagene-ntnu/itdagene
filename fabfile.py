from fabric.api import local, run, cd, env
from fabric.context_managers import settings
from fabric.contrib.console import confirm
from fabric.decorators import task
from fabric.operations import sudo
from fabric.utils import abort
import sys, os

env.hosts = ['web@itdagene.no']

def print_color_message(message, color):
    def get_color_code(color):
        colors = {'green':'\033[92m', 'yellow':'\033[93m', 'red':'\033[91m'}
        if color in colors:
            return colors[color]
        return ''

    print get_color_code(color) + message + '\033[0m'

def prepare_deploy():
    local("git status")

def test():
    with settings(warn_only=True):
        print_color_message("Running tests, please wait!", "yellow")
        result = local("bin/django test --failfast", capture=True)
    if result.failed:
        if not confirm("Tests failed, continue anyway?"):
            print_color_message("Aborted deployment!", "red")
            abort("")
    else:
        print_color_message("All tests OK!", "green")

def silent_run(cmd):
    f = open(os.devnull, 'w')
    sys.stdout = f
    out = run(cmd)
    sys.stdout = sys.__stdout__
    return out

def run_server_updates(code_dir):
    with cd(code_dir):
        run("git pull origin master")

        run("venv/bin/pip install -r requirements.txt")

        # Sync the database
        run("venv/bin/python manage.py syncdb --noinput")

        # Migrate changes to the database
        run("venv/bin/python manage.py migrate --merge")


@task(default=True)
def deploy_dev():
    env.password = silent_run("cat ~/p")

    #if confirm("Do you want to run tests before deploying?"):
    #    test()

    run_server_updates("/home/web/itdagene-dev")

    sudo("touch  /home/web/uwsgi/itdagene-dev.ini", shell=False)

@task
def deploy_prod(run_test=True):
    env.password = silent_run("cat ~/p")

    if run_test: test()

    run_server_updates("/home/web/itdagene-prod")

    sudo("touch /home/web/uwsgi/itdagene-prod.ini", shell=False)
