import click
import click_spinner
import os
import requests
import json
import time

from git import Repo, InvalidGitRepositoryError, GitCommandError

from gureume.cli import pass_context
from gureume.lib.util import request, json_to_table, haikunate


@click.command('create', short_help='Create a new app')
@click.option('--name', prompt=True, default=haikunate(), help='Name of the app')
@click.option('--tasks', prompt=False, default='1', help='Number of tasks to run')
@click.option('--health-check-path', prompt=False, default='/health', help='Path that is queried for health checks')
@click.option('--image', prompt=False, default='nginx:latest', help='Docker image to run')
@pass_context
def cli(ctx, **kwargs):
    """Create a new application."""
    id_token = ""
    apps = {}
    payload = {}

    id_token = ctx.config.get('default', 'id_token')
    api_uri = ctx.config.get('default', 'api_uri')

    url = api_uri + '/apps'
    headers = {'Authorization': id_token}
    
    # Dynamically get options and remove undefined options
    payload = json.dumps({k: v for k, v in kwargs.items() if v is not None})

    r = request('post', url, headers, payload)
    apps = json.loads(r.text)

    # Start a loop that checks for stack creation status
    with click_spinner.spinner():
        while True:
            # Update creation status
            url = api_uri + '/apps/' + kwargs['name']
            headers = {'Authorization': id_token}

            r = request('get', url, headers)
            apps = json.loads(r.text)

            # Get CloudFormation Events
            url = api_uri + '/events/' + kwargs['name']

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

            click.echo(json_to_table(events))

            click.echo('Working on: {}'.format(kwargs['name']))
            click.echo('This usually takes a couple of minutes...')
            click.echo('This call is asynchrounous so feel free to Ctrl+C ' \
                        'anytime and it will continue running in background.')

            # Stop loop if task is complete
            if apps['status'].endswith('_COMPLETE'):
                break

            # refresh every 5 seconds
            time.sleep(5)

    # Check if app returned a repository endpoint, if so configure a git remote
    if 'repository' in apps:
        repo = ""
        try:
            repo = Repo('.')
            click.echo('Found existing git repository. Importing...')
        except InvalidGitRepositoryError as ex:
            click.echo('No existing git repository. Initializing... {}'.format(ex))
            repo = Repo.init('.')

        try:
            repo.create_remote('gureume', apps['repository'])
            click.echo('Creating remote for platform...')
        except GitCommandError as ex:
            click.secho('Remote already exists...', fg='yellow')

        repo.remotes

        click.echo('Deploy by using git push gureume master')
