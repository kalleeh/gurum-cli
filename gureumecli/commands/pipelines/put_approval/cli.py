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
import json
import time

from gurumcli.cli.main import pass_context, common_options
from gurumcli.lib.utils.util import request, json_to_table, prettyprint

@click.command('put-approval', short_help='Displays status about your pipeline')
@click.argument('name')
@click.option('--summary', prompt=True, help="Approve update message.")
@click.option('--status', prompt=True, type=click.Choice(['Approved','Rejected']), help="String giving the Approved or Rejected status")
@pass_context
def cli(ctx, name, **kwargs):
    """Approve or reject an application deployment."""
    states = []

    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

    url = api_uri + '/pipelines/' + name + '/states'
    headers = {'Authorization': id_token}

    # Dynamically get options and remove undefined options
    payload = json.dumps({k: v for k, v in kwargs.items() if v is not None})

    resp = request('put', url, headers, payload)
    states = resp['states']
    
    click.secho("=== " + name + ' status', fg='blue')

    click.echo(states)