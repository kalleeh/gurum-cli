"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import click

from botocore.client import ClientError
from gurumcli.cli.main import pass_context, common_options
from gurumcommon.logs.awslogs import AWSLogs
import gurumcommon.logs.exceptions as exceptions


@click.command('logs', short_help='Displays logs about your app')
@click.argument('name')
@click.option('--start', default='5m', help='Filter starting date/time to get logs')
@click.option('--end', help='Filter end date/time to get logs')
@click.option('--filter-pattern', help='Filter logs matching a filter pattern')
@click.option('--watch', is_flag=True, help='Follow logs')
@pass_context
@common_options
def cli(ctx, name, **kwargs):
    """View logs for your app"""
    options = {}
    log_group_name = 'platform-svc-{}'.format(name)

    # Dynamically get options and remove undefined options
    options = {k: v for k, v in kwargs.items() if v is not None}
    options['log_group_name'] = log_group_name
    options['log_stream_name'] = 'ALL'
    options['color'] = 'always'
    options['output_stream_enabled'] = True
    options['watch_interval'] = 1
    options['aws_access_key_id'] = ctx.config.get(ctx.profile, 'aws_access_key_id')
    options['aws_secret_access_key'] = ctx.config.get(ctx.profile, 'aws_secret_access_key')
    options['aws_session_token'] = ctx.config.get(ctx.profile, 'aws_session_token')
    options['aws_region'] = ctx.config.get(ctx.profile, 'region')

    try:
        logs = AWSLogs(**options)

        logs.list_logs()
    except ClientError as ex:
        code = ex.response['Error']['Code']
        if code in (u'AccessDeniedException', u'ExpiredTokenException'):
            hint = ex.response['Error'].get('Message', 'AccessDeniedException')
            click.secho("{0}\n".format(hint), fg='yellow')
            return 4
        if code in u'ResourceNotFoundException':
            click.echo('Error: Could not find logs for "{}"...'.format(name))
            return 4
        raise
    except exceptions.BaseAWSLogsException as ex:
        click.secho("{0}\n".format(ex.hint()), fg='red')
        return ex.code

    return 0
