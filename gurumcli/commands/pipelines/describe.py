import click

from gurumcli.cli.main import pass_context
from gurumcli.libs.formatter import json_to_table, prettyprint
from gurumcommon.clients.api_client import ApiClient


@click.command('describe', short_help='Displays details about pipeline')
@click.argument('name')
@pass_context
def cli(ctx, name):
    """Display detailed information about the application."""
    pipelines = {}
    payload = {}
    payload['name'] = name

    api_client = ApiClient(
        api_uri=ctx.config.get(ctx.profile, 'api_uri'),
        id_token=ctx.config.get(ctx.profile, 'id_token')
    )

    resp = api_client.pipelines.describe(name)
    pipelines = resp['pipelines'][0]

    resp = api_client.events.list(name)
    events = resp['events']

    prettyprint(pipelines)
    click.echo(json_to_table(events))
