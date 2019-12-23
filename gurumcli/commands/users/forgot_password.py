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


@click.command('forgot-password', short_help='Initiate forgot password for a user')
@click.option('--user', prompt=True, help='Username (email)')
@pass_context
def cli(ctx, user):
    """Initiates a forgot password."""
    click.echo('Initiating forgot password process for {}...'.format(user), nl=True)

    user_pool_id = ctx.config.get(ctx.profile, 'cognito_user_pool_id')
    app_client_id = ctx.config.get(ctx.profile, 'cognito_app_client_id')

    u = Cognito(
        user_pool_id,
        app_client_id,
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
