import os
import sys
import logging
from shutil import copyfile

import click
import requests
import boto3
import botocore

from termcolor import colored
from warrant import Cognito, exceptions

import gurumcommon.gurum_manifest as gurum_manifest
from gurumcli.cli.main import pass_context, common_options

LOG = logging.getLogger(__name__)

GURUM_SKELETON_FILE = "gurum_manifest_skeleton.yaml"

@click.command(context_settings=dict(help_option_names=[u'-h', u'--help']))
@pass_context
def cli(ctx):
    """ \b
        Initialise GURUM.
        This will look for gurum.yaml file in the directory you are executing the command.

    \b
    Common usage:

        \b
        Initialise GURUM.
        \b
        $ gurum init
    """
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx)  # pragma: no cover


def do_cli(ctx):
    base_dir = os.path.abspath(__file__ + "../../../../../gurumcommon")

    skeleton_file = os.path.join(base_dir, GURUM_SKELETON_FILE)

    if not os.path.isfile(skeleton_file) or not os.access(skeleton_file, os.R_OK):
        raise click.ClickException('Invalid command: {}'.format("skeleton not found or unable to access " + skeleton_file))

    gurum_init_file = os.path.join(os.getcwd(), gurum_manifest.GURUM_FILE)

    gurum_schema_file = os.path.join(base_dir, gurum_manifest.GURUM_SCHEMA_FILE)

    if os.path.isfile(gurum_init_file) and os.access(gurum_init_file, os.R_OK):
        click.echo("Found " + gurum_init_file)
    else:
        copyfile(skeleton_file, gurum_init_file)
        click.echo("Initialised from skeleton!")

    # validate schema
    gurum_manifest.GurumManifest()

    click.echo('Initialised!')
