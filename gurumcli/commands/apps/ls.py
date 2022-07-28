import click

from gurumcli.cli.main import pass_context, common_options
from gurumcli.libs.formatter import json_to_table
from gurumcommon.clients.api_client import ApiClient


@click.command('ls', short_help='List your apps')
@pass_context
@common_options
def cli(ctx):
    """ \b
        Lists your applications in the platform.

    \b
    Common usage:

        \b
        Logs in to the platform.
        \b
        $ gurum login
    """
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx)  # pragma: no cover


def do_cli(ctx):
    """List your apps in the platform."""
    api_client = ApiClient(
        api_uri=ctx.config.get(ctx.profile, 'api_uri'),
        id_token=ctx.config.get(ctx.profile, 'id_token')
    )

    resp = api_client.apps.list()
    apps = resp['apps']

    click.echo("=== Apps:")
    click.echo(json_to_table(apps))
