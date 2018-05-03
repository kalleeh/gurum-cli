import click
import click_spinner
import os
import requests
import json
import time

from gureume.cli import pass_context
from gureume.lib.util import request, json_to_table


@click.command('create', short_help='Create a new pipeline')
@click.argument('name')
@click.option('--app', prompt=True, help="App to link pipeline to")
@click.option('--dev', prompt=False, default='', required=False, help="Add a development stage to the pipeline")
@click.option('--test', prompt=False, default='', required=False, help="Add a test stage to the pipeline")
@click.option('--repo', prompt=True, help="GitHub repo to pull source from")
@click.option('--branch', prompt=True, default='master', help="Branch to deploy")
@click.option('--token', prompt=True, help="OAuth Token for access")
@click.option('--user', prompt=True, help="GitHub user name")
@pass_context
def cli(ctx, name, app, dev, test, repo, branch, token, user):
    """Create a new application."""
    id_token = ""
    apps = {}

    id_token = ctx.config.get('default', 'id_token')
    api_uri = ctx.config.get('default', 'api_uri')

    url = api_uri + '/pipelines/' + name
    headers = {'Authorization': id_token}
    payload = {
        "app_name": app,
        "app_dev": dev,
        "app_test": test,
        "github_repo": repo,
        "github_branch": branch,
        "github_token": token,
        "github_user": user
    }

    # Convert dict to JSON
    payload = json.dumps(payload)

    try:
        r = requests.post(url, json=payload, headers=headers)
        r.raise_for_status()  # throw exception if request does not return 2xx
    except requests.exceptions.HTTPError as e:
        if r.status_code == 422:  # Unprocessable Entity
            json_response = json.loads(r.text)
            if json_response['errors'][0]['code'] == 'error_code':
                print('error explanation')

        # Unprocessable for some other reason or other HTTP error != 422
        print(r.text)
        print('HTTP Error: {}'.format(e))
        return -1
    except requests.exceptions.RequestException as e:
        print('Connection error: {}'.format(e))
        return -1

    # Start a loop that checks for stack creation status
    with click_spinner.spinner():
        while True:
            # Update creation status
            url = api_uri + '/pipelines/' + name
            headers = {'Authorization': id_token}

            try:
                r = requests.get(url, headers=headers)
                r.raise_for_status()  # throw exception if request does not return 2xx
            except requests.exceptions.HTTPError as e:
                if r.status_code == 422:  # Unprocessable Entity
                    json_response = json.loads(r.text)
                    if json_response['errors'][0]['code'] == 'error_code':
                        print('error explanation')

                # Unprocessable for some other reason or other HTTP error != 422
                print(r.text)
                print('HTTP Error: {}'.format(e))
                return -1
            except requests.exceptions.RequestException as e:
                print('Connection error: {}'.format(e))
                return -1

            apps = json.loads(r.text)

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

            click.echo('Creating pipeline: {}.\nThis usually takes around 5 minutes...'.format(name))
            
            # Get CloudFormation Events
            url = api_uri + '/events/' + name

            r = request('get', url, headers)
            events = json.loads(r.text)

            click.echo(json_to_table(events))

            if apps['status'] == 'CREATE_COMPLETE':
                break

            # refresh every 5 seconds
            time.sleep(5)
