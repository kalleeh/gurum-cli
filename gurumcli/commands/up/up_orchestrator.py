"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import json

from gurumcommon.exceptions import AlreadyExistsError, UnknownParameterError
from gurumcommon.github_api import split_user_repo
from gurumcommon.logger import configure_logger

LOGGER = configure_logger(__name__)


class UpOrchestrator:

    def __init__(self, api_client, config, project):
        self.cfg = config
        self.project = project
        self.api_client = api_client

    def provision_environment(self, environment):
        LOGGER.info('Provisioning Environment: %s', environment['name'])
        payload = {}

        payload['name'] = '{0}-{1}'.format(self.project['name'], environment['name'])
        payload['product_flavor'] = self.project['type']
        payload['config'] = environment['config']
        payload['env_vars'] = environment['env_vars']

        try:
            self.api_client.apps.create(payload=json.dumps(payload))
        except AlreadyExistsError:
            LOGGER.info('%s already exists. Updating...', environment['name'])
            payload['upgrade_version'] = 'False'
            try:
                self.api_client.apps.update(name=payload['name'], payload=json.dumps(payload))
            except UnknownParameterError as ex:
                LOGGER.warning(ex)

        return payload['name']

    def provision_pipeline(self, environment_names, github_token):
        LOGGER.info('Provisioning %s Pipeline.', self.project['source']['provider'])
        payload = {}

        payload['name'] = self.project['name']

        payload['environments'] = environment_names

        source = self.project['source']
        payload['source'] = {}
        payload['source']['GitHubBranch'] = source['branch'] if 'branch' in source else 'master'
        payload['source']['GitHubToken'] = github_token

        source_details = split_user_repo(source['repo'])
        payload['source']['GitHubUser'] = source_details['user']
        payload['source']['GitHubRepo'] = source_details['repo']

        try:
            self.api_client.pipelines.create(payload=json.dumps(payload))
        except AlreadyExistsError:
            LOGGER.info('Pipeline already exists. Updating...')
            payload['upgrade_version'] = 'False'
            try:
                self.api_client.pipelines.update(name=self.project['name'], payload=json.dumps(payload))
            except UnknownParameterError as ex:
                LOGGER.warning(ex)

    def provision_service(self, service):
        LOGGER.info('Provisioning Service: %s', service['name'])
        payload = {}

        payload['name'] = '{0}-{1}'.format(self.project['name'], service['name'])
        payload['product_flavor'] = service['type']
        if 'config' in service:
            payload['config'] = service['config']

        try:
            self.api_client.services.create(payload=json.dumps(payload))
        except AlreadyExistsError:
            LOGGER.info('%s already exists. Updating...', service['name'])
            payload['upgrade_version'] = 'False'
            try:
                self.api_client.services.update(name=payload['name'], payload=json.dumps(payload))
            except UnknownParameterError as ex:
                LOGGER.warning(ex)

        return payload['name']
