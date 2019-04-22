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

from gureumecli.cli.main import pass_context, common_options
from gureumecli.lib.utils.util import request, json_to_table, prettyprint


@click.command('update', short_help='Update the app')
@click.argument('name')
@click.option('--tasks', prompt=False, help='Number of tasks to run')
@click.option('--health-check-path', prompt=False, help='Path that is queried for health checks')
@click.option('--image', prompt=False, help='Docker image to run')
@click.option('--upgrade-version', is_flag=True, prompt=False, help='Force platform version upgrade')
@pass_context
@common_options
def cli(ctx, name, **kwargs):
    """ \b
        Update your application.

    \b
    Common usage:

        \b
        Update your application parameters such as number of running tasks,
        health-check-path or the Docker image.
        \b
        $ gureume apps update MyApp --health-check-path '/'
    """
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx, name, **kwargs)  # pragma: no cover


def do_cli(ctx, name, **kwargs):
    """Update a new application."""
    id_token = ""
    apps = {}

    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

    url = api_uri + '/apps/' + name
    headers = {'Authorization': id_token}

    # Dynamically get options and remove undefined options
    payload = json.dumps({k: v for k, v in kwargs.items() if v is not None})

    resp = request('patch', url, headers, payload)
    apps = resp['apps']
    
    # Start a loop that checks for stack creation status
    with click_spinner.spinner():
        while True:
            # Update creation status
            url = api_uri + '/apps/' + name
            
            resp = request('get', url, headers)
            apps = resp['apps'][0]

            # Get CloudFormation Events
            url = api_uri + '/events/' + name

            resp = request('get', url, headers)
            events = resp['events']

            click.clear()
            prettyprint(apps)
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