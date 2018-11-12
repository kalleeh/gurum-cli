import click
import click_spinner
import os
import requests
import json
import time

from gureumecli.cli.main import pass_context, common_options
from gureumecli.lib.utils.util import request, json_to_table


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
    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

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

            click.echo('Deleting pipeline: {}\nThis usually takes around 5 minutes...'.format(name))
            
            # Get CloudFormation Events
            url = api_uri + '/events/' + name

            r = request('get', url, headers)
            events = json.loads(r.text)
            events = json.loads(events['body'])

            click.echo(json_to_table(events))

            click.echo('Working on: {}'.format(name))
            click.echo('This usually takes a couple of minutes...')
            click.echo('This call is asynchrounous so feel free to Ctrl+C ' \
                        'anytime and it will continue running in background.')

            if pipelines['status'].endswith('_COMPLETE'):
                break

            # refresh every 5 seconds
            time.sleep(5)
