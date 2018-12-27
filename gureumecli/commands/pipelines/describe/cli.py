import click
import os
import requests
import json

from gureumecli.cli.main import pass_context, common_options
from gureumecli.lib.utils.util import request, json_to_table, prettyprint


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
    pipelines = json.loads(r['body'])

    click.secho("=== " + pipelines['name'], fg='blue')
    click.secho("Description: " + pipelines['description'])

    # Get CloudFormation Events
    url = api_uri + '/events/' + name
    headers = {'Authorization': id_token}

    r = request('get', url, headers)
    events = json.loads(r['body'])

    prettyprint(pipelines)
    click.echo(json_to_table(events))