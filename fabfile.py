import os
from contextlib import contextmanager
from fabric.api import cd, env, prefix, run, sudo, task


PROJECT_NAME = 'jumpvrp-data-service'
PROJECT_ROOT = '/home/seksan/deploy/%s' % PROJECT_NAME
REPO = 'git@git.morange.co.th:jumpup/%s.git' % PROJECT_NAME

env.hosts = ['seksan@erp.morange.co.th']

@contextmanager
def source_virtualenv():
    with prefix('source ' + os.path.join(PROJECT_ROOT, 'bin/activate')):
        yield

@task
def deploy():
    """
    Deploys the latest tag to the production server
    """
    run('chown -R %s:%s %s' % (env.user, env.user, PROJECT_ROOT))

    with cd(PROJECT_ROOT):
        run('git pull origin master')
        with source_virtualenv():
            run('source ./bin/activate && pip install -r requirements.txt')
            with cd(os.path.join(PROJECT_ROOT, 'dataservice')):
                run('./manage.py migrate')
