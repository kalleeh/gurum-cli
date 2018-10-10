import click
import click_spinner
import os
import requests
import json
import time

from gureume.cli import pass_context
from gureume.lib.util import request, json_to_table


@click.command('update', short_help='Update the pipeline')
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
    """Update pipeline configuration."""
    id_token = ""
    pipelines = {}

    id_token = ctx.config.get('default', 'id_token')
    api_uri = ctx.config.get('default', 'api_uri')

    url = api_uri + '/pipelines/' + name
    headers = {'Authorization': id_token}

    # Dynamically get options and remove undefined options
    payload = json.dumps({k: v for k, v in kwargs.items() if v is not None})

    try:
        r = request('patch', url, headers, payload)
        pipelines = json.loads(r.text)
    except Exception:
        pass
    else:
        # Start a loop that checks for stack creation status
        with click_spinner.spinner():
            while True:
                # Update creation status
                url = api_uri + '/pipelines/' + name

                r = request('get', url, headers)
                pipelines = json.loads(r.text)
                pipelines = json.loads(pipelines['body'])

                # Get CloudFormation Events
                url = api_uri + '/events/' + name

                r = request('get', url, headers)
                events = json.loads(r.text)
                events = json.loads(events['body'])

                click.clear()
                
                click.secho("=== " + pipelines['name'], fg='blue')
                click.secho("Description: " + pipelines['description'])

                # print status yellow if in progress, completed is green
                if(pipelines['status'].endswith('_IN_PROGRESS')):
                    click.secho("Status: " + pipelines['status'], fg='yellow')
                elif(pipelines['status'].endswith('_COMPLETE')):
                    click.secho("Status: " + pipelines['status'], fg='green')
                else:
                    click.secho("Status: " + pipelines['status'], fg='red')

                if 'endpoint' in pipelines:
                    click.secho("Endpoint: " + pipelines['endpoint'], fg='green')
                if 'repository' in pipelines:
                    click.secho("Repository: " + pipelines['repository'], fg='green')

                # iterate over and print tags
                click.secho("Tags: ")
                for key, val in pipelines['tags'].items():
                    click.secho("- {}: {}".format(key, val))

                click.echo(json_to_table(events))

                click.echo('Working on: {}'.format(name))
                click.echo('This usually takes a couple of minutes...')
                click.echo('This call is asynchrounous so feel free to Ctrl+C ' \
                            'anytime and it will continue running in background.')

                if pipelines['status'].endswith('_COMPLETE'):
                    break

                # refresh every 5 seconds
                time.sleep(5)
