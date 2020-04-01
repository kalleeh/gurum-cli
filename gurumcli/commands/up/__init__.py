"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import os
import logging

import click

from gurumcli.cli.main import pass_context, common_options
import gurumcommon.gurum_manifest as gurum_manifest
from gurumcommon.github_api import validate_pat, split_user_repo
from gurumcommon.keyring_api import get_github_secret, set_github_secret
from gurumcommon.exceptions import InvalidGurumManifestError, GurumManifestNotFoundError, InvalidPersonalAccessTokenError, RepositoryNotFoundError
from gurumcommon.clients.api_client import ApiClient
from gurumcommon.logger import configure_logger

from .up_orchestrator import UpOrchestrator

LOGGER = configure_logger(__name__)

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
    api_client = ApiClient(
        api_uri=ctx.config.get(ctx.profile, 'api_uri'),
        id_token=ctx.config.get(ctx.profile, 'id_token')
    )

    try:
        manifest = gurum_manifest.GurumManifest().load()
    except InvalidGurumManifestError as e:
        LOGGER.error(e)
        click.echo("Invalid configuration file.")
    except GurumManifestNotFoundError as e:
        LOGGER.error(e)
        click.echo("Missing or invalid configuration file. Please run 'gurum init'.")
    else:
        provision_pipeline_resources(api_client, ctx.config, manifest)

def provision_pipeline_resources(api_client, config, manifest):
    orchestrator = UpOrchestrator(api_client, config, manifest.project())
    repository = manifest.project()['source']['repo']

    environment_names = []
    for environment in manifest.environments():
        orchestrator.provision_environment(environment)
        environment_names.append('{}-{}'.format(manifest.project()['name'], environment['name']))

    for service in manifest.services():
        orchestrator.provision_service(service)

    if get_provider(manifest).startswith('github'):
        github_token = get_github_requirements(repository)
        orchestrator.provision_pipeline(environment_names, github_token)

def get_provider(manifest):
    return manifest.project()['source']['provider'].lower()

def get_github_requirements(repository):
    github_token = get_github_secret(repository)
    source = split_user_repo(repository)

    while True:
        try:
            validate_pat(github_token, source['user'], source['repo'])

            LOGGER.debug('Personal Access Token valid. Saving to keyring...')
            set_github_secret(repository, github_token)

            return github_token
        except InvalidPersonalAccessTokenError as ex:
            click.echo("Error: {}".format(ex.message))
            LOGGER.debug('GitHub Token invalid or not found in keyring. Prompting user...')
            github_token = click.prompt('Please enter your GitHub Personal Access Token', hide_input=True)
        except RepositoryNotFoundError as ex:
            click.echo("Error: {}".format(ex.message))

    return False
