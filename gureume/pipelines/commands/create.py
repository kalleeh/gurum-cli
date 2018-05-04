import click
import click_spinner
import os
import requests
import json
import time

from gureume.cli import pass_context
from gureume.lib.util import request, json_to_table


@click.command('create', short_help='Create a new pipeline')
@click.argument('name')
@click.option('--app-name', prompt=True, help="App to link pipeline to")
@click.option('--app-dev', prompt=False, required=False, help="Add a development stage to the pipeline")
@click.option('--app-test', prompt=False, required=False, help="Add a test stage to the pipeline")
@click.option('--github-repo', prompt=True, help="GitHub repo to pull source from")
@click.option('--github-branch', prompt=True, default='master', help="Branch to deploy")
@click.option('--github-token', prompt=True, help="OAuth Token for access")
@click.option('--github-user', prompt=True, help="GitHub user name")
@pass_context
def cli(ctx, name, **kwargs):
    """Create a new pipeline."""
    id_token = ""
    apps = {}

    id_token = ctx.config.get('default', 'id_token')
    api_uri = ctx.config.get('default', 'api_uri')

    url = api_uri + '/pipelines/' + name
    headers = {'Authorization': id_token}
    
    # Dynamically get options and remove undefined options
    payload = json.dumps({k: v for k, v in kwargs.items() if v is not None})
    
    r = request('post', url, headers, payload)
    apps = json.loads(r.text)

    # Start a loop that checks for stack creation status
    with click_spinner.spinner():
        while True:
            # Update creation status
            url = api_uri + '/pipelines/' + name
            headers = {'Authorization': id_token}

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
            if(apps['status'] == 'CREATE_IN_PROGRESS'):
                click.secho("Status: " + apps['status'], fg='yellow')
            elif(apps['status'] == 'CREATE_COMPLETE'):
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

            click.echo('Creating pipeline: {}.\nThis usually takes around 5 minutes...'.format(name))
            
            # Get CloudFormation Events
            url = api_uri + '/events/' + name

            r = request('get', url, headers)
            events = json.loads(r.text)

            click.echo(json_to_table(events))

            if apps['status'] == 'CREATE_COMPLETE':
                break

            # refresh every 5 seconds
            time.sleep(5)
