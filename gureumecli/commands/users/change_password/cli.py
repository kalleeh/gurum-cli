import click
import os
import requests

from gureumecli.cli.main import pass_context, common_options
from warrant import Cognito


@click.command('change-password', short_help='Change password for current user')
@click.option('--password', prompt=True, hide_input=True)
@click.option('--new-password', prompt=True, hide_input=True, confirmation_prompt=True)
@pass_context
def cli(ctx, password, new_password, confirm_password):
    """Change password."""
    user = ctx.config.get('default', 'user')
    click.echo('Changing password for {}...'.format(user), nl=True)

    id_token = ""
    refresh_token = ""
    access_token = ""
    id_token = ctx.config.get('default', 'id_token')
    refresh_token = ctx.config.get('default', 'refresh_token')
    access_token = ctx.config.get('default', 'access_token')

    u = Cognito(
        'eu-west-1_MkM8NwiuN',
        '1ts0lglioorltjrs0j3k3bniv5',
        username=user,
        id_token=id_token,
        refresh_token=refresh_token,
        access_token=access_token)

    try:
        u.change_password(password, new_password)
        click.echo('Successfully updated password.')
    except Exception as ex:
        click.echo(ex)
