"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import json

from gurumcommon.exceptions import UnknownError
from gurumcommon.logger import configure_logger

LOGGER = configure_logger(__name__)

class DownOrchestrator:

    def __init__(self, api_client, config, project):
        self.cfg = config
        self.project = project
        self.api_client = api_client

    def down_environment(self, environment):
        LOGGER.info('Destroying Environment: %s', environment['name'])
        payload = {}

        payload['name'] = '{0}-{1}'.format(self.project['name'], environment['name'])

        try:
            self.api_client.apps.delete(payload['name'])
        except Exception:
            raise UnknownError

    def down_pipeline(self):
        LOGGER.info('Destroying %s Pipeline.', format(self.project['source']['provider']))
        payload = {}

        payload['name'] = self.project['name']

        try:
            self.api_client.pipelines.delete(payload['name'])
        except Exception:
            raise UnknownError

    def down_service(self, service):
        LOGGER.info('Destroying Service: %s', service['name'])
        payload = {}

        payload['name'] = '{0}-{1}'.format(self.project['name'], service['name'])

        try:
            self.api_client.services.delete(payload['name'])
        except Exception:
            raise UnknownError
