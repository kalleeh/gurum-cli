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
