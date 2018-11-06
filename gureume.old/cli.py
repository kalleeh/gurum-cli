import os
import sys
import click
import configparser

from .apps.cli import apps
from .pipelines.cli import pipelines
from .users.cli import users
from .main.cli import main

CONTEXT_SETTINGS = dict(auto_envvar_prefix='GUREUME')


class Context(object):
    app_name = 'gureume'
    cfg_path = click.get_app_dir(app_name)
    """Reads config file"""
    if not os.path.exists(cfg_path):
        os.makedirs(cfg_path)
    cfg_name = os.path.join(cfg_path, '.gureume')
    if not os.path.exists(cfg_name):
        with open(cfg_name, 'a') as f:
            f.write(' \
                [default] \
                user = \
            ')

    config = configparser.ConfigParser()
    config.read(cfg_name)

    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_context = click.make_pass_decorator(Context, ensure=True)


@click.group()
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')
@pass_context
def cli(ctx, verbose):
    ctx.verbose = verbose

cli.add_command(apps)
cli.add_command(pipelines)
cli.add_command(users)
cli = click.CommandCollection(sources=[cli, main])

# If Frozen
if getattr(sys, 'frozen', False):
    cli(sys.argv[1:])