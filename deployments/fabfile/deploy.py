from fabric.api import *

import base
import database
import support
import tools
import web


@task
def sup(branch='master'):
    """
    Deploy a web app (Django, Postgresql, etc.) server from scratch.
    """
    execute(base.Base(), branch)
    execute(database.Postgresql())
    execute(web.NginxFull())
    execute(support.Support())


@task
def update(branch='master'):
    """
    A full deploy without the hassle.
    * Checks out your latest commit to given branch
    * Ensures that the latest Nginx and Uwsgi configs are installed
    * Ensures that web app log dirs exist and have the correct permissions
    * Installs all pip packages
    * Restarts Nginx and Uwsgi
    """
    tools.git_co(branch)
    execute(support.Support())
    execute(web.NginxBasic())
