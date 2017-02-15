"""
Utilities (but no Fabric tasks).
"""
from contextlib import contextmanager

from os.path import join

import posixpath

from fabric.api import abort, cd, env, prefix, puts, run, settings, sudo
from fabric.colors import green, red, yellow
from fabric.contrib.files import exists, append
from fabric.contrib.console import confirm

LE_REPO = 'https://github.com/letsencrypt/letsencrypt'
LE_DIR = '/var/letsencrypt'
LE_CRON = join(env.ETC_DIR, 'cron.d', 'ssl_cert_renewal')

NGINX_PLACEHOLDER = 'INSERT_HOST_HERE'

APP_LOG_DIR = join('/var', 'log', 'kando')


def apt_get_install(packages):
    """
    Install a list of packages
    """
    sudo('apt-get -y --no-install-recommends install {}'.format(' '.join(packages)), shell=False)


def prep_gulp(repo_path, npm_debs):
    """
    Install gulp and all its dependencies using npm.
    Run gulp to generate the CSS static file.
    """
    puts(green('Installing gulp and its dependencies using npm(node package manager)'))
    with cd(repo_path):
        run('npm install {}'.format(' '.join(npm_debs)))
        run('npm install -g bower gulp')
        run('bower install bourbon --allow-root')
        run("gulp production")


def set_shell_to_zsh():
    """
    Set the default shell to zsh
    """
    puts(yellow('Installing OhMyZsh theme and setting zsh to default shell'))
    run('curl -L http://install.ohmyz.sh | sh')


def create_directory(path):
    """
    Create directory. If the path doesn't exist, will create it.
    """
    puts(green('Creating website home directory'))
    run('mkdir -p {}'.format(path))


def install_letsencrypt():
    """
    Enable HTTPS and SSL on Nginx.
    Installs a temprorary Nginx config to allow LE to verify certificate generation.
    """
    puts(yellow('Installing insecure intermediate Nginx config'))
    run('install -v -m 644 {} /etc/nginx/nginx.conf'.format(
        join(env.ETC_DIR, 'nginx', 'insecure_nginx.conf')))
    # Replace INSERT_HOST_HERE instaces with host name
    sed_replace(NGINX_PLACEHOLDER, env.host, join('/etc', 'nginx', 'nginx.conf'))

    # Ensure temp settings propagate
    run('systemctl restart nginx')

    puts(yellow('Starting Installation of letsencrypt to enable HTTPs and SSL on Nginx'))
    git_co('master', LE_DIR, LE_REPO)

    with cd(LE_DIR):
        run('chgrp www-data /usr/share/nginx/html/')
        run('./letsencrypt-auto certonly -a webroot --webroot-path=/usr/share/nginx/html -d {}'.format(env.host))

        # Generate a 2048-bit cert
        run('openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048')

    puts(yellow('Copying cron to refresh certificate.'))
    run('install -v -m 644 {} /etc/cron.d/'.format(LE_CRON))


def sed_replace(regex, replacement, file_path):
    """
    Replace all instances of @regex with @replacement in the given @file_path.
    """
    puts(yellow('Replacing all instances of {} with {} in {}'.format(regex, replacement, file_path)))
    run('sed -i \'s/{}/{}/g\' {}'.format(regex, replacement, file_path))


def apt_clean_up():
    sudo('apt-get update')
    sudo('apt-get -y dist-upgrade')
    sudo('apt-get -y autoremove')


def apt_get_purge(packages):
    """
    Purge a list of packages
    """
    sudo('apt-get -y purge {}'.format(' '.join(packages)), shell=False)


def pip_install_reqs(requirements_file_path):
    """
    Install packages using pip requirements file
    """
    sudo('pip3 install -U -r {}'.format(requirements_file_path))  # NOTE: sudo negates agent forwarding!!!


def create_directories(directories):
    """
    Create a list of directories. Doesn't error when directory already exists. directories must be list, not string.
    """
    sudo('mkdir -p {}'.format(' '.join(directories)))


def add_user_to_group(group, user):
    """
    Ensure group exists and add user to it, if the user exists
    """
    with settings(warn_only=True):
        sudo('addgroup {group}'.format(group=group))
        sudo('usermod -aG {group} {user}'.format(group=group, user=user))


