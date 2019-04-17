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
        $ gureume login
    """
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx)  # pragma: no cover


def do_cli(ctx):
    """List your apps in the platform."""
    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

    url = api_uri + '/apps'
    headers = {'Authorization': id_token}

    r = request('get', url, headers)
    apps = json.loads(r['body'])

    click.echo("=== Apps:")
    click.echo(json_to_table(apps))
