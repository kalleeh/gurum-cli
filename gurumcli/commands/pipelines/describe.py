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
from gurumcli.lib.utils.util import request, json_to_table, prettyprint


@click.command('describe', short_help='Displays details about pipeline')
@click.argument('name')
@pass_context
def cli(ctx, name):
    """Display detailed information about the application."""
    pipelines = {}

    id_token = ctx.config.get('default', 'id_token')
    api_uri = ctx.config.get('default', 'api_uri')

    url = api_uri + '/pipelines/' + name
    headers = {'Authorization': id_token}

    resp = request('get', url, headers)
    pipelines = resp['pipelines'][0]

    click.secho("=== " + pipelines['name'], fg='blue')
    click.secho("Description: " + pipelines['description'])

    # Get CloudFormation Events
    url = api_uri + '/events/' + name
    headers = {'Authorization': id_token}

    resp = request('get', url, headers)
    events = resp['events']

    prettyprint(pipelines)
    click.echo(json_to_table(events))
