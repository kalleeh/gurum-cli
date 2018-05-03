import click
import click_spinner
import os
import requests
import json
import time

from gureume.cli import pass_context
from gureume.lib.util import request, json_to_table


@click.command('destroy', short_help='Delete app')
@click.argument('name')
@click.option('--confirm', is_flag=True, help='Silence confirmation question.')
@pass_context
def cli(ctx, name, confirm):
    """Deletes the application."""
    id_token = ctx.config.get('default', 'id_token')
    api_uri = ctx.config.get('default', 'api_uri')

    # Check if app exists
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

    if not confirm:
        if click.confirm('Are you sure you want to delete pipeline: ' + name + '?', abort=True):
            confirm = True

    if confirm:
        click.echo('Deleting app...')

        url = api_uri + '/pipelines/' + name
        headers = {'Authorization': id_token}
        try:
            r = requests.delete(url, headers=headers)
            r.raise_for_status()  # throw exception if request does not return 2xx
        except requests.exceptions.HTTPError as e:
            if r.status_code == 422:  # Unprocessable Entity
                json_response = json.loads(r.text)
                if json_response['errors'][0]['code'] == 'error_code':
                    print('error explanation')

            # Unprocessable for some other reason or other HTTP error != 422
            print('HTTP Error: {}'.format(e))
            return -1
        except requests.exceptions.RequestException as e:
            print('Connection error: {}'.format(e))
            return -1

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
