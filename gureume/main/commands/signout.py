import click
import os
import requests

from gureume.cli import pass_context
from warrant import Cognito


@click.command('signout', short_help='Log out of the platform')
@pass_context
def cli(ctx):
    """Authenticates to the platform to access your apps."""
    user = ctx.config.get('default', 'user')
    id_token = ctx.config.get('default', 'id_token')
    refresh_token = ctx.config.get('default', 'refresh_token')
    access_token = ctx.config.get('default', 'access_token')

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
    if not ctx.config.has_section('default'):
        ctx.config.add_section('default')
    if not ctx.config.has_option('default', 'api_uri'):
        ctx.config.set('default', 'api_uri', 'https://api.gureu.me')
    ctx.config.set('default', 'user', '')
    ctx.config.set('default', 'access_token', '')
    cfgfile = open(ctx.cfg_name, 'w+')
    ctx.config.write(cfgfile)
    cfgfile.close()
