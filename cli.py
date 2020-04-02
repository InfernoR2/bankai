
import click as c
from bankai import Bankai
import validate


@c.group()
def cli():
    pass


@c.command('add-user', help='Command to add a new user')
@c.option('--user', '-u', help='New user')
@c.option('--key', '-k', help='ssh public key for new user')
@c.option('--target', '-t', help=r'Target host\network')
@c.option('--login', '-l', help='Authentication login')
@c.option('--password', '-p', help='Authentication password')
def add_user(user, key, target, login, password):
    params = {'user': f'{user}',
              'key': f'{key}',
              'target': f'{target}',
              'login': f'{login}',
              'password': f'{password}'}

    for option, value in params.items():
        params[option] = validate.check_params(option, value)

    c.clear()
    for option, value in params.items():
        if option == 'password':
            continue
        c.secho(f'{option}: ', fg='white', bold=True, nl=False)
        c.secho(f'{value}', fg='green')

    c.confirm('Are you ready?', abort=True)

    ba = Bankai(params)
    ba.add_user()

    c.echo('Done')
    c.pause()


@c.command('ping', help='Command ping device')
@c.option('--target', '-t', help=r'Target host\network')
def ping(target):
    params = {'target': f'{target}'}
    for option, value in params.items():
        params[option] = validate.check_params(option, value)

    ba = Bankai(params)
    ba.ping()

    c.pause()

cli.add_command(add_user)
cli.add_command(ping)
