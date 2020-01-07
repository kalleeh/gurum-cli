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
from gurumcli.libs.formatter import json_to_table
from gurumcommon.clients.api_client import ApiClient

@click.command('put-approval', short_help='Displays status about your pipeline')
@click.argument('name')
@click.option('--summary', prompt=True, help="Approve update message.")
@click.option('--status', prompt=True, type=click.Choice(['Approved', 'Rejected']), help="String giving the Approved or Rejected status")
@pass_context
def cli(ctx, name, **kwargs):
    """Approve or reject an application deployment."""
    payload = {}
    payload['name'] = name
    states = []

    api_client = ApiClient(
        api_uri=ctx.config.get(ctx.profile, 'api_uri'),
        id_token=ctx.config.get(ctx.profile, 'id_token')
    )

    # Dynamically get options and remove undefined options
    args = json.dumps({k: v for k, v in kwargs.items() if v is not None})
    payload.update(json.loads(args))

    resp = api_client.put(resource='pipelines', payload=json.dumps(payload), custom_uri='/states')
    states = resp['states']

    click.secho("=== " + name + ' status', fg='blue')

    click.echo(json_to_table(states))
