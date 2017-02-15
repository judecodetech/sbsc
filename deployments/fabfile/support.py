from os.path import join

from fabric.api import *
from fabric.contrib.files import exists
from fabric.tasks import Task

import tools


class Support(Task):
    """
    Install Kando web server.
    """
    name = 'Support'

    def run(self):
        tools.chown_log_dir()

        if not exists(env.VENV_DIR):
            sudo('python3 -m venv {}'.format(env.VENV_DIR))

        sudo('mkdir -p /var/www/static/')
        sudo('chown -R www-data:www-data /var/www')

        with tools.virtualenv('/var/venv/'):
            sudo('pip install -U -r {}'.format(join(env.PROJECT_DIR, 'requirements.txt')))

            with cd(env.PROJECT_DIR):
                sudo('python3 manage.py migrate --noinput')
                sudo('python3 manage.py collectstatic --noinput')

        tools.assign_correct_project_dir_permissions()

        tools.restart_uwsgi()
