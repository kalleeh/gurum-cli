import click
import os
import requests
import json

from gureumecli.cli.main import pass_context, common_options
from gureumecli.lib.utils.util import request, json_to_table


@click.command('describe', short_help='Displays details about pipeline')
@click.argument('name')
@pass_context
def cli(ctx, name):
    """Display detailed information about the application."""
    pipelines = {}

    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

    url = api_uri + '/pipelines/' + name
    headers = {'Authorization': id_token}

    r = request('get', url, headers)
    pipelines = json.loads(r.text)
    pipelines = json.loads(pipelines['body'])

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

    # iterate over and print outputs
    click.secho("Outputs: ")
    for key, val in pipelines['outputs'].items():
        click.secho("- {}: {}".format(key, val))
    
    # iterate over and print tags
    click.secho("Tags: ")
    for key, val in pipelines['tags'].items():
        click.secho("- {}: {}".format(key, val))

    # Get CloudFormation Events
    url = api_uri + '/events/' + name
    headers = {'Authorization': id_token}

    r = request('get', url, headers)
    events = json.loads(r.text)
    events = json.loads(events['body'])

    click.echo(json_to_table(events))