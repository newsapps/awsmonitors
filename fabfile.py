from fabric.api import run, env
from fabric.context_managers import cd

env.git_repo = "https://github.com/newsapps/awsmonitors.git"


def setup():
    run('git clone %(git_repo)s' % env)


def update():
    with cd('awsmonitors'):
        run('git reset HEAD')
        run('git checkout .')
        run('git fetch')
        run('git pull')
