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


@click.command('reset-password', short_help='Initiate forgot password for a user')
@click.option('--user', prompt=True, help='Username (email)')
@click.option('--confirmation-code', prompt=True, help='Confirmation Code')
@pass_context
def cli(ctx, user, confirmation_code):
    """Confirm user signup."""
    click.echo('Initiating forgot password process for {}...'.format(user), nl=True)

    user_pool_id = ctx.config.get(ctx.profile, 'cognito_user_pool_id')
    app_client_id = ctx.config.get(ctx.profile, 'cognito_app_client_id')

    u = Cognito(
        user_pool_id,
        app_client_id,
        username=user)

    try:
        u.confirm_sign_up(confirmation_code, username=user)
        click.echo('Successfully confirmed signup.')
    except Exception as ex:
        click.echo(ex)
