import ipaddress
import re
from sshkey import PublicKey
import click as c


rx_user = re.compile(r'[a-zA-Z0-9]+')


def check_params(option, value):

    if value == 'None':
        value = __request(option)

    if option == 'user':
        while not re.match(rx_user, value):
            c.secho(r"[-u] User isn't valid", fg='red')
            value = __request(option)

    if option == 'key':
        while not PublicKey(value).key_valid:
            c.secho(r"[-k] RSA public key isn't valid", fg='red')
            value = __request(option)
        value = PublicKey(value).convert_to_openssh()

    if option == 'target':
        while True:
            try:
                ipaddress.ip_network(value)
            except ValueError:
                c.secho(r'[-t] TARGET is not IP-address\network', fg='red')
                value = __request(option)
            break

    if option == 'login':
        while not re.match(rx_user, value):
            c.secho(r"[-l] Login isn't valid", fg='red')
            value = __request(option)

    return value


def __request(option):
    value = ''
    if option == 'user':
        value = c.prompt('Enter new user')

    if option == 'key':
        c.secho('Enter/Paste ssh public key for new user. Ctrl-D or Ctrl-Z ( windows ) to save it.')
        while True:
            try:
                line = input()
            except EOFError:
                break
            value += line

    if option == 'target':
        value = c.prompt(r'Enter target host\network')

    if option == 'login':
        value = c.prompt('Enter login for authentication')

    if option == 'password':
        value = c.prompt('Enter password for authentication')

    return value
