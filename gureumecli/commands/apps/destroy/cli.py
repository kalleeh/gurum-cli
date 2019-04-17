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


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()

@click.command('destroy', short_help='Delete app')
@click.argument('name')
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to destroy the app?')
@pass_context
@common_options
def cli(ctx, name):
    """ \b
        Delete an application.

    \b
    Common usage:

        \b
        Delete an application.
        \b
        $ gureume apps destroy myApp
    """
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx, name)  # pragma: no cover


def do_cli(ctx, name):
    """Deletes the application."""
    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

    click.echo('Deleting app...')

    url = api_uri + '/apps/' + name
    headers = {'Authorization': id_token}

    r = request('delete', url, headers)

    with click_spinner.spinner():
        while True:
            # Update creation status
            url = api_uri + '/apps/' + name
            headers = {'Authorization': id_token}

            r = request('get', url, headers)
            apps = json.loads(r['body'])

            # Get CloudFormation Events
            url = api_uri + '/events/' + name

            r = request('get', url, headers)
            events = json.loads(r['body'])

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