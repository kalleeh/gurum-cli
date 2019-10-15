"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import logging
import click
import os,sys
import requests
import boto3
import botocore
import gurumcommon.gurum_manifest as gurum_manifest

from shutil import copyfile
from termcolor import colored
from warrant import Cognito, exceptions
from gurumcli.cli.main import pass_context, common_options
from gurumcli.commands.exceptions import UserException

LOG = logging.getLogger(__name__)

GURUM_SKELETON_FILE = "gurum_manifest_skeleton_stub.yaml"

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
    
    base_dir = os.getcwd()

    skeleton_file = os.path.join(base_dir, "gurumcommon", GURUM_SKELETON_FILE)

    if not os.path.isfile(skeleton_file) or not os.access(skeleton_file, os.R_OK):
        raise click.ClickException('Invalid command: {}'.format("skeleton not found or unable to access " + skeleton_file))

    gurum_init_file = os.path.join(base_dir, "gurumcommon", gurum_manifest.GURUM_FILE)

    gurum_schema_file = os.path.join(base_dir, "gurumcommon", gurum_manifest.GURUM_SCHEMA_FILE)
   

    if os.path.isfile(gurum_init_file) and os.access(gurum_init_file, os.R_OK):
        click.echo("Found " + gurum_init_file)
    else:
        copyfile(skeleton_file, gurum_init_file)
        click.echo("Initialised from skeleton!")

    # validate schema
    gurum_manifest.GurumManifest(
            manifest_schema_path=gurum_schema_file,
            manifest_path=gurum_init_file
    )

    click.echo('Initialised!')
