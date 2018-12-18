import click
import click_spinner
import os
import requests
import json
import time

from git import Repo, InvalidGitRepositoryError, GitCommandError

from gureumecli.cli.main import pass_context, common_options
from gureumecli.lib.utils.util import request, json_to_table, haikunate


@click.command('deploy', short_help='Deploy through pipeline')
@click.option('--name', prompt=True, help='Name of the pipeline to deploy to')
@click.option('--force', isFlag=True, help='Force re-deployment even if there are no changes')
@pass_context
def cli(ctx, **kwargs):
    """Deploys the current directories repository through pipeline."""
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
            events = json.loads(r.text)
            events = json.loads(events['body'])

            click.clear()

            click.secho("=== " + apps['name'], fg='blue')
            click.secho("Description: " + apps['description'])

            # print status yellow if in progress, completed is green
            if(apps['status'] == 'CREATE_IN_PROGRESS'):
                click.secho("Status: " + apps['status'], fg='yellow')
            elif(apps['status'] == 'CREATE_COMPLETE'):
                click.secho("Status: " + apps['status'], fg='green')
            else:
                click.secho("Status: " + apps['status'], fg='red')

            if 'endpoint' in apps:
                click.secho("Endpoint: " + apps['endpoint'], fg='green')
            if 'repository' in apps:
                click.secho("Repository: " + apps['repository'], fg='green')

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
