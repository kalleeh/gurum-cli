"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import sys
import click

from botocore.client import ClientError
from termcolor import colored
from gurumcli.cli.main import pass_context, common_options
from gurumcli.lib.logs.awslogs import AWSLogs
import gurumcommon.exceptions as exceptions


@click.command('logs', short_help='Displays logs about your pipeline')
@click.argument('name')
@click.option('--start', default='5m', help='Filter starting date/time to get logs')
@click.option('--end', help='Filter end date/time to get logs')
@click.option('--filter-pattern', help='Filter logs matching a filter pattern')
@click.option('--watch', is_flag=True, help='Follow logs')
@pass_context
@common_options
def cli(ctx, name, **kwargs):
    """ \b
        View logs for your build job. Supports multiple options for watching logs, filtering patterns and time options.
        Wrapper for https://github.com/jorgebastida/awslogs

    \b
    Common usage:

        \b
        Logs in to the platform.
        \b
        $ gurum pipelines logs myPipeline

    \b
    Filter options:

        \b
        You can use --filter-pattern if you want to only retrieve logs which match one CloudWatch Logs Filter pattern.
        This is helpful if you know precisely what you are looking for, and don't want to download the entire stream.

        \b
        $ gurum pipelines logs myPipeline --filter-pattern="[r=REPORT,...]"
        Full documentation of how to write patterns: http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/FilterAndPatternSyntax.html

    \b
    Time options:

        \b
        While querying for logs you can filter events by --start -s and --end -e date.

        \b
        By minute:

        \b
        --start='2m' Events generated two minutes ago.
        --start='1 minute' Events generated one minute ago.
        --start='5 minutes' Events generated five minutes ago.

        \b
        By hours:

        \b
        --start='2h' Events generated two hours ago.
        --start='1 hour' Events generated one hour ago.
        --start='5 hours' Events generated five hours ago.

        \b
        By days:

        \b
        --start='2d' Events generated two days ago.
        --start='1 day' Events generated one day ago.
        --start='5 days' Events generated five days ago.

        \b
        By weeks:

        \b
        --start='2w' Events generated two week ago.
        --start='1 week' Events generated one weeks ago.
        --start='5 weeks' Events generated five week ago.

        \b
        Using specific dates:

        \b
        --start='23/1/2015 12:00' Events generated after midday on the 23th of January 2015.
        --start='1/1/2015' Events generated after midnight on the 1st of January 2015.
        --start='Sat Oct 11 17:13:46 UTC 2003' You can use detailed dates too.
    """
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx, name, **kwargs)  # pragma: no cover


def do_cli(ctx, name, **kwargs):
    """View logs for your pipeline"""
    options = {}
    log_group_name = name

    # Dynamically get options and remove undefined options
    options = {k: v for k, v in kwargs.items() if v is not None}
    options['log_group_name'] = '/aws/codebuild/gurum-{}'.format(log_group_name)
    options['log_stream_name'] = 'ALL'
    options['color_enabled'] = 'true'
    options['output_stream_enabled'] = 'true'
    options['output_timestamp_enabled'] = 'true'
    options['aws_access_key_id'] = ctx.config.get('default', 'aws_access_key_id')
    options['aws_secret_access_key'] = ctx.config.get('default', 'aws_secret_access_key')
    options['aws_session_token'] = ctx.config.get('default', 'aws_session_token')
    options['aws_region'] = ctx.config.get('default', 'region')

    try:
        logs = AWSLogs(**options)

        logs.list_logs()
    except ClientError as ex:
        code = ex.response['Error']['Code']
        if code in (u'AccessDeniedException', u'ExpiredTokenException'):
            hint = ex.response['Error'].get('Message', 'AccessDeniedException')
            sys.stderr.write(colored("{0}\n".format(hint), "yellow"))
            return 4
        if code in u'ResourceNotFoundException':
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
