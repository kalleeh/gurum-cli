import click
import click_spinner
import os
import requests
import json
import time

from gureumecli.cli.main import pass_context, common_options
from gureumecli.lib.utils.util import request, json_to_table, prettyprint


@click.command('update', short_help='Update the app')
@click.argument('name')
@click.option('--tasks', prompt=False, help='Number of tasks to run')
@click.option('--health-check-path', prompt=False, help='Path that is queried for health checks')
@click.option('--image', prompt=False, help='Docker image to run')
@pass_context
def cli(ctx, name, **kwargs):
    """Create a new application."""
    id_token = ""
    apps = {}

    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

    url = api_uri + '/apps/' + name
    headers = {'Authorization': id_token}

    # Dynamically get options and remove undefined options
    payload = json.dumps({k: v for k, v in kwargs.items() if v is not None})

    r = request('patch', url, headers, payload)
    apps = json.loads(r['body'])
    
    # Start a loop that checks for stack creation status
    with click_spinner.spinner():
        while True:
            # Update creation status
            url = api_uri + '/apps/' + name
            
            r = request('get', url, headers)
            apps = json.loads(r.text)
            apps = json.loads(r['body'])

            # Get CloudFormation Events
            url = api_uri + '/events/' + name

            r = request('get', url, headers)
            events = json.loads(r['body'])

            click.clear()
            prettyprint(apps)
            click.echo(json_to_table(events))

            click.echo('Working on: {}'.format(name))
            click.echo('This usually takes a couple of minutes...')
            click.echo('This call is asynchrounous so feel free to Ctrl+C ' \
                        'anytime and it will continue running in background.')

            # Stop loop if task is complete
            if apps['status'].endswith('_COMPLETE'):
                break

            # refresh every 5 seconds
            time.sleep(5)