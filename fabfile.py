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


def install_cron():
    with cd('awsmonitors'):
        sudo('cp crontab /etc/cron.d/awsmonitors')
        sudo('service cron reload')
