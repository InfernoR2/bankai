import logging
import ipaddress
import subprocess


class Bankai(object):
    def __init__(self, params):
        self.params = params

    def add_user(self):
        pass

    def ping(self):
        self.__init_ping()
        for host in self.hosts:
            unreachable = subprocess.call(f'ping {host} -n 1', stdout=subprocess.DEVNULL)
            if not unreachable:
                logging.info(f'{host} is available')
            if unreachable:
                logging.info(f'{host} unreachable')

    def __init_ping(self):
        self.hosts = ipaddress.ip_network(self.params['target'])