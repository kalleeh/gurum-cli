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

from gurumcli.cli.main import pass_context, common_options
from gurumcli.lib.utils.util import request, json_to_table, prettyprint, prettyprint


@click.command('describe', short_help='Displays details about service')
@click.argument('name')
@pass_context
def cli(ctx, name):
    """Display detailed information about the application."""
    services = {}

    id_token = ctx._config.get('default', 'id_token')
    api_uri = ctx._config.get('default', 'api_uri')

    url = api_uri + '/services/' + name
    headers = {'Authorization': id_token}

    resp = request('get', url, headers)
    services = resp['services'][0]

    # Get CloudFormation Events
    url = api_uri + '/events/' + name
    headers = {'Authorization': id_token}

    resp = request('get', url, headers)
    events = resp['events']

    prettyprint(services)
    click.echo(json_to_table(events))
