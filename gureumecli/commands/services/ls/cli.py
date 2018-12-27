import click
import os
import requests
import json

from gureumecli.cli.main import pass_context, common_options
from gureumecli.lib.utils.util import request, json_to_table, prettyprint


@click.command('ls', short_help='List your services')
@pass_context
def cli(ctx):
    """List your services in the platform."""
    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

    url = api_uri + '/services'
    headers = {'Authorization': id_token}

    r = request('get', url, headers)
    services = json.loads(r['body'])

    click.echo("=== Services:")
    click.echo(json_to_table(services))