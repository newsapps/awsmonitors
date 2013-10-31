from fabric.api import run, sudo, env, put
from fabric.context_managers import cd
import os

env.git_repo = "git://github.com/newsapps/awsmonitors.git"


def setup():
    sudo('apt-get -y install python-boto git unzip libwww-perl libcrypt-ssleay-perl')
    run('git clone %(git_repo)s' % env)


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


def setup_instance_alarms():
    with cd('awsmonitors'):
        run('AWS_ACCESS_KEY_ID=%(AWS_ACCESS_KEY_ID)s AWS_SECRET_ACCESS_KEY=%(AWS_SECRET_ACCESS_KEY)s ./setup_instance_alarms.py' % os.environ)


def remove_cloudkick():
    sudo('apt-get -y remove cloudkick-agent cloudkick-config')


def remove():
    run('rm -Rf awsmonitors')
    sudo('rm /etc/cron.d/awsmonitors')
    sudo('service cron restart')
