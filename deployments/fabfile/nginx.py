"""
Task to Configure Nginx on server
"""
from os.path import join, sep

from fabric.api import env, puts, run
from fabric.colors import green, red, yellow
from fabric.contrib.files import exists
from fabric.tasks import Task
from fabric.operations import sudo

import tools


class Nginx(Task):
    """
    Install Nginx on server
    """
    name = 'Install Nginx'

    nginx_dir = join(sep, 'etc', 'nginx')
    sites_available = join(env.OPS_ETC_DIR, 'nginx', 'sites-available')
    nginx_sites_available = join(nginx_dir, 'sites-available')
    ops_nginx_dir = join(env.OPS_ETC_DIR, 'nginx')
    insecure_nginx_config = join(ops_nginx_dir, 'insecure_nginx.conf')
    nginx_config = join(ops_nginx_dir, 'nginx.conf')
    secure_nginx_config = join(sites_available, 'serthe')
    ssl_dir = join(nginx_dir, 'ssl')
    ssl_config = join(ops_nginx_dir, 'ssl', 'winecellar-ssl.conf')
    cron_file = join(env.REPO_DIR, 'deployments', 'ubuntu', 'etc', 'cron.d', '*_ssl_cert_renewal')
    cron_config_path = join(sep, 'etc', 'cron.d')

    def run(self):
        cert_file = join(sep, 'etc', 'letsencrypt', 'live', env.DOMAINS, 'cert.pem')

        #Check if certificate files are present then skip copying over
        #nginx unsecure configuration
        if exists(cert_file, use_sudo=True):
            # Print out expiration date of SSL Certificates
            puts(red('Certificate exists: skipping certificate creation'))
            sudo('echo | openssl s_client -connect {}:443 2>/dev/null | openssl x509'
                ' -in {} -noout -dates'.format(env.DOMAINS, cert_file))
            puts(green('Cert file doesn\'t exist. Creating one.'))
        else:
            puts(yellow('Installing insecure intermediate Nginx config'))
            sudo('cp {} {}'.format(self.insecure_nginx_config, join(self.nginx_dir, 'nginx.conf')))

            # Replace INSERT_HOST_HERE instaces with host name
            tools.sed_replace('INSERT_HOST_HERE', env.DOMAINS, join(self.nginx_dir, 'nginx.conf'))

            sudo('nginx -t')
            sudo('service nginx restart')

            # Does a lot. Installs SSL certs with Let's Encrypt and reconfigures Nginx.
            puts(yellow('Starting Let\'s Encrypt install.'))
            tools.install_letsencrypt()

            puts(yellow('Copying cron to refresh certificate.'))
            sudo('cp {} {}'.format(self.cron_file, self.cron_config_path))


        # Upload real Nginx configs
        puts(yellow('Installing secure Nginx configs.'))
        sudo('cp {} {}'.format(self.ssl_config, self.ssl_dir))
        sudo('cp {} {}'.format(self.nginx_config, self.nginx_dir))
        sudo('cp {} {}'.format(self.secure_nginx_config, self.nginx_sites_available))

        sudo('nginx -t')
        sudo('service nginx restart')
