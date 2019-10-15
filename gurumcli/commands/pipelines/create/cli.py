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

from gurumcli.cli.main import pass_context, common_options
from gurumcli.lib.utils.util import request, json_to_table, prettyprint, haikunate


@click.command('create', short_help='Create a new pipeline')
@click.option('--name', prompt=True, default=haikunate(), help='Name of the pipeline')
@click.option('--app-name', prompt=True, help="App to link pipeline to")
@click.option('--app-dev', prompt=False, required=False, help="Add a development stage to the pipeline")
@click.option('--app-test', prompt=False, required=False, help="Add a test stage to the pipeline")
@click.option('--github-repo', prompt=True, help="GitHub repo to pull source from")
@click.option('--github-branch', prompt=True, default='master', help="Branch to deploy")
@click.option('--github-token', prompt=True, help="OAuth Token for access")
@click.option('--github-user', prompt=True, help="GitHub user name")
@pass_context
def cli(ctx, **kwargs):
    """Create a new pipeline."""
    id_token = ""
    pipelines = {}

    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

    url = api_uri + '/pipelines'
    headers = {'Authorization': id_token}
    
    # Dynamically get options and remove undefined options
    payload = json.dumps({k: v for k, v in kwargs.items() if v is not None})

    resp = request('post', url, headers, payload)
    pipelines = resp['pipelines']

    # Start a loop that checks for stack creation status
    with click_spinner.spinner():
        while True:
            # Update creation status
            url = api_uri + '/pipelines/' + kwargs['name']
            headers = {'Authorization': id_token}

            resp = request('get', url, headers)
            pipelines = resp['pipelines'][0]

            # Get CloudFormation Events
            url = api_uri + '/events/' + kwargs['name']

            resp = request('get', url, headers)
            events = resp['events']

            click.clear()
            prettyprint(pipelines)
            click.echo(json_to_table(events))

            click.echo('Working on: {}'.format(kwargs['name']))
            click.echo('This usually takes a couple of minutes...')
            click.echo('This call is asynchrounous so feel free to Ctrl+C ' \
                        'anytime and it will continue running in background.')

            if pipelines['status'] == 'CREATE_COMPLETE':
                break

            # refresh every 5 seconds
            time.sleep(5)