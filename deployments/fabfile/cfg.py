"""
Define generic constants for reusabililty
"""

from os.path import join, sep

from fabric.api import env

env.HOME_DIR = join(sep, 'etc')
env.REPO_DIR = join(env.HOME_DIR, 'sbsc')
env.REPO_URL = 'https://gitlab.com/erpweb/sbsc.git'
env.OPS_DIR = join(env.REPO_DIR, 'deployments')
env.OPS_ETC_DIR = join(env.OPS_DIR, 'ubuntu', 'etc')

# add subdomains to this list separated with a comma
env.DOMAINS = 'sbsc.serthe.com'