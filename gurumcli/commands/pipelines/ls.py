import click

from gurumcli.cli.main import pass_context
from gurumcli.libs.formatter import json_to_table
from gurumcommon.clients.api_client import ApiClient


@click.command('ls', short_help='List your pipelines')
@pass_context
def cli(ctx):
    """List your pipelines in the platform."""
    api_client = ApiClient(
        api_uri=ctx.config.get(ctx.profile, 'api_uri'),
        id_token=ctx.config.get(ctx.profile, 'id_token')
    )

    resp = api_client.pipelines.list()
    pipelines = resp['pipelines']

    click.echo("=== Pipelines:")
    click.echo(json_to_table(pipelines))
