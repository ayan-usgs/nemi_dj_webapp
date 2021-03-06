import os

from fabric.api import local, task, abort, env
from fabric.context_managers import lcd, shell_env, warn_only
from fabric.contrib.console import confirm


#REPO_URL = "ssh://git@cida-eros-stash.er.usgs.gov:7999/nemi/nemi_dj_webapp.git"

env.roledefs = {
    'dev' : ['django@cida-eros-nemidjdev.er.usgs.gov'],
    'test' : ['django@cida-eros-nemidjqa.er.usgs.gov'],
    'prod' : ['django@cida-eros-nemidjprod2.er.usgs.gov']
    }


def execute_django_command(command, for_deployment=False, force_overwrite=False):
    '''
    When building for deployment there will not be a local_settings.py. The
    django management commands require SECRET_KEY to be defined so create a
    temporary local_settings, perform the command and then remove the local_settings.
    The command parameter should be a string.
    '''
    if for_deployment:
        local('echo "SECRET_KEY = \'temporary key\'" > nemi_project/local_settings.py')

    if force_overwrite and for_deployment:
        local('yes yes | env/bin/python manage.py ' + command)
    else:
        local('env/bin/python manage.py ' + command)

    if for_deployment:
        local('rm nemi_project/local_settings.*')


@task
def build_virtualenv(for_deployment=False):
    '''Create the project's virtualenv and install the project requirements.
    Assumes code has been retrieved from SVN'
    '''
    if for_deployment:
        download_cache = os.environ['HOME'] + '/.pip/download_cache'
        oracle_home = os.environ['ORACLE_HOME']

    else:
        download_cache = os.environ.get('PIP_DOWNLOAD_CACHE', '')
        oracle_home = os.environ.get('ORACLE_HOME', '')
        if download_cache == '' and not confirm('PIP_DOWNLOAD_CACHE not defined. Continue anyway?'):
            abort('Aborting')

        if oracle_home == '':
            abort('Must define ORACLE_HOME which should point to the oracle client directory.')

    local('virtualenv --no-site-packages --python=python3.6 env')

    if for_deployment:
        # this is needed so that the link to lib64 is relative rather than absolute
        local('rm env/lib64')
        local('ln -s lib env/lib64')

    with shell_env(PIP_DOWNLOAD_CACHE=download_cache, ORACLE_HOME=oracle_home):
        local('env/bin/pip --timeout=120 install -r requirements.txt')


@task
def build_project_env(for_deployment=False):
    '''
    Assumes code has already been retrieved from SVN and requirements installed in the virtualenv in env.
    '''
    # Install or update compass and compile sass files
    # Note that nemidjdev will always contain a copy of the latest css files in
    # webapps/nemi/nemi_project/static/styles if you don't have Ruby installed.
    with lcd('compass'):
        with shell_env(GEM_HOME=os.environ.get('PWD', '') + '/compass/Gem'):
            with warn_only():
                available = local('gem list -i compass', capture=True)
            if available == 'true':
                local('gem update -i Gem compass')
            else:
                local('gem install -i Gem compass -v 0.12.7')
        local('./compass.sh compile')

    # Collect static files
    if for_deployment:
        execute_django_command('collectstatic --settings=nemi_project.settings', for_deployment, force_overwrite=True)


@task
def run_jenkins_tests(for_deployment=False):
    if not for_deployment:
        abort('Can\'t run jenkins test on local development server')

    with shell_env(DBA_SQL_DJANGO_ENGINE='django.db.backends.sqlite3',
                   PATH='$HOME/bin:$PATH'):
        local('echo $PATH')
        execute_django_command('jenkins --enable-coverage', for_deployment)


@task
def build(for_deployment=False):
    build_virtualenv(for_deployment)

    # Create dummy local_settings.py if for_deployment
    build_project_env(for_deployment)
