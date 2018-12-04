import click
import click_spinner
import os
import requests
import json
import time

from gureumecli.cli.main import pass_context, common_options
from gureumecli.lib.utils.util import request, json_to_table


@click.command('update', short_help='Update the service')
@click.argument('name')
@click.option('--app-name', prompt=True, help="App to link service to")
@click.option('--app-dev', prompt=False, required=False, help="Add a development stage to the service")
@click.option('--app-test', prompt=False, required=False, help="Add a test stage to the service")
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
        services = json.loads(r.text)
        services = json.loads(services['body'])
    except Exception:
        pass
    else:
        # Start a loop that checks for stack creation status
        with click_spinner.spinner():
            while True:
                # Update creation status
                url = api_uri + '/services/' + name

                r = request('get', url, headers)
                services = json.loads(r.text)
                services = json.loads(services['body'])

                # Get CloudFormation Events
                url = api_uri + '/events/' + name

                r = request('get', url, headers)
                events = json.loads(r.text)
                events = json.loads(events['body'])

                click.clear()
                
                click.secho("=== " + services['name'], fg='blue')
                click.secho("Description: " + services['description'])

                # print status yellow if in progress, completed is green
                if(services['status'].endswith('_IN_PROGRESS')):
                    click.secho("Status: " + services['status'], fg='yellow')
                elif(services['status'].endswith('_COMPLETE')):
                    click.secho("Status: " + services['status'], fg='green')
                else:
                    click.secho("Status: " + services['status'], fg='red')

                if 'endpoint' in services:
                    click.secho("Endpoint: " + services['endpoint'], fg='green')
                if 'repository' in services:
                    click.secho("Repository: " + services['repository'], fg='green')

                # iterate over and print tags
                click.secho("Tags: ")
                for key, val in services['tags'].items():
                    click.secho("- {}: {}".format(key, val))

                click.echo(json_to_table(events))

                click.echo('Working on: {}'.format(name))
                click.echo('This usually takes a couple of minutes...')
                click.echo('This call is asynchrounous so feel free to Ctrl+C ' \
                            'anytime and it will continue running in background.')

                if services['status'].endswith('_COMPLETE'):
                    break

                # refresh every 5 seconds
                time.sleep(5)
