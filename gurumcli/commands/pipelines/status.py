"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import time
import json

import click
import click_spinner

from gurumcli.cli.main import pass_context
from gurumcli.libs.formatter import json_to_table
from gurumcommon.clients.api_client import ApiClient

@click.command('status', short_help='Displays status about your pipeline')
@click.argument('name')
@click.option('--watch', is_flag=True, help='Automatically update the stauts every 5s')
@pass_context
def cli(ctx, name, watch):
    """Display detailed information about the application."""
    payload = {}
    payload['name'] = name
    states = []

    api_client = ApiClient(
        api_uri=ctx.config.get(ctx.profile, 'api_uri'),
        id_token=ctx.config.get(ctx.profile, 'id_token')
    )

    # Start a loop that checks for stack creation status
    with click_spinner.spinner():
        while True:
            resp = api_client.describe(resource='pipelines', payload=json.dumps(payload), custom_uri='/states')
            states = resp['states']

            if watch:
                click.clear()

            click.secho("=== " + name + ' status', fg='blue')

            click.echo(json_to_table(states))

            if not watch:
                break

            click.echo('Watching status of pipeline: {}'.format(name))
            click.echo('This call is asynchrounous so feel free to Ctrl+C ' \
                        'anytime and it will continue running in background.')

            # refresh every 5 seconds
            time.sleep(5)