def chown_log_dir():
    """
    Create and groom the logging directory.
    Ensures www-data is added to baywest group
    """

    create_directories([APP_LOG_DIR])

    # Add default Django log file
    sudo('touch {}'.format(join(APP_LOG_DIR, 'kando.log')))

    group = 'breadcrumb'
    users = ('www-data', )
    for user in users:
        add_user_to_group(group, user)

    sudo('chown -R {user}:{group} {log_dir}'.format(user='root', group=group, log_dir=APP_LOG_DIR))
    sudo('chmod -Rf g+rwX {log_dir}'.format(log_dir=APP_LOG_DIR))


def git_co(branch, dest=env.GIT_REPO_DIR, repo_url=env.GIT_REPO_URL):
    """
    Checkout (cloning if necessary) git branch from repo to dest.
    """
    create_directories([env.BASE_DIR, ])
    with settings(sudo_prefix="sudo -E -S -p '{}' ".format(env.sudo_prompt)):

        if not exists(dest):
            sudo('git clone -b {0} {1} {2}'.format(branch, repo_url, dest))

        with cd(dest):
            git_setup_remote(repo_url)

            # todo: replace below 'find' adding 'x' to git clean when grunt puts generated templates
            # in a Django template dir outside of the repository.
            sudo('find %s -iname "*.pyc"  -exec rm -vf "{}" \;' % dest)
            sudo('git clean -df')

            sudo('git fetch --prune')
            sudo('git checkout -f {}'.format(branch))
            with settings(warn_only=True):
                sudo('git branch --set-upstream-to=origin/{br} {br}'.format(br=branch))
            result = sudo('git pull')
            if result.failed and not confirm('Pull failed. Continue anyway?'):
                abort('Aborting at user request.')


def git_setup_remote(repo_url):
    """
    Remove all remotes and (re)add just the needed one
    """
    with settings(warn_only=True):
        remotes_str = run('git remote -v').strip()
        if remotes_str:
            # Handle the No-remotes case.
            remotes = set([r.split()[0] for r in remotes_str.split('\n')])
            for r in remotes:
                run('git remote rm {}'.format(r))

        sudo('git remote add origin {}'.format(repo_url))


def set_timezone_sast():
    """
    Set timezone to South African Standard Time.
    """
    sudo('ln -sf /usr/share/zoneinfo/Africa/Johannesburg  /etc/localtime')


def su(user, command, password=env.password):
    """
    Run a command as a different user
    """
    with settings(password=password, sudo_prefix='su {} -c'.format(user)):
        return sudo(command)


def configure_project_owner_user():
    """
    Create a user called project-owner that should own all executable Python files.
    This user won't have shell access.
    """

    with settings(warn_only=True):
        result = sudo('grep project-owner /etc/passwd')
    if not result.failed:
        # Success
        puts(green('User project-owner exists.'))
        return

    puts(yellow('User project-owner does not exist.  Creating...'))
    sudo('useradd -r project-owner -s /bin/false')


def add_project_group():
    """
    Add a group that the www-data user (which Nginx, uWSGI, etc. run as) will be part of,
    and will have read-only access to the SkybirdOne files.
    """
    with settings(warn_only=True):
        result = sudo('grep project-group /etc/group')
    if not result.failed:
        # Success
        puts(green('Group project-group exists.'))
        return

    puts(yellow('Group project-group does not exist.  Creating...'))
    sudo('groupadd project-group')


def assign_correct_project_dir_permissions():
    """
    Defines a safe permissions / user policy for the SkybirdOne Django application.
    """

    # Shell-less user owns project files
    sudo('chown -R project-owner {}'.format(env.GIT_REPO_DIR))

    # Create group so that our services (Nginx, uWSGI, etc.) can read the project-owner-owned files.
    add_project_group()

    # Check that all of the files in the project are NOT group-writable.
    # sudo('find {} -type f -perm +20'.format(env.GIT_REPO_DIR))

    # Add www-data to project-group. Nginx and uWSGI run as www-data.
    sudo('usermod -a -G project-group www-data')

    # Set the sticky (1xxx) bit on the project directory. (To restrict deletion of files to root and the file owner.)
    sudo('chmod +t {}'.format(env.GIT_REPO_DIR))

    # Set the gid (2xxx) on the project directory so that all files and directories created in there have
    # project-group automatically in future.)
    sudo('chmod g+s {}'.format(env.GIT_REPO_DIR))


def configure_readonly_user():
    """
    Create the `readonly` user and configure directory structure
    and file ownership permissions.
    """

    with settings(warn_only=True):
        result = sudo('grep readonly /etc/passwd')
    if not result.failed:
        # Success
        puts(green('User readonly exists.'))
        return

    puts(yellow('User readonly does not exist.  Creating...'))

    sudo('useradd -c "bctech Readonly" -s /bin/bash -m readonly')  # , warn_only=True)
    append('/home/readonly/.bashrc', 'source /etc/bashrc', use_sudo=False)

    # Media location: prompts, msg_voicemail, msg_welcome
    # sudo('mkdir -p /home/logiport/trackman/media/')

    # So Django can upload media.
    sudo("chown -R www-data:readonly /home/baywest/")
    sudo("find /home/baywest/  -type d -exec chmod 750  '{}' \;")
    sudo("find /home/baywest/  -type f -exec chmod 640  '{}' \;")


def stop_nginx(force=False):
    sudo('systemctl stop nginx')


def start_nginx(force=False):
    sudo('systemctl start nginx')


def restart_nginx(force=False):
    sudo('systemctl restart nginx')


def restart_uwsgi():
    sudo('systemctl restart emperor.uwsgi.service')


def upgrade_pip():
    """
    Install the latest pip.
    """
    sudo('pip3 install -U pip')


def create_extensions(database, extensions):
    """
    Create Postgres extensions in the specified database.
    """
    for extension in extensions:
        su('postgres', 'psql -d {db} -c "CREATE EXTENSION IF NOT EXISTS {ext};"'.format(db=database, ext=extension))


def enable_swap(size):
    # Enable swap file on Linux Server, since most VPS providers
    # (Rackspace, Digital Ocean, etc.) do not enable this by default.

    ## Check state:
    # cat /proc/meminfo | grep MemTotal
    # swapon -s
    # df -h

    SWAPFILE_NAME = 'swapfile'
    SWAPFILE_DIR = '/'
    SWAPFILE_LOCATION = SWAPFILE_DIR + SWAPFILE_NAME

    print(yellow("Checking swap status..."))
    run('swapon -s')

    try:
        input('Press enter to assign {}G of swap, or Ctrl-C to cancel\n'.format(size))
    except KeyboardInterrupt:
        print('\nAction aborted.')
        exit(1)
    else:
        print(yellow('Assigning {} gigabytes of swap'.format(size)))

    run('fallocate -l {}G {}'.format(size, SWAPFILE_LOCATION))
    run('chmod 600 {}'.format(SWAPFILE_LOCATION))
    run('ls -lh {}'.format(SWAPFILE_LOCATION))
    run('mkswap {}'.format(SWAPFILE_LOCATION))
    run('swapon {}'.format(SWAPFILE_LOCATION))

    # Persist by appending to fstab (don't run this more that once).
    print("Appending to fstab")
    run('echo -e "\n{}   none    swap    defaults    0   0\n" >> /etc/fstab'.format(SWAPFILE_LOCATION))
    run('cat /etc/fstab')

    print(yellow('Resultant swap:'))
    run('swapon -s')


@contextmanager
def virtualenv(path):
    """Context manager that performs commands with an active virtualenv, eg:

    path is the path to the virtualenv to apply

    >>> with virtualenv(env):
            run('python foo')

    It is highly recommended to use an absolute path, as Fabric's with cd()
    feature is always applied BEFORE virtualenv(), regardless of how they are
    nested.

    """
    activate = posixpath.join(path, 'bin', 'activate')
    if not exists(activate):
        raise OSError("Cannot activate virtualenv %s" % path)
    with prefix('. %s' % activate):
        yield
