"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""


import sys
import logging
import click

from gurumcli import __version__
from .options import debug_option, config_option, region_option, profile_option
from .context import Context
from .command import BaseCommand

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


pass_context = click.make_pass_decorator(Context)


def common_options(f):
    """
    Common CLI options used by all commands. Ex: --debug
    :param f: Callback function passed by Click
    :return: Callback function
    """
    f = debug_option(f)
    f = config_option(f)
    return f


def aws_creds_options(f):
    """
    Common CLI options necessary to interact with AWS services
    """
    f = region_option(f)
    f = profile_option(f)
    return f


@click.command(cls=BaseCommand)
@common_options
@click.version_option(version=__version__, prog_name="GURUM CLI")
@pass_context
def cli(_ctx):
    """
    AWS Gurum Platform (GURUM) CLI

    The AWS Gurum Platform extends AWS Container Services to provide a simplified way of managing container
    applications on Elastic Container Service, AWS CodePipeline, and other services needed by your container application.
    You can find more in-depth guide about the GURUM specification here:
    https://github.com/kalleeh/gurum-platform.
    """
    pass

if getattr(sys, 'frozen', False):
    cli(sys.argv[1:])
