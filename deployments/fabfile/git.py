"""
This module fetches code from git and updates
the code base on the server
"""

from fabric.api import puts, run
from fabric.colors import yellow
from fabric.operations import sudo


def fetch_clean_repo(repo):
    """
    Fetch remote code.
    """
    puts(yellow('Fetching remote code from repo {}'.format(repo)))
    sudo("git clone {}".format(repo))


def git_pull(git_branch):
    """
    Switches to @git_branch and pull latest code.
    Also gets all other branches, and removes stale branches.
    """
    git_checkout(git_branch)

    puts(yellow('Pulling latest code from {} branch'.format(git_branch)))
    sudo('git pull --all --prune')


def git_checkout(git_branch):
    """
    Switch to the branch you want to pull code from.
    """
    puts(yellow('Switching to {} branch'.format(git_branch)))
    sudo('git checkout {}'.format(git_branch))
