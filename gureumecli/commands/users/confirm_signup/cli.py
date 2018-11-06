import click
import os
import requests

from gureumecli.cli.main import pass_context, common_options
from warrant import Cognito


@click.command('reset-password', short_help='Initiate forgot password for a user')
@click.option('--user', prompt=True, help='Username (email)')
@click.option('--confirmation-code', prompt=True, help='Confirmation Code')
@pass_context
def cli(ctx, user, confirmation_code):
    """Confirm user signup."""
    click.echo('Initiating forgot password process for {}...'.format(user), nl=True)

    u = Cognito(
        'eu-west-1_MkM8NwiuN',
        '1ts0lglioorltjrs0j3k3bniv5',
        username=user)

    try:
        u.confirm_sign_up(confirmation_code, username=user)
        click.echo('Successfully confirmed signup.')
    except Exception as ex:
        click.echo(ex)
