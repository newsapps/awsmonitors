from fabric.api import run, sudo, env
from fabric.context_managers import cd

env.git_repo = "https://github.com/newsapps/awsmonitors.git"


def setup():
    run('git clone %(git_repo)s' % env)
    sudo('apt-get -y install unzip libwww-perl libcrypt-ssleay-perl')


def update():
    with cd('awsmonitors'):
        run('git reset HEAD')
        run('git checkout .')
        run('git fetch')
        run('git pull')


def install_cron(filename):
    with cd('awsmonitors'):
        sudo('cp %s /etc/cron.d/awsmonitors' % filename)
        sudo('service cron restart')
