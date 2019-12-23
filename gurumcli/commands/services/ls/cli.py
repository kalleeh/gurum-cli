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


@click.command('ls', short_help='List your services')
@pass_context
def cli(ctx):
    """List your services in the platform."""
    id_token = ctx.config.get('default', 'id_token')
    api_uri = ctx.config.get('default', 'api_uri')

    url = api_uri + '/services'
    headers = {'Authorization': id_token}

    resp = request('get', url, headers)
    services = resp['services']

    click.echo("=== Services:")
    click.echo(json_to_table(services))
