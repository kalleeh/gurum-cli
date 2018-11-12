"""
CLI command for "logout" command
"""

import click
import os
import requests

from gureumecli.cli.main import pass_context, common_options
from warrant import Cognito

SHORT_HELP = "Log out from the GUREUME platform."


@click.command("logout", short_help=SHORT_HELP, context_settings={"ignore_unknown_options": True})
@common_options
@pass_context
def cli(ctx, args):

    # All logic must be implemented in the ``do_cli`` method. This helps with easy unit testing

    do_cli(ctx, args)  # pragma: no cover


def do_cli(ctx, args):
    """Authenticates to the platform to access your apps."""
    user = ctx._config.get('default', 'user')
    id_token = ctx._config.get('default', 'id_token')
    refresh_token = ctx._config.get('default', 'refresh_token')
    access_token = ctx._config.get('default', 'access_token')

    click.echo('Signing out {}...'.format(user), nl=True)

    u = Cognito(
        'eu-west-1_MkM8NwiuN',
        '1ts0lglioorltjrs0j3k3bniv5',
        id_token=id_token,
        refresh_token=refresh_token,
        access_token=access_token)

    try:
        u.logout
        click.echo('Signed out!')
    except Exception as ex:
        click.echo(ex)

    # Configure the config file with API URI and temporary credentials
    if not ctx._config.has_section('default'):
        ctx._config.add_section('default')
    if not ctx._config.has_option('default', 'api_uri'):
        ctx._config.set('default', 'api_uri', 'https://api.gureu.me')
    ctx._config.set('default', 'user', '')
    ctx._config.set('default', 'access_token', '')
    cfgfile = open(ctx.cfg_name, 'w+')
    ctx._config.write(cfgfile)
    cfgfile.close()