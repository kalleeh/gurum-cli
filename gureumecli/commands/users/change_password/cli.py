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

from gurumcli.cli.main import pass_context, common_options
from warrant import Cognito


@click.command('change-password', short_help='Change password for current user')
@click.option('--password', prompt=True, hide_input=True)
@click.option('--new-password', prompt=True, hide_input=True, confirmation_prompt=True)
@pass_context
def cli(ctx, password, new_password, confirm_password):
    """Change password."""
    user = ctx._config.get('default', 'user')
    click.echo('Changing password for {}...'.format(user), nl=True)

    id_token = ""
    refresh_token = ""
    access_token = ""
    id_token = ctx._config.get('default', 'id_token')
    refresh_token = ctx._config.get('default', 'refresh_token')
    access_token = ctx._config.get('default', 'access_token')

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
