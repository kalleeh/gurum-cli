import click
import os
import requests
import json

from gureume.cli import pass_context
from gureume.lib.util import request, json_to_table


@click.command('describe', short_help='Displays details about app')
@click.argument('name')
@pass_context
def cli(ctx, name):
    """Display detailed information about the application."""
    apps = {}

    id_token = ctx.config.get('default', 'id_token')
    api_uri = ctx.config.get('default', 'api_uri')

    # Get app status
    url = api_uri + '/apps/' + name
    headers = {'Authorization': id_token}

    r = request('get', url, headers)
    apps = json.loads(r.text)

    # Get CloudFormation Events
    url = api_uri + '/events/' + name

    r = request('get', url, headers)
    events = json.loads(r.text)

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
    if 'service_role' in apps:
        click.secho("Service Role: " + apps['service_role'], fg='yellow')

    # iterate over and print tags
    click.secho("Tags: ")
    for key, val in apps['tags'].items():
        click.secho("- {}: {}".format(key, val))

    click.echo(json_to_table(events))