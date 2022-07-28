
import sys
import logging
import click

from gurumcommon.logger import configure_logger
from gurumcli import __version__
from .options import debug_option, profile_option
from .context import Context
from .command import BaseCommand

LOGGER = configure_logger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger('keyring').setLevel(logging.WARNING)

pass_context = click.make_pass_decorator(Context)


def common_options(f):
    """
    Common CLI options used by all commands. Ex: --debug
    :param f: Callback function passed by Click
    :return: Callback function
    """
    f = debug_option(f)
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
