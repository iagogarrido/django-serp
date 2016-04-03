from fabric.api import local, cd, run, env as fabenv
from subprocess import call
import sys


REMOTE_HOST_NAME = "ec2-user@ec2-52-11-231-198.us-west-2.compute.amazonaws.com"
REMOTE_KEY_PATH = "serp-website.pem"
REMOTE_DIR_PATH = "/var/www/django/mysite"

fabenv.hosts = [REMOTE_HOST_NAME]
fabenv.key_filename = REMOTE_KEY_PATH
        
def env(action):
    if action == "init":
        print("Initalizing virtualenv...")
        local("virtualenv -p python3 env")
        local("source env/bin/activate")
        
        print("Installing dependencies...")
        local("pip install --upgrade pip")
        local("pip install django")
        local("pip install fabric3")

        local("deactivate")
    elif action == "check":
        if hasattr(sys, "real_prefix"):
            print("Checking virtual environment... OK")
            return True
        else:
            print("Checking virtual environment... FAIL")
            print("Execute source env/bin/activate before entering any command")
            return False
    # TODO: Check how I can do this
    #elif action == "activate":
    #    print("Activating virtualenv...")
    #    local("env/bin/activate_this.py")
    #    local("source env/bin/activate")
    else:
        print("Unknown action: " + action)


def manage(action):
    if env("check"):
        if action == "test":
            print("Running tests...")
            local("python manage.py test serp")
        elif action == "runserver":
            print("Running development server...")
            local("python manage.py runserver 8000")
        else:
            print("Unknown action: " + action)


def deploy():
    if env("check"):
        with cd(REMOTE_DIR_PATH):
            run("git pull")

