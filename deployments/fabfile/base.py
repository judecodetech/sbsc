"""
Base Task for all server deploys.
"""

from fabric.api import cd, env, execute, puts, run
from fabric.contrib.files import exists
from fabric.tasks import Task

import git
import nginx
import tools


class Base(Task):
    """
    Base Task to install basic server requirements
    """
    name = "prep_server"
    APT_DEBS = (
        'bc',
        'git-core',
        'gzip',
        'htop',
        'nginx',
        'python-pip',
        'rsync',
        'sendmail',
        'zsh',
    )

    def run(self, git_branch='dev'):
        """
        Run Base task
        """

        # Housekeeping
        run('apt-get clean')
        run('apt-get update')

        tools.apt_get_install(self.APT_DEBS)

        tools.set_shell_to_zsh()

        if exists(env.REPO_DIR):
            with cd(env.REPO_DIR):
                git.git_pull(git_branch)
        else:
            with cd(env.HOME_DIR):
                git.fetch_clean_repo(env.REPO_URL)

        execute(nginx.Nginx())
BASE = Base()
