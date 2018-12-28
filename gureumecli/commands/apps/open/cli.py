import click
import os
import requests
import json
import webbrowser

from gureumecli.cli.main import pass_context, common_options
from gureumecli.lib.utils.util import request, json_to_table, prettyprint


@click.command('open', short_help='Opens the app endpoint')
@click.argument('name')
@pass_context
@common_options
def cli(ctx, name):
    """ \b
        Open the application.

    \b
    Common usage:

        \b
        Fetches the application endpoint and opens it in a browser.
        \b
        $ gureume apps open myApp
    """
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx, name)  # pragma: no cover


def do_cli(ctx, name):
    """Open the application."""
    apps = {}

    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

    # Get app status
    url = api_uri + '/apps/' + name
    headers = {'Authorization': id_token}

    r = request('get', url, headers)
    apps = json.loads(r['body'])

    click.secho("=== " + apps['name'], fg='blue')
    click.secho("Description: " + apps['description'])

    if 'Endpoint' in apps['outputs']:
        click.secho("Endpoint: " + apps['outputs']['Endpoint'], fg='green')
        webbrowser.open('http://' + apps['outputs']['Endpoint'], new=0, autoraise=True)