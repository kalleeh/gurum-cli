"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import os
import sys
import logging
from shutil import copyfile

import click
from gurumcli.cli.main import pass_context, common_options
import gurumcommon.gurum_manifest as gurum_manifest
from gurumcommon.github_api import validate_pat, split_user_repo
from gurumcommon.exceptions import InvalidGurumManifestError
from gurumcommon.clients.api_client import ApiClient

from .destroy_orchestrator import DestroyOrchestrator

LOGGER = logging.getLogger(__name__)

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
        $ gurum destroy
    """
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx)  # pragma: no cover


def do_cli(ctx):
    api_client = ApiClient(
        api_uri=ctx.config.get(ctx.profile, 'api_uri'),
        id_token=ctx.config.get(ctx.profile, 'id_token')
    )

    # TODO: We need to look at handling errors when there is no ~/Library/Application Support/gurum/.gurum file
    try:
        manifest = read_manifest()
    except InvalidGurumManifestError as e:
        LOGGER.debug(e)
        click.echo("Missing or invalid configuration file. Please run 'gurum init'.")
    else:
        destroy_pipeline_resources(api_client, ctx.config, manifest)

def destroy_pipeline_resources(api_client, config, manifest):
    orchestrator = DestroyOrchestrator(api_client, config, manifest.project())

    environment_names = []
    for environment in manifest.environments():
        environment_names.append(orchestrator.destroy_environment(environment))

    for service in manifest.services():
        orchestrator.destroy_service(service)

    orchestrator.destroy_pipeline()

#TODO: Make this a helper.
def read_manifest():
    click.echo("Reading gurum.yaml")
    base_dir = os.path.abspath(__file__ + "../../../../../gurumcommon")
    gurum_schema_file = os.path.join(base_dir, gurum_manifest.GURUM_SCHEMA_FILE)
    gurum_init_file = os.path.join(os.getcwd(), gurum_manifest.GURUM_FILE)
    return gurum_manifest.GurumManifest(manifest_schema_path=gurum_schema_file, manifest_path=gurum_init_file)

def get_provider(manifest):
    return manifest.project()['source']['provider'].lower()
