"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import json
import click

from gurumcli.cli.main import pass_context
from gurumcli.libs.formatter import json_to_table, prettyprint
from gurumcommon.clients.api_client import ApiClient


@click.command('describe', short_help='Displays details about pipeline')
@click.argument('name')
@pass_context
def cli(ctx, name):
    """Display detailed information about the application."""
    pipelines = {}
    payload = {}
    payload['name'] = name

    api_client = ApiClient(
        api_uri=ctx.config.get(ctx.profile, 'api_uri'),
        id_token=ctx.config.get(ctx.profile, 'id_token')
    )

    resp = api_client.describe(resource='pipelines', payload=json.dumps(payload))
    pipelines = resp['pipelines'][0]

    resp = api_client.describe(resource='events', payload=json.dumps(payload))
    events = resp['events']

    prettyprint(pipelines)
    click.echo(json_to_table(events))
