import click
import click_spinner
import os
import requests
import json
import time

from gureume.cli import pass_context
from gureume.lib.util import request, json_to_table


@click.command('update', short_help='Update the pipeline')
@click.argument('name')
@click.option('--app', prompt=True, help="App to link pipeline to")
@click.option('--dev', prompt=False, default='', required=False, help="Add a development stage to the pipeline")
@click.option('--test', prompt=False, default='', required=False, help="Add a test stage to the pipeline")
@click.option('--repo', prompt=True, default='2048', help="GitHub repo to pull source from")
@click.option('--branch', prompt=True, default='master', help="Branch to deploy")
@click.option('--token', prompt=True, default='b248f1e73603d95c33e12d4bca375fc965c96ad8', help="OAuth Token for access")
@click.option('--user', prompt=True, default='kalleeh', help="GitHub user name")
@pass_context
def cli(ctx, name, app, dev, test, repo, branch, token, user):
    """Update pipeline configuration."""
    id_token = ""
    pipelines = {}

    id_token = ctx.config.get('default', 'id_token')
    api_uri = ctx.config.get('default', 'api_uri')

    url = api_uri + '/pipelines/' + name
    headers = {'Authorization': id_token}
    payload = {
        'app_name': app,
        'app_dev': dev,
        'app_test': test,
        'github_repo': repo,
        'github_branch': branch,
        'github_token': token,
        'github_user': user
    }

    try:
        r = request('patch', url, headers, payload)
        pipelines = json.loads(r.text)
    except Exception:
        pass
    else:
        # Start a loop that checks for stack creation status
        with click_spinner.spinner():
            while True:
                # Update creation status
                url = api_uri + '/pipelines/' + name

                r = request('get', url, headers)
                pipelines = json.loads(r.text)

                # Get CloudFormation Events
                url = api_uri + '/events/' + name

                r = request('get', url, headers)
                events = json.loads(r.text)

                click.clear()
                
                click.secho("=== " + pipelines['name'], fg='yellow')
                click.secho("Description: " + pipelines['description'])

                # print status yellow if in progress, completed is green
                if(pipelines['status'].endswith('_IN_PROGRESS')):
                    click.secho("Status: " + pipelines['status'], fg='yellow')
                elif(pipelines['status'].endswith('_COMPLETE')):
                    click.secho("Status: " + pipelines['status'], fg='green')
                else:
                    click.secho("Status: " + pipelines['status'], fg='red')

                if 'endpoint' in pipelines:
                    click.secho("Endpoint: " + pipelines['endpoint'], fg='yellow')
                if 'repository' in pipelines:
                    click.secho("Repository: " + pipelines['repository'], fg='yellow')

                # iterate over and print tags
                click.secho("Tags: ")
                for key, val in pipelines['tags'].items():
                    click.secho("- {}: {}".format(key, val))

                click.echo('Updating app: {}.\nThis usually takes around 5 minutes...'.format(name))
                
                click.echo(json_to_table(events))

                if pipelines['status'].endswith('_COMPLETE'):
                    break

                # refresh every 5 seconds
                time.sleep(5)
