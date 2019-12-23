"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import json
import webbrowser
import click

from gurumcli.cli.main import pass_context, common_options
from gurumcommon.clients.api_client import ApiClient


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
        $ gurum apps open myApp
    """
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx, name)  # pragma: no cover


def do_cli(ctx, name):
    """Open the application."""
    apps = {}
    payload = {}
    payload['name'] = name

    api_client = ApiClient(
        api_uri=ctx.config.get('default', 'api_uri'),
        id_token=ctx.config.get('default', 'id_token')
    )

    resp = api_client.describe(resource='apps', payload=json.dumps(payload))
    apps = resp['apps'][0]

    click.secho("=== " + apps['name'], fg='blue')
    click.secho("Description: " + apps['description'])

    if 'Endpoint' in apps['outputs']:
        click.secho("Endpoint: " + apps['outputs']['Endpoint'], fg='green')
        webbrowser.open('https://' + apps['outputs']['Endpoint'], new=0, autoraise=True)
