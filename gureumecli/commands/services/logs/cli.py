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
import sys

import boto3

from botocore.client import ClientError
from termcolor import colored
from gureumecli.cli.main import pass_context, common_options
from gureumecli.lib.logs.awslogs import AWSLogs
import gureumecli.commands.exceptions as exceptions

@click.command('logs', short_help='Displays logs about your app')
@click.argument('name')
@click.option('--start', default='5m', help='Filter starting date/time to get logs')
@click.option('--end', help='Filter end date/time to get logs')
@click.option('--filter-pattern', help='Filter logs matching a filter pattern')
@click.option('--watch', is_flag=True, help='Follow logs')
@pass_context
def cli(ctx, name, **kwargs):
    """View logs for your app"""
    options = {}
    log_group_name = name
    
    # Dynamically get options and remove undefined options
    options = {k: v for k, v in kwargs.items() if v is not None}
    options['log_group_name'] = 'platform-svc-{}'.format(log_group_name)
    options['log_stream_name'] = 'ALL'
    options['color_enabled'] = 'true'
    options['output_stream_enabled'] = 'true'
    options['output_timestamp_enabled'] = 'true'
    options['aws_access_key_id'] = ctx._config.get('default', 'aws_access_key_id')
    options['aws_secret_access_key'] = ctx._config.get('default', 'aws_secret_access_key')
    options['aws_session_token'] = ctx._config.get('default', 'aws_session_token')
    options['aws_region'] = ctx._config.get('default', 'aws_region')

    try:
        logs = AWSLogs(**options)

        logs.list_logs()
    except ClientError as ex:
        code = ex.response['Error']['Code']
        if code in (u'AccessDeniedException', u'ExpiredTokenException'):
            hint = ex.response['Error'].get('Message', 'AccessDeniedException')
            sys.stderr.write(colored("{0}\n".format(hint), "yellow"))
            return 4
        if code in (u'ResourceNotFoundException'):
            click.echo('Error: Could not find logs for "{}"...'.format(name))
            return 4
        raise
    except exceptions.BaseAWSLogsException as ex:
        sys.stderr.write(colored("{0}\n".format(ex.hint()), "red"))
        return ex.code
    except Exception:
        import traceback
        sys.stderr.write(traceback.format_exc())
        return 1

    return 0