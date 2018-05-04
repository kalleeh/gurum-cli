import click
import os
import requests
import json
import sys

import boto3

from botocore.client import ClientError
from termcolor import colored
from gureume.cli import pass_context
from gureume.lib.awslogs import AWSLogs
import gureume.lib.exceptions as exceptions

@click.command('logs', short_help='Displays logs about your app')
@click.argument('name')
@click.option('--start', help='Filter starting date/time to get logs')
@click.option('--end', help='Filter end date/time to get logs')
@click.option('--filter-pattern', help='Filter logs matching a filter pattern')
@click.option('--watch', is_flag=True, help='Follow logs')
@pass_context
def cli(ctx, name, start, end, filter_pattern, watch):
    """View logs for your app"""
    options = {}
    log_group_name = name

    options['log_group_name'] = 'platform-app-{}'.format(log_group_name)
    options['log_stream_name'] = 'ALL'
    if 'start' in locals():
        options['start'] = start
    if 'end' in locals():
        options['end'] = end
    if 'watch' in locals():
        options['watch'] = watch
    if 'filter_pattern' in locals():
        options['filter_pattern'] = filter_pattern
    options['color_enabled'] = 'true'
    options['output_stream_enabled'] = 'true'
    options['output_timestamp_enabled'] = 'true'
    options['aws_access_key_id'] = ctx.config.get('default', 'aws_access_key_id')
    options['aws_secret_access_key'] = ctx.config.get('default', 'aws_secret_access_key')
    options['aws_session_token'] = ctx.config.get('default', 'aws_session_token')
    options['aws_region'] = ctx.config.get('default', 'aws_region')

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