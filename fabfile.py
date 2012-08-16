from fabric.api import local, run, cd, env
from fabric.context_managers import settings
from fabric.contrib.console import confirm
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
        result = local("bin/django test", capture=True)
    if result.failed and not confirm("Tests failed, continue anyway?"):
        abort("Aborting request")
    else:
        print_color_message("All tests OK!", "green")

def silent_run(cmd):
    f = open(os.devnull, 'w')
    sys.stdout = f
    out = run(cmd)
    sys.stdout = sys.__stdout__
    return out

def deploy_dev():

    env.password = silent_run("cat ~/p")

    if confirm("Do you want to run tests before deploying?"):
        test()

    code_dir = "/home/web/starthjelpa"
    with cd(code_dir):
        run("git pull origin master")
        run("bin/django syncdb --noinput")
        run("bin/django migrate --merge")

    sudo("touch /etc/uwsgi/apps-available/itdagene-dev.ini", shell=False)

def deploy_prod():

    env.password = silent_run("cat ~/p")

    if confirm("Do you want to run tests before deploying?"):
        test()

    code_dir = "/home/web/starthjelpa"
    with cd(code_dir):
        run("git pull origin master")
        run("bin/django syncdb --noinput")
        run("bin/django migrate --merge")

    sudo("touch /etc/uwsgi/apps-available/itdagene-prod.ini", shell=False)
