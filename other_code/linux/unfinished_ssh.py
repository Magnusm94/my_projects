import warnings

import paramiko
from Tools.ssh import connection_info


class ssh:

    def __init__(self, hostname=None):
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if hostname:
            try:
                info = connection_info.keys[hostname]
                conn.connect(hostname=info['ip'], username=info['username'],
                             password=info['password'], key_filename=info['key'])
                stdin, stdout, stderr = conn.exec_command('ls')
                print(stdout.readlines())
                conn.close()
            except KeyError:
                warnings.warn('Connection error')


