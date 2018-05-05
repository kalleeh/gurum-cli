import click
import click_spinner
import os
import requests
import json
import time

from gureume.cli import pass_context
from gureume.lib.util import request, json_to_table


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

    id_token = ctx.config.get('default', 'id_token')
    api_uri = ctx.config.get('default', 'api_uri')

    url = api_uri + '/apps/' + name
    headers = {'Authorization': id_token}

    # Dynamically get options and remove undefined options
    payload = json.dumps({k: v for k, v in kwargs.items() if v is not None})
    
    try:
        r = request('patch', url, headers, payload)
        apps = json.loads(r.text)
    except Exception:
        pass
    else:
        # Start a loop that checks for stack creation status
        with click_spinner.spinner():
            while True:
                # Update creation status
                url = api_uri + '/apps/' + name

                r = request('get', url, headers)
                apps = json.loads(r.text)

                # Get CloudFormation Events
                url = api_uri + '/events/' + name

                r = request('get', url, headers)
                events = json.loads(r.text)

                click.clear()

                click.secho("=== " + apps['name'], fg='yellow')
                click.secho("Description: " + apps['description'])

                # print status yellow if in progress, completed is green
                if(apps['status'].endswith('_IN_PROGRESS')):
                    click.secho("Status: " + apps['status'], fg='yellow')
                elif(apps['status'].endswith('_COMPLETE')):
                    click.secho("Status: " + apps['status'], fg='green')
                else:
                    click.secho("Status: " + apps['status'], fg='red')

                if 'endpoint' in apps:
                    click.secho("Endpoint: " + apps['endpoint'], fg='yellow')
                if 'repository' in apps:
                    click.secho("Repository: " + apps['repository'], fg='yellow')

                # iterate over and print tags
                click.secho("Tags: ")
                for key, val in apps['tags'].items():
                    click.secho("- {}: {}".format(key, val))

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