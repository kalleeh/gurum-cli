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
    user_pool_id = ctx.config.get(ctx.profile, 'cognito_user_pool_id')
    app_client_id = ctx.config.get(ctx.profile, 'cognito_app_client_id')

    user = ctx.config.get(ctx.profile, 'user')
    id_token = ctx.config.get(ctx.profile, 'id_token')
    refresh_token = ctx.config.get(ctx.profile, 'refresh_token')
    access_token = ctx.config.get(ctx.profile, 'access_token')

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
    if not ctx.config.has_section('default'):
        ctx.config.add_section('default')
    if not ctx.config.has_option('default', 'api_uri'):
        ctx.config.set('default', 'api_uri', 'https://api.gurum.cloud')
    ctx.config.set('default', 'user', '')
    ctx.config.set('default', 'access_token', '')
    cfgfile = open(ctx.cfg_name, 'w+')
    ctx.config.write(cfgfile)
    cfgfile.close()
