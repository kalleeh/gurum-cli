"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import json

from gurumcommon.clients.api_client import ApiClient
from gurumcommon.exceptions import UnknownError


class DestroyOrchestrator:

    def __init__(self, config, project):
        self.cfg = config
        self.project = project
        self.api_client = self.init_api_client()

    def init_api_client(self):
        return ApiClient(
            api_uri=self.cfg.get('default', 'api_uri'),
            id_token=self.cfg.get('default', 'id_token')
        )

    def destroy_environment(self, environment):
        print('Destroying Environment: ' + environment['name'])
        payload = {}

        payload['name'] = '{0}-{1}'.format(self.project['name'], environment['name'])

        try:
            self.api_client.delete(resource='apps', payload=json.dumps(payload))
        except Exception:
            raise UnknownError

    def destroy_pipeline(self):
        print('Destroying {0} Pipeline.'.format(self.project['source']['provider']))
        payload = {}

        payload['name'] = self.project['name']

        try:
            self.api_client.delete(resource='pipelines', payload=json.dumps(payload))
        except Exception:
            raise UnknownError

    def destroy_service(self, service):
        print('Destroying Service: ' + service['name'])
        payload = {}

        payload['name'] = '{0}-{1}'.format(self.project['name'], service['name'])

        try:
            self.api_client.delete(resource='services', payload=json.dumps(payload))
        except Exception:
            raise UnknownError
