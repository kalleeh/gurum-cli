import click
import click_spinner
import os
import requests
import json
import time

from gureumecli.cli.main import pass_context, common_options
from gureumecli.lib.utils.util import request, json_to_table, prettyprint, prettyprint, haikunate


@click.command('create', short_help='Create a new service')
@click.option('--name', prompt=True, default=haikunate(), help='Name of the service')
@click.option('--service-type', type=click.Choice(['s3', 'dynamodb']), prompt=True, help="The type of backing service")
@click.option('--service-bindings', prompt=True, required=True, help="Comma-separated string of applications to bind the service to")
@click.option('--service-version', prompt=False, required=False, help="Add a test stage to the service")
@pass_context
def cli(ctx, **kwargs):
    """Create a new service."""
    id_token = ""
    services = {}

    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

    url = api_uri + '/services'
    headers = {'Authorization': id_token}
    
    # Dynamically get options and remove undefined options
    payload = json.dumps({k: v for k, v in kwargs.items() if v is not None})

    r = request('post', url, headers, payload)
    services = json.loads(r['body'])

    # Start a loop that checks for stack creation status
    with click_spinner.spinner():
        while True:
            # Update creation status
            url = api_uri + '/services/' + kwargs['name']
            headers = {'Authorization': id_token}

            r = request('get', url, headers)
            services = json.loads(r['body'])

            # Get CloudFormation Events
            url = api_uri + '/events/' + kwargs['name']

            r = request('get', url, headers)
            events = json.loads(r['body'])

            prettyprint(services)
            click.echo(json_to_table(events))

            click.echo('Working on: {}'.format(kwargs['name']))
            click.echo('This usually takes a couple of minutes...')
            click.echo('This call is asynchrounous so feel free to Ctrl+C ' \
                        'anytime and it will continue running in background.')

            if services['status'] == 'CREATE_COMPLETE':
                break

            # refresh every 5 seconds
            time.sleep(5)
