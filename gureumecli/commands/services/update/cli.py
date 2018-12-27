import click
import click_spinner
import os
import requests
import json
import time

from gureumecli.cli.main import pass_context, common_options
from gureumecli.lib.utils.util import request, json_to_table, prettyprint


@click.command('update', short_help='Update the service')
@click.argument('name')
@click.option('--service-bindings', prompt=True, required=True, help="Comma-separated string of applications to bind the service to")
@pass_context
def cli(ctx, name, **kwargs):
    """Update service configuration."""
    id_token = ""
    services = {}

    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

    url = api_uri + '/services/' + name
    headers = {'Authorization': id_token}

    # Dynamically get options and remove undefined options
    payload = json.dumps({k: v for k, v in kwargs.items() if v is not None})

    try:
        r = request('patch', url, headers, payload)
        services = json.loads(r['body'])
    except Exception:
        pass
    else:
        # Start a loop that checks for stack creation status
        with click_spinner.spinner():
            while True:
                # Update creation status
                url = api_uri + '/services/' + name

                r = request('get', url, headers)
                services = json.loads(r['body'])

                # Get CloudFormation Events
                url = api_uri + '/events/' + name

                r = request('get', url, headers)
                events = json.loads(r['body'])

                click.clear()
                prettyprint(services)
                click.echo(json_to_table(events))

                click.echo('Working on: {}'.format(name))
                click.echo('This usually takes a couple of minutes...')
                click.echo('This call is asynchrounous so feel free to Ctrl+C ' \
                            'anytime and it will continue running in background.')

                if services['status'].endswith('_COMPLETE'):
                    break

                # refresh every 5 seconds
                time.sleep(5)
