"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import click
import os
import requests

from gureumecli.cli.main import pass_context, common_options
from warrant import Cognito


@click.command('forgot-password', short_help='Initiate forgot password for a user')
@click.option('--user', prompt=True, help='Username (email)')
@pass_context
def cli(ctx, user):
    """Initiates a forgot password."""
    click.echo('Initiating forgot password process for {}...'.format(user), nl=True)

    u = Cognito(
        'eu-west-1_MkM8NwiuN',
        '1ts0lglioorltjrs0j3k3bniv5',
        username=user)

    try:
        u.initiate_forgot_password()
        click.echo('Successful. Check your inbox for confirmation code.')
    except Exception as ex:
        click.echo(ex)

    confirmation_code = click.prompt('Confirmation Code')
    new_password = click.prompt('New Password', hide_input=True)

    try:
        u.confirm_forgot_password(confirmation_code, new_password)
        click.echo('Successfully set new password. Please login.')
    except Exception as ex:
        click.echo(ex)
