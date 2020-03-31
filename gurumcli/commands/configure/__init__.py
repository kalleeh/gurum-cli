"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import logging
import click

from gurumcli.cli.main import pass_context, common_options
from gurumcommon.logger import configure_logger

LOGGER = configure_logger(__name__)

@click.command(context_settings=dict(help_option_names=[u'-h', u'--help']))
@common_options
@pass_context
def cli(ctx):
    """ \b
        Configure the default GURUM CLI profile.
        This will populate your configuration file with the required settings.

        You can add several profiles by adding the --profile argument and
        specify a new profile name.

    \b
    Common usage:

        \b
        Configures your CLI profile.
        \b
        $ gurum configure
        $ gurum configure --profile mysecondprofile
    """
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx)  # pragma: no cover


def do_cli(ctx):
    api_uri = click.prompt('API URI', default='https://api.gurum.cloud')
    region = click.prompt('API Region', default='eu-west-1')
    user_pool_id = click.prompt('Cognito User Pool ID')
    identity_pool_id = click.prompt('Cognito Identity Pool ID')
    identity_pool_id = identity_pool_id.rpartition(':')[2] # clean out eventual region and colon at start of string
    app_client_id = click.prompt('Cognito App Client ID')

    try:
        store_credentials_file(ctx, api_uri, region, user_pool_id, identity_pool_id, app_client_id)
    except Exception as ex:
        click.echo(ex)

def store_credentials_file(ctx, api_uri, region, user_pool_id, identity_pool_id, app_client_id):
    # Configure the config file with API URI and temporary credentials
    if not ctx.config.has_section(ctx.profile):
        ctx.config.add_section(ctx.profile)
    ctx.config.set(ctx.profile, 'api_uri', api_uri)
    ctx.config.set(ctx.profile, 'region', region)
    ctx.config.set(ctx.profile, 'cognito_user_pool_id', user_pool_id)
    ctx.config.set(ctx.profile, 'cognito_identity_pool_id', identity_pool_id)
    ctx.config.set(ctx.profile, 'cognito_app_client_id', app_client_id)
    with click.open_file(ctx.cfg_name, 'w+') as f:
        ctx.config.write(f)
