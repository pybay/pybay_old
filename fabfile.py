from __future__ import print_function
from datetime import datetime as dt
from os.path import join

from fabric.api import cd, env, hide, local, run, sudo
from fabric.contrib import files

env.hosts = ['pyconsf.com']
env.user = 'pybay'

BASE = "/data/websites"
CHECKOUTS = "/data/websites/checkouts"

def checkout(prod=False):
    """Git clone pybay project to unique folder"""
    path = "prod" if prod else "staging"
    ts = dt.now().strftime("%Y-%m-%d.%H.%M.%S")
    dirname = join(CHECKOUTS, path, ts)
    run("mkdir %s" % dirname)
    with cd(dirname):
        with hide('running', 'stdout'):
            clone_args = '' if prod else ' -b staging'
            run("git clone https://github.com/pybay/pybay.git%s" % clone_args)
    return dirname

def virtualenv(checkout):
    """Create virtualenv in checkout directory."""
    with cd(checkout):
        run("virtualenv ENV")
        with hide('running', 'stdout'):
            run("ENV/bin/pip3 install -r pybay/requirements.txt")
            run("ENV/bin/pip3 install -r pybay/requirements-server.txt")

def migrate(checkout, prod=False):
    """Run migrations in checkout."""
    settings = "pybay.prod_settings" if prod else "pybay.staging_settings"
    with cd(checkout):
        run("ENV/bin/python3 pybay/manage.py migrate --settings=%s" % settings)
        run("ENV/bin/python3 pybay/manage.py compilescss --settings=%s" % settings)
        run("ENV/bin/python3 pybay/manage.py collectstatic --noinput --settings=%s" % settings)

def relink(checkout, prod=False):
    """Move symlink to point to current checkout."""
    dir = "prod" if prod else "staging"
    with cd(BASE):
        run("ln -s %s new && mv -Tf new %s" % (checkout, dir))

def touch(prod):
    """Touch symlinks to reload uwsgi config."""
    dir = "prod" if prod else "staging"
    run("touch /etc/uwsgi-emperor/vassals/%s_uwsgi.ini" % dir)


def deploy(version="staging"):
    """Run this to redeploy site from github master. Run `fab deploy:prod` to deploy main site."""
    prod = True if version == 'prod' else False
    print("Start with a git checkout.")
    dir = checkout(prod)
    print("Created %s" % dir)
    print("Now create the virtualenv")
    virtualenv(dir)
    print("Run migrations and collectstatic")
    migrate(dir, prod)
    print("Update the active version")
    relink(dir, prod)
    touch(prod)
    print("Successfully completed")
