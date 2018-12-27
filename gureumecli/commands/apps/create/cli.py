import click
import click_spinner
import os
import requests
import json
import time

from git import Repo, InvalidGitRepositoryError, GitCommandError

from gureumecli.cli.main import pass_context, common_options
from gureumecli.lib.utils.util import request, json_to_table, prettyprint, haikunate


@click.command('create', short_help='Create a new app')
@click.option('--name', prompt=True, default=haikunate(), help='Name of the app')
@click.option('--tasks', prompt=False, default='1', help='Number of tasks to run')
@click.option('--health-check-path', prompt=False, default='/health', help='Path that is queried for health checks')
@click.option('--image', prompt=False, default='nginx:latest', help='Docker image to run')
@pass_context
def cli(ctx, **kwargs):
    """ \b
        Create a new application.

    \b
    Common usage:

        \b
        Display detailed information about an application.
        \b
        $ gureume apps create myApp
    """
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx, **kwargs)  # pragma: no cover


def do_cli(ctx, **kwargs):
    """Create a new application."""
    id_token = ""
    apps = {}
    payload = {}

    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

    url = api_uri + '/apps'
    headers = {'Authorization': id_token}
    
    # Dynamically get options and remove undefined options
    payload = json.dumps({k: v for k, v in kwargs.items() if v is not None})
    
    r = request('post', url, headers, payload)
    apps = json.loads(r['body'])

    # Start a loop that checks for stack creation status
    with click_spinner.spinner():
        while True:
            # Update creation status
            url = api_uri + '/apps/' + kwargs['name']
            headers = {'Authorization': id_token}

            r = request('get', url, headers)
            apps = json.loads(r.text)
            apps = json.loads(r['body'])

            # Get CloudFormation Events
            url = api_uri + '/events/' + kwargs['name']

            r = request('get', url, headers)
            events = json.loads(r['body'])

            click.clear()
            prettyprint(apps)
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
