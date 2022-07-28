import click

from gurumcli.cli.main import pass_context
from gurumcli.libs.formatter import json_to_table
from gurumcommon.clients.api_client import ApiClient

@click.command('put-approval', short_help='Displays status about your pipeline')
@click.argument('name')
@click.option('--status', prompt=True, type=click.Choice(['Approved', 'Rejected']), help="String giving the Approved or Rejected status")
@click.option('--summary', prompt=True, help="Approve update message.")
@pass_context
def cli(ctx, name, status, summary):
    """Approve or reject an application deployment."""
    api_client = ApiClient(
        api_uri=ctx.config.get(ctx.profile, 'api_uri'),
        id_token=ctx.config.get(ctx.profile, 'id_token')
    )
    states = []

    resp = api_client.pipelines.put_approval(name, status, summary)
    states = resp['states']

    click.secho("=== " + name + ' status', fg='blue')

    click.echo(json_to_table(states))
