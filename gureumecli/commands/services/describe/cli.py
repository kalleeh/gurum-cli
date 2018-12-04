import click
import os
import requests
import json

from gureumecli.cli.main import pass_context, common_options
from gureumecli.lib.utils.util import request, json_to_table


@click.command('describe', short_help='Displays details about service')
@click.argument('name')
@pass_context
def cli(ctx, name):
    """Display detailed information about the application."""
    services = {}

    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

    url = api_uri + '/services/' + name
    headers = {'Authorization': id_token}

    r = request('get', url, headers)
    services = json.loads(r.text)
    services = json.loads(services['body'])

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

    # iterate over and print outputs
    click.secho("Outputs: ")
    for key, val in services['outputs'].items():
        click.secho("- {}: {}".format(key, val))
    
    # iterate over and print tags
    click.secho("Tags: ")
    for key, val in services['tags'].items():
        click.secho("- {}: {}".format(key, val))

    # Get CloudFormation Events
    url = api_uri + '/events/' + name
    headers = {'Authorization': id_token}

    r = request('get', url, headers)
    events = json.loads(r.text)
    events = json.loads(events['body'])

    click.echo(json_to_table(events))
