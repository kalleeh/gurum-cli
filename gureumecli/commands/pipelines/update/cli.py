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


@click.command('update', short_help='Update the pipeline')
@click.argument('name')
@click.option('--app-name', prompt=True, help="App to link pipeline to")
@click.option('--app-dev', prompt=False, required=False, help="Add a development stage to the pipeline")
@click.option('--app-test', prompt=False, required=False, help="Add a test stage to the pipeline")
@click.option('--github-repo', prompt=False, required=False, help="GitHub repo to pull source from")
@click.option('--github-branch', prompt=False, required=False, default='master', help="Branch to deploy")
@click.option('--github-token', prompt=False, required=False, help="OAuth Token for access")
@click.option('--github-user', prompt=False, required=False, help="GitHub user name")
@pass_context
def cli(ctx, name, **kwargs):
    """Update pipeline configuration."""
    id_token = ""
    pipelines = {}

    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

    url = api_uri + '/pipelines/' + name
    headers = {'Authorization': id_token}

    # Dynamically get options and remove undefined options
    payload = json.dumps({k: v for k, v in kwargs.items() if v is not None})

    try:
        r = request('patch', url, headers, payload)
        pipelines = json.loads(pipelines['body'])
    except Exception:
        pass
    else:
        # Start a loop that checks for stack creation status
        with click_spinner.spinner():
            while True:
                # Update creation status
                url = api_uri + '/pipelines/' + name

                r = request('get', url, headers)
                pipelines = json.loads(r['body'])

                # Get CloudFormation Events
                url = api_uri + '/events/' + name

                r = request('get', url, headers)
                events = json.loads(r['body'])

                click.clear()
                prettyprint(pipelines)
                click.echo(json_to_table(events))

                click.echo('Working on: {}'.format(name))
                click.echo('This usually takes a couple of minutes...')
                click.echo('This call is asynchrounous so feel free to Ctrl+C ' \
                            'anytime and it will continue running in background.')

                if pipelines['status'].endswith('_COMPLETE'):
                    break

                # refresh every 5 seconds
                time.sleep(5)
