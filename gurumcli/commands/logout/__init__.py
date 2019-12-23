"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import os
import click
import requests
from warrant import Cognito

from gurumcli.cli.main import pass_context, common_options

SHORT_HELP = "Log out from the GURUM platform."


@click.command("logout", short_help=SHORT_HELP, context_settings={"ignore_unknown_options": True})
@common_options
@pass_context
def cli(ctx):

    # All logic must be implemented in the ``do_cli`` method. This helps with easy unit testing

    do_cli(ctx)  # pragma: no cover


def do_cli(ctx):
    """Logs the user out from the platform."""
    user_pool_id = ctx.cfg.get('default', 'cognito_user_pool_id')
    app_client_id = ctx.cfg.get('default', 'cognito_app_client_id')

    user = ctx.cfg.get('default', 'user')
    id_token = ctx.cfg.get('default', 'id_token')
    refresh_token = ctx.cfg.get('default', 'refresh_token')
    access_token = ctx.cfg.get('default', 'access_token')

    click.echo('Signing out {}...'.format(user), nl=True)

    u = Cognito(
        user_pool_id,
        app_client_id,
        id_token=id_token,
        refresh_token=refresh_token,
        access_token=access_token)

    try:
        u.logout()
        click.echo('Signed out!')
    except Exception as ex:
        click.echo(ex)

    # Configure the config file with API URI and temporary credentials
    if not ctx.cfg.has_section('default'):
        ctx.cfg.add_section('default')
    if not ctx.cfg.has_option('default', 'api_uri'):
        ctx.cfg.set('default', 'api_uri', 'https://api.gurum.cloud')
    ctx.cfg.set('default', 'user', '')
    ctx.cfg.set('default', 'access_token', '')
    cfgfile = open(ctx.cfg_name, 'w+')
    ctx.cfg.write(cfgfile)
    cfgfile.close()
