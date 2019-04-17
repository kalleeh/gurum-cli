"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import click
import os
import requests
import json

from gureumecli.cli.main import pass_context, common_options
from gureumecli.lib.utils.util import request, json_to_table, prettyprint


@click.command('ls', short_help='List your pipelines')
@pass_context
def cli(ctx):
    """List your pipelines in the platform."""
    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

    url = api_uri + '/pipelines'
    headers = {'Authorization': id_token}

    r = request('get', url, headers)
    pipelines = json.loads(r['body'])

    click.echo("=== Pipelines:")
    click.echo(json_to_table(pipelines))