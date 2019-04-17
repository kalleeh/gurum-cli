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


@click.command('describe', short_help='Displays details about app')
@click.argument('name')
@click.option('--watch', is_flag=True, help='Automatically update the stauts every 5s')
@pass_context
@common_options
def cli(ctx, name, watch):
    """ \b
        Display detailed information about the application

    \b
    Common usage:

        \b
        Display detailed information about an application.
        \b
        $ gureume apps describe myApp
    """
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx, name, watch)  # pragma: no cover


def do_cli(ctx, name, watch):
    """Display detailed information about the application."""
    apps = {}

    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

    # Start a loop that checks for stack creation status
    with click_spinner.spinner():
        while True:
            # Get app status
            url = api_uri + '/apps/' + name
            headers = {'Authorization': id_token}
            
            r = request('get', url, headers)
            apps = json.loads(r['body'])

            # Get CloudFormation Events
            url = api_uri + '/events/' + name

            r = request('get', url, headers)
            events = json.loads(r['body'])

            if watch:
                click.clear()

            prettyprint(apps)
            click.echo(json_to_table(events))
            
            if not watch:
                break
            
            click.echo('Working on: {}'.format(name))
            click.echo('This usually takes a couple of minutes...')
            click.echo('This call is asynchrounous so feel free to Ctrl+C ' \
                        'anytime and it will continue running in background.')

            # Stop loop if task is complete
            if apps['status'].endswith('_COMPLETE') and not watch:
                break

            # refresh every 5 seconds
            time.sleep(5)