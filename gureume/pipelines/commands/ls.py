import click
import os
import requests
import json

from gureume.cli import pass_context
from gureume.lib.util import request, json_to_table


@click.command('ls', short_help='List your pipelines')
@pass_context
def cli(ctx):
    """List your pipelines in the platform."""
    id_token = ctx.config.get('default', 'id_token')
    api_uri = ctx.config.get('default', 'api_uri')

    url = api_uri + '/pipelines'
    headers = {'Authorization': id_token}

    r = request('get', url, headers)
    apps = json.loads(r.text)

    click.echo("=== Pipelines:")
    click.echo(json_to_table(apps))