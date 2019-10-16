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
import gurumcommon.gurum_manifest as gurum_manifest
from .up_orchestrator import UpOrchestrator

from shutil import copyfile
from gurumcli.cli.main import pass_context, common_options

LOG = logging.getLogger(__name__)

GURUM_SKELETON_FILE = "gurum_manifest_skeleton.yaml"

@click.command(context_settings=dict(help_option_names=[u'-h', u'--help']))
@pass_context
def cli(ctx):
    """ \b
        Deploy Gurum application.
        The gurum.yaml file will be read from the directory you are executing the command.

    \b
    Common usage:

        \b
        Deploy application.
        \b
        $ gurum up
    """
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx)  # pragma: no cover


def do_cli(ctx):
    manifest = read_manifest()

    click.echo(manifest.project())

    orchestrator = UpOrchestrator(manifest.project())

    for environment in manifest.environments():
        orchestrator.provision_environment(environment)

#TODO: Make this a helper.
def read_manifest():
    click.echo("Reading gurum.yaml")
    base_dir = os.path.abspath(__file__ + "../../../../../gurumcommon")
    gurum_schema_file = os.path.join(base_dir, gurum_manifest.GURUM_SCHEMA_FILE)
    gurum_init_file = os.path.join(os.getcwd(), gurum_manifest.GURUM_FILE)
    return gurum_manifest.GurumManifest(manifest_schema_path=gurum_schema_file, manifest_path=gurum_init_file)
