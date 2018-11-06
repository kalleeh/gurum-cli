import click
import os
import requests
import json

from gureumecli.cli.main import pass_context, common_options
from gureumecli.lib.utils.util import request, json_to_table


@click.command('ls', short_help='List your apps')
@pass_context
def cli(ctx):
    """List your apps in the platform."""
    id_token = ctx.config.get('default', 'id_token')
    api_uri = ctx.config.get('default', 'api_uri')

    url = api_uri + '/apps'
    headers = {'Authorization': id_token}

    r = request('get', url, headers)
    apps = json.loads(r.text)
    apps = json.loads(apps['body'])

    click.echo("=== Apps:")
    click.echo(json_to_table(apps))
