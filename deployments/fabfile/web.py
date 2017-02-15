"""
Task to Configure Nginx on server
"""
from os.path import join

from fabric.api import env, execute, puts, run, sudo
from fabric.colors import green, red, yellow
from fabric.contrib.files import exists
from fabric.tasks import Task

import tools


class NginxBasic(Task):
    """
    Install Nginx.
    """
    name = 'NginxBasic'
    DEBS = (
        'nginx',
        'nginx-full'
    )

    def run(self):
        tools.apt_get_install(self.DEBS)
        # Install Nginx config file
        sudo('install -v -m 644 {} /etc/nginx/'.format(
            join(env.ETC_DIR, 'nginx/nginx.conf')))

        sudo('install -v -m 644 {} /etc/nginx/'.format(
            join(env.ETC_DIR, 'nginx/nginx.conf')))

        # Replace INSERT_HOST_HERE instaces with host name
        tools.sed_replace(tools.NGINX_PLACEHOLDER, env.host, join('/etc', 'nginx', '*.conf'))

        # Install uWSGI file
        sudo('mkdir -p /etc/uwsgi/init/')
        sudo('install -v -m 644 {} /etc/uwsgi/init/'.format(
            join(env.ETC_DIR, 'uwsgi', 'kando.json')))

        # Install uWSGI upstart file
        sudo('install -v -m 644 {} /etc/systemd/system/'.format(
            join(env.ETC_DIR, 'uwsgi/emperor.uwsgi.service')))

        tools.restart_nginx()
        tools.restart_uwsgi()


class NginxFull(Task):
    """
    Install Nginx and secure with LetsEncrypt.
    """
    name = 'NginxFull'

    def run(self):
        execute(NginxBasic())

        # Check if certificate files are present then skip copying over
        # Nginx unsecure configuration. Always define this inside a function, or
        # env.host will be `None`.
        CERT_FILE = '/etc/letsencrypt/live/{}/cert.pem'.format(env.host)
        print "CERT FILE", CERT_FILE
        if not exists(CERT_FILE):
            # Installs SSL certs with Let's Encrypt and reconfigures Nginx.
            tools.install_letsencrypt()

            puts(yellow('Copying cron to refresh certificate.'))
            run('install -v -m 644 {} /etc/cron.d/'.format(join(env.ETC_DIR, 'cron.d', 'ssl_cert_renewal')))

        else:
            # Print out expiration date of SSL Certificates
            puts(red('Certificate exists: skipping certificate creation'))
            run('echo | openssl s_client -connect {}:443 2>/dev/null | openssl x509 -noout -dates'.format(env.host))

        # Upload real Nginx configs
        puts(yellow('Installing secure Nginx configs.'))
        run('install -v -m 644 {} /etc/nginx/'.format(join(env.ETC_DIR, 'nginx', 'special-*')))
        run('install -v -m 644 {} /etc/nginx/'.format(join(env.ETC_DIR, 'nginx', 'ssl.conf')))
        run('install -v -m 644 {} /etc/nginx/'.format(join(env.ETC_DIR, 'nginx', 'nginx.conf')))

        # Replace INSERT_HOST_HERE instaces with host name
        tools.sed_replace(tools.NGINX_PLACEHOLDER, env.host, join('/etc', 'nginx', '*.conf'))
        tools.restart_nginx()
