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
from gurumcli.lib.utils.util import request, json_to_table, prettyprint, prettyprint, haikunate


@click.command('create', short_help='Create a new service')
@click.option('--name', prompt=True, default=haikunate(), help='Name of the service')
@click.option('--service-type', type=click.Choice(['s3']), prompt=True, help="The type of backing service")
@click.option('--service-bindings', prompt=True, required=True, help="Comma-separated string of applications to bind the service to")
@click.option('--service-version', prompt=False, required=False, help="Add a test stage to the service")
@pass_context
def cli(ctx, **kwargs):
    """Create a new service."""
    id_token = ""
    services = {}

    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

    url = api_uri + '/services'
    headers = {'Authorization': id_token}
    
    # Dynamically get options and remove undefined options
    payload = json.dumps({k: v for k, v in kwargs.items() if v is not None})

    resp = request('post', url, headers, payload)
    services = resp['services']

    # Start a loop that checks for stack creation status
    with click_spinner.spinner():
        while True:
            # Update creation status
            url = api_uri + '/services/' + kwargs['name']
            headers = {'Authorization': id_token}

            resp = request('get', url, headers)
            services = resp['services'][0]

            # Get CloudFormation Events
            url = api_uri + '/events/' + kwargs['name']

            resp = request('get', url, headers)
            events = resp['events']

            click.clear()
            prettyprint(services)
            click.echo(json_to_table(events))

            click.echo('Working on: {}'.format(kwargs['name']))
            click.echo('This usually takes a couple of minutes...')
            click.echo('This call is asynchrounous so feel free to Ctrl+C ' \
                        'anytime and it will continue running in background.')

            if services['status'] == 'CREATE_COMPLETE':
                break

            # refresh every 5 seconds
            time.sleep(5)
