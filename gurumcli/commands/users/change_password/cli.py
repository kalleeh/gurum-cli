"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import click
from warrant import Cognito

from gurumcli.cli.main import pass_context


@click.command('change-password', short_help='Change password for current user')
@click.option('--password', prompt=True, hide_input=True)
@click.option('--new-password', prompt=True, hide_input=True, confirmation_prompt=True)
@pass_context
def cli(ctx, password, new_password, confirm_password, profile='default'):
    """Change password."""
    user = ctx.config.get('default', 'user')
    click.echo('Changing password for {}...'.format(user), nl=True)

    id_token = ""
    refresh_token = ""
    access_token = ""
    id_token = ctx.config.get('default', 'id_token')
    refresh_token = ctx.config.get('default', 'refresh_token')
    access_token = ctx.config.get('default', 'access_token')

    user_pool_id = ctx.config.get(profile, 'cognito_user_pool_id')
    app_client_id = ctx.config.get(profile, 'cognito_app_client_id')

    u = Cognito(
        user_pool_id,
        app_client_id,
        username=user,
        id_token=id_token,
        refresh_token=refresh_token,
        access_token=access_token)

    try:
        u.change_password(password, new_password)
        click.echo('Successfully updated password.')
    except Exception as ex:
        click.echo(ex)
