"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import click

from gurumcli.cli.main import pass_context
from gurumcli.lib.utils.util import request, json_to_table


@click.command('ls', short_help='List your pipelines')
@pass_context
def cli(ctx):
    """List your pipelines in the platform."""
    id_token = ctx.cfg.get('default', 'id_token')
    api_uri = ctx.cfg.get('default', 'api_uri')

    url = api_uri + '/pipelines'
    headers = {'Authorization': id_token}

    resp = request('get', url, headers)
    pipelines = resp['pipelines']

    click.echo("=== Pipelines:")
    click.echo(json_to_table(pipelines))
