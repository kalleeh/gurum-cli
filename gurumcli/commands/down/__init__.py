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
from gurumcommon.logger import configure_logger

from .down_orchestrator import DownOrchestrator

LOGGER = configure_logger(__name__)

@click.command(context_settings=dict(help_option_names=[u'-h', u'--help']))
@pass_context
def cli(ctx):
    """ \b
        Destroy Gurum application.
        The gurum.yaml file will be read from the directory you are executing the command.

    \b
    Common usage:

        \b
        Destroy application.
        WARNING: This is a irreversible destructive operation.
        \b
        $ gurum down
    """
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx)  # pragma: no cover


def do_cli(ctx):
    api_client = ApiClient(
        api_uri=ctx.config.get(ctx.profile, 'api_uri'),
        id_token=ctx.config.get(ctx.profile, 'id_token')
    )

    click.confirm('Destroy the application and all its environments (including CI/CD)? \
        (WARNING: This is a irreversible destructive operation)', abort=True)

    try:
        manifest = gurum_manifest.GurumManifest().load()
    except InvalidGurumManifestError as e:
        LOGGER.debug(e)
        click.echo("Missing or invalid configuration file. Please run 'gurum init'.")
    else:
        down_pipeline_resources(api_client, ctx.config, manifest)

def down_pipeline_resources(api_client, config, manifest):
    orchestrator = DownOrchestrator(api_client, config, manifest.project())

    environment_names = []
    for environment in manifest.environments():
        environment_names.append(orchestrator.down_environment(environment))

    for service in manifest.services():
        orchestrator.down_service(service)

    orchestrator.down_pipeline()

def get_provider(manifest):
    return manifest.project()['source']['provider'].lower()
