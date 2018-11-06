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
              prompt='Are you sure you want to destroy the app?')
@pass_context
def cli(ctx, name):
    """Deletes the application."""
    id_token = ctx.config.get('default', 'id_token')
    api_uri = ctx.config.get('default', 'api_uri')

    click.echo('Deleting app...')

    url = api_uri + '/apps/' + name
    headers = {'Authorization': id_token}

    r = request('delete', url, headers)

    with click_spinner.spinner():
        while True:
            # Update creation status
            url = api_uri + '/apps/' + name
            headers = {'Authorization': id_token}

            r = request('get', url, headers)
            apps = json.loads(r.text)
            apps = json.loads(apps['body'])

            # Get CloudFormation Events
            url = api_uri + '/events/' + name

            r = request('get', url, headers)
            events = json.loads(r.text)
            events = json.loads(events['body'])

            click.clear()
            
            click.secho("=== " + apps['name'], fg='blue')
            click.secho("Description: " + apps['description'])

            # print status yellow if in progress, completed is green
            if(apps['status'].endswith('_IN_PROGRESS')):
                click.secho("Status: " + apps['status'], fg='yellow')
            elif(apps['status'].endswith('_COMPLETE')):
                click.secho("Status: " + apps['status'], fg='green')
            else:
                click.secho("Status: " + apps['status'], fg='red')

            if 'endpoint' in apps:
                click.secho("Endpoint: " + apps['endpoint'], fg='green')
            if 'repository' in apps:
                click.secho("Repository: " + apps['repository'], fg='green')
            if 'service_role' in apps:
                click.secho("Service Role: " + apps['service_role'], fg='green')

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