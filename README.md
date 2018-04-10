# pybay

[![Build Status](https://travis-ci.org/pybay/pybay.svg)](https://travis-ci.org/pybay)

The website for PyBay - the Bay Area Python Conference.

To work on this you'll need Python 3.6. Then:

1. Fork the repo to your own personal github.
    - also clone the symposion repository, take note of the path to symposion/
2. Clone the repo to your local environment.
3. Use `pipenv install` to install all required packages locally (using a virtualenv)
4. Use `pipenv shell` to use the local packages
5. start the management server

Try:

    $ python3.6 -m pip install --user pipenv
    $ git clone git@github.com:pybay/symposion
    $ git clone git@github.com:YOURUSERNAME/pybay
    $ cd pybay
    $ python3.6 -m pipenv install --dev
    $ python3.6 -m pipenv shell
    (ENV)$ python ./manage.py migrate
    (ENV)$ python ./manage.py loaddata fixtures/*     # doesn't work on Windows, see "Windows instructions" below
    (ENV)$ python ./manage.py runserver

The default admin user is test and password is test

You may need to update your copy of symposion from time to time.

### Windows Instructions

For some reason, running `manage.py loaddata fixtures/*` gives a `No fixture named '*' found` error on Windows. You'll have to load each fixture file individually:

    (ENV)$ python manage.py loaddata fixtures/auth.json
    (ENV)$ python manage.py loaddata fixtures/conference.json
    (ENV)$ python manage.py loaddata fixtures/proposal_base.json
    (ENV)$ python manage.py loaddata fixtures/sites.json
    (ENV)$ python manage.py loaddata fixtures/sponsor_benefits.json
    (ENV)$ python manage.py loaddata fixtures/sponsor_levels.json

(You can ignore the "invalid foreign keys" warnings you get. The foreign keys will become valid once you've loaded all the fixture files.)

## Deploying

Install fabric. Then use the `fab` command to run the deploy
task. You'll need the ssh login password for this.

    $ pip install fabric3
    $ fab deploy
    [pyconsf.com] Executing task 'deploy'
    Start with a git checkout.
    [pyconsf.com] Passphrase for private key:
    ... much output...
    Successfully completed

By default the deploy task deploys to staging.pyconsf.com using pybay's
staging branch.  To deploy master branch to production (same server but
virtualhost pyconsf.com) run it with the prod target as an argument.

    $ fab deploy:prod
    [pyconsf.com] Executing task 'deploy'
    ... much output...
    Successfully completed
