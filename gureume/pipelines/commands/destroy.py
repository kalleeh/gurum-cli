import click
import click_spinner
import os
import requests
import json
import time

from gureume.cli import pass_context
from gureume.lib.util import request, json_to_table


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()

@click.command('destroy', short_help='Delete app')
@click.argument('name')
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to destroy the pipeline?')
@pass_context
def cli(ctx, name):
    """Deletes the pipeline."""
    id_token = ctx.config.get('default', 'id_token')
    api_uri = ctx.config.get('default', 'api_uri')

    click.echo('Deleting pipeline...')

    url = api_uri + '/pipelines/' + name
    headers = {'Authorization': id_token}

    r = request('delete', url, headers)

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

            click.echo('Deleting pipeline: {}.\nThis usually takes around 5 minutes...'.format(name))
            
            # Get CloudFormation Events
            url = api_uri + '/events/' + name

            r = request('get', url, headers)
            events = json.loads(r.text)

            click.echo(json_to_table(events))

            if apps['status'].endswith('_COMPLETE'):
                break

            # refresh every 5 seconds
            time.sleep(5)
