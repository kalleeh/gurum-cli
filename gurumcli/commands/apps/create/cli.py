"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import click
import click_spinner
import os
import requests
import json
import time

from git import Repo, InvalidGitRepositoryError, GitCommandError

from gurumcli.cli.main import pass_context, common_options
from gurumcli.lib.utils.util import request, json_to_table, prettyprint, haikunate


@click.command('create', short_help='Create a new app')
@click.option('--name', prompt=True, default=haikunate(), help='Name of the app')
@click.option('--tasks', prompt=False, default='1', help='Number of tasks to run')
@click.option('--health-check-path', prompt=False, default='/', help='Path that is queried for health checks')
@click.option('--image', prompt=False, default='nginx:latest', help='Docker image to run')
@click.option('--subtype', type=click.Choice(['shared-lb','dedicated-lb'],), prompt=False, default='shared-lb', help='Type of application to provision')
@pass_context
def cli(ctx, **kwargs):
    """ \b
        Create a new application.

    \b
    Common usage:

        \b
        Display detailed information about an application.
        \b
        $ gurum apps create myApp
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
    
    resp = request('post', url, headers, payload)
    apps = resp['apps']

    # Start a loop that checks for stack creation status
    with click_spinner.spinner():
        while True:
            # Update creation status
            url = api_uri + '/apps/' + kwargs['name']
            headers = {'Authorization': id_token}

            resp = request('get', url, headers)
            apps = resp['apps'][0]

            # Get CloudFormation Events
            url = api_uri + '/events/' + kwargs['name']

            resp = request('get', url, headers)
            events = resp['events']

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
        create_repository(apps['repository'])

def create_repository(git_url):
    repo = ""
    try:
        repo = Repo('.')
        click.echo('Found existing git repository. Importing...')
    except InvalidGitRepositoryError as ex:
        click.echo('No existing git repository. Initializing... {}'.format(ex))
        repo = Repo.init('.')

    try:
        repo.create_remote('gurum', git_url)
        click.echo('Creating remote for platform...')
    except GitCommandError as ex:
        click.secho('Remote already exists...', fg='yellow')

    repo.remotes

    click.echo('Deploy by using git push gurum master')
