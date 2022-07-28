import click

from gurumcli.cli.main import pass_context
from gurumcli.libs.formatter import json_to_table
from gurumcommon.clients.api_client import ApiClient


@click.command('ls', short_help='List your services')
@pass_context
def cli(ctx):
    """List your services in the platform."""
    api_client = ApiClient(
        api_uri=ctx.config.get(ctx.profile, 'api_uri'),
        id_token=ctx.config.get(ctx.profile, 'id_token')
    )

    resp = api_client.services.list()
    services = resp['services']

    click.echo("=== Services:")
    click.echo(json_to_table(services))
