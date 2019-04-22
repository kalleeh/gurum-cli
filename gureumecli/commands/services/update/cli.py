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


@click.command('update', short_help='Update the service')
@click.argument('name')
@click.option('--service-bindings', prompt=True, required=True, help="Comma-separated string of applications to bind the service to")
@click.option('--upgrade-version', is_flag=True, prompt=False, help='Force platform version upgrade')
@pass_context
def cli(ctx, name, **kwargs):
    """Update service configuration."""
    id_token = ""
    services = {}

    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

    url = api_uri + '/services/' + name
    headers = {'Authorization': id_token}

    # Dynamically get options and remove undefined options
    payload = json.dumps({k: v for k, v in kwargs.items() if v is not None})

    try:
        resp = request('patch', url, headers, payload)
        services = resp['services']
    except Exception:
        pass
    else:
        # Start a loop that checks for stack creation status
        with click_spinner.spinner():
            while True:
                # Update creation status
                url = api_uri + '/services/' + name

                resp = request('get', url, headers)
                services = resp['services'][0]

                # Get CloudFormation Events
                url = api_uri + '/events/' + name

                resp = request('get', url, headers)
                events = resp['events']

                click.clear()
                prettyprint(services)
                click.echo(json_to_table(events))

                click.echo('Working on: {}'.format(name))
                click.echo('This usually takes a couple of minutes...')
                click.echo('This call is asynchrounous so feel free to Ctrl+C ' \
                            'anytime and it will continue running in background.')

                if services['status'].endswith('_COMPLETE'):
                    break

                # refresh every 5 seconds
                time.sleep(5)
