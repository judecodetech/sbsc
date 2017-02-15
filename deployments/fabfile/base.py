"""
Base Task for all server deploys.
"""

from os.path import join

from fabric.api import env
from fabric.tasks import Task

from . import tools


class Base(Task):
    """
    Base Task to install basic server requirements
    """
    name = "prep_server"

    APT_DEBS = (
        'build-essential',
        'curl',
        'ethtool',
        'gdb',
        'git-core',
        'htop',
        'ipython',
        'libpq-dev',
        'nginx',
        'nginx-full',
        'python3-dev',
        'python3-pip',
        'python3-setuptools',
        'python3-venv',
        'screen',
        'sysstat',
        'tree',
        'uwsgi',
        'uwsgi-plugin-python3',
        'whois',
        'zsh',
    )

    @classmethod
    def run(cls, git_branch='master'):
        """
        Run Base task
        """
        tools.set_timezone_sast()

        tools.apt_clean_up()

        tools.apt_get_install(cls.APT_DEBS)

        tools.upgrade_pip()

        tools.set_shell_to_zsh()

        tools.chown_log_dir()

        tools.git_co(git_branch)

        tools.pip_install_reqs(join(env.PROJECT_DIR, 'requirements.txt'))

        tools.configure_project_owner_user()
        tools.assign_correct_project_dir_permissions()
