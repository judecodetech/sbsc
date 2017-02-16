from fabric.api import *
from fabric.colors import *
from fabric.tasks import Task
from fabric.contrib.files import exists

from . import tools

PG_VERSION = '9.5'
PG_ETC_DIR = '/etc/postgresql/' + PG_VERSION + '/main/'
PG_DATA_DIR = '/var/lib/postgresql/' + PG_VERSION + '/main/'


class Postgresql(Task):
    """
    Get PostgreSQL installed and access configured.
    """
    name = 'Postgresql'

    DB_NAME = 'sbsc'
    DJANGO_ROLE = 'sbsc'
    DJANGO_PASS = 'sbsc'
    BACKUP_USER = 'backup'
    BACKUP_PASS = 'YxhAdBpSuL8QLeCMWlbB2SEZen7wHd37'

    def run(self, pg_version=PG_VERSION):
        """
        This moves PG to a non-ubuntu repo which is naturally newer.  We will migrate to 9.3 on it, then to 9.4.
        """

        pg_apt_repo = '/etc/apt/sources.list.d/pgdg.list'

        if not exists(pg_apt_repo):
            sudo('echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > {}'.format(pg_apt_repo))
            sudo('wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -')
            sudo('apt-get update')
            sudo('apt-get remove -y postgresql postgresql-contrib postgresql-common')
            sudo('apt-get upgrade -y')

        debs = (
            # To build the pip version of psycopg2.
            'libpq-dev',
            'gcc',
            'mutt',  # For emailing reports.
            'postgresql-' + pg_version,
            'postgresql-contrib-' + pg_version,
        )
        tools.apt_get_install(debs)
        tools.apt_get_purge(('python-psycopg2',))
        sudo('pip install -U psycopg2')

        sudo('service postgresql start')

        # Create Django role.
        user_exists = tools.su(
            'postgres', '''psql -t -A -c "SELECT COUNT(*) FROM pg_roles WHERE rolname = {u!r};"'''.format(u=self.DJANGO_ROLE))

        if user_exists != '1':
            tools.su(
                'postgres',
                'psql -c "CREATE ROLE {0} WITH LOGIN CREATEDB NOCREATEUSER ENCRYPTED PASSWORD E{1!r}"'.format(
                    self.DJANGO_ROLE, self.DJANGO_PASS))

        # Create database.
        with settings(warn_only=True):
            db_exists = tools.su('postgres', 'psql -d {db} -c ""'.format(db=self.DB_NAME)).succeeded

        if not db_exists:
            # Add extensions to template DB, because all new DBs are copied from it.
            tools.su(
                'postgres',
                'psql -c "CREATE DATABASE {0} WITH OWNER {1};"'.format(self.DB_NAME, self.DJANGO_ROLE))

        tools.create_extensions('template1', ['hstore', 'adminpack', 'btree_gist'])
        tools.create_extensions(self.DB_NAME, ['hstore', 'adminpack', 'btree_gist'])

        # Create backup user
        user_exists = tools.su(
            'postgres', '''psql -t -A -c "SELECT COUNT(*) FROM pg_roles WHERE rolname = {u!r};"'''.format(u=self.BACKUP_USER))

        if user_exists != '1':
            tools.su('postgres', 'psql -c "CREATE ROLE {0} WITH LOGIN NOCREATEDB NOCREATEUSER ENCRYPTED PASSWORD E{1!r}"'.format(self.BACKUP_USER, self.BACKUP_PASS))

        sudo('service postgresql restart', pty=True)
