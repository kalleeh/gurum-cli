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
from gurumcli.libs.formatter import json_to_table
from gurumcommon.clients.api_client import ApiClient


@click.command('ls', short_help='List your pipelines')
@pass_context
def cli(ctx):
    """List your pipelines in the platform."""
    api_client = ApiClient(
        api_uri=ctx.config.get(ctx.profile, 'api_uri'),
        id_token=ctx.config.get(ctx.profile, 'id_token')
    )

    resp = api_client.list('pipelines')
    pipelines = resp['pipelines']

    click.echo("=== Pipelines:")
    click.echo(json_to_table(pipelines))
