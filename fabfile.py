from fabric.api import run, sudo, env, put
from fabric.context_managers import cd

env.git_repo = "git://github.com/newsapps/awsmonitors.git"


def setup():
    run('git clone %(git_repo)s' % env)
    sudo('apt-get -y install unzip libwww-perl libcrypt-ssleay-perl')
    sudo('easy_install -U boto==2.8')


def update():
    with cd('awsmonitors'):
        run('git reset HEAD')
        run('git checkout .')
        run('git fetch')
        run('git pull')


def install_cron(filename):
    put('crontab-creds', 'awsmonitors/crontab-creds')
    with cd('awsmonitors'):
        sudo('cat crontab-creds %s > /etc/cron.d/awsmonitors' % filename)
        sudo('service cron restart')
        run('rm crontab-creds')


def setup_alarms():
    with cd('awsmonitors'):
        run('./setup_alarms.py')


def remove_cloudkick():
    sudo('apt-get -y remove cloudkick-agent cloudkick-config')


def remove():
    run('rm -Rf awsmonitors')
    sudo('rm /etc/cron.d/awsmonitors')
    sudo('service cron restart')
