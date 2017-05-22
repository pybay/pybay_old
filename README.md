# pybay

The website for PyBay - the Bay Area Python Conference.

To work on this you'll need Python 3. Then:

1. Fork the repo to your own personal github.
    - also clone the symposion repository, take note of the path to symposion/
2. Clone the repo to your local environment.
3. Create a virtualenv and activate it
4. `pip install` the requirements
5. `pip install -e` the symposion repository
6. start the management server

Try:

    $ git clone git@github.com:YOURUSERNAME/pybay
    $ git clone git@github.com:pybay/symposion.git
    $ cd pybay
    $ python3 -m venv .
    $ source ./bin/activate
    (ENV)$ pip install -r requirements.txt
    (ENV)$ pip install -e YOUR/PATH/TO/symposion/   # this installs our symposion fork to ENV!
    (ENV)$ ./manage.py migrate
    (ENV)$ ./manage.py loaddata fixtures/*
    (ENV)$ ./manage.py runserver

The default admin user is test and password is test

If you also will be adding fixes to symposion we forked you can delete
the version in your site-packages and symlink in the directory on your
disk. Eg:

    $ cd ~/workspace/pybay/ENV/lib/python3.6/site-packages/
    $ rm -rf symposion
    $ ln -s ~/workspace/symposion/symposion .

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
