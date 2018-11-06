import click
import os
import requests
import json
import webbrowser

from gureumecli.cli.main import pass_context, common_options
from gureumecli.lib.utils.util import request, json_to_table


@click.command('describe', short_help='Displays details about app')
@click.argument('name')
@pass_context
def cli(ctx, name):
    """Display detailed information about the application."""
    apps = {}

    id_token = ctx.config.get('default', 'id_token')
    api_uri = ctx.config.get('default', 'api_uri')

    # Get app status
    url = api_uri + '/apps/' + name
    headers = {'Authorization': id_token}

    r = request('get', url, headers)
    apps = json.loads(r.text)
    apps = json.loads(apps['body'])

    click.secho("=== " + apps['name'], fg='blue')
    click.secho("Description: " + apps['description'])

    if 'endpoint' in apps:
        click.secho("Endpoint: " + apps['endpoint'], fg='green')
        webbrowser.open('http://' + apps['endpoint'], new=0, autoraise=True)