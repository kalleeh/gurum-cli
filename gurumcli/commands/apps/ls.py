"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import click

from gurumcli.cli.main import pass_context, common_options
from gurumcli.libs.formatter import json_to_table
from gurumcommon.clients.api_client import ApiClient


@click.command('ls', short_help='List your apps')
@pass_context
@common_options
def cli(ctx):
    """ \b
        Lists your applications in the platform.

    \b
    Common usage:

        \b
        Logs in to the platform.
        \b
        $ gurum login
    """
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx)  # pragma: no cover


def do_cli(ctx):
    """List your apps in the platform."""
    api_client = ApiClient(
        api_uri=ctx.config.get(ctx.profile, 'api_uri'),
        id_token=ctx.config.get(ctx.profile, 'id_token')
    )

    resp = api_client.apps.list()
    apps = resp['apps']

    click.echo("=== Apps:")
    click.echo(json_to_table(apps))
