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

from gurumcommon.clients.api_client import ApiClient
from gurumcli.lib.utils.github_api import split_user_repo


class UpOrchestrator:

    def __init__(self, config, project):
        self.config = config
        self.project = project
        self.api_client = self.init_api_client()

    def init_api_client(self):
        return ApiClient(
            api_uri=self.config.get('default', 'api_uri'),
            id_token=self.config.get('default', 'id_token')
        )

    def provision_environment(self, environment):
        print('Provisioning Environment: ' + environment['name'])
        payload = {}

        payload['name'] = '{0}-{1}'.format(self.project['name'], environment['name'])
        payload['config'] = environment['config']
        payload['env_vars'] = environment['env_vars']

        try:
            self.api_client.create(resource='apps', payload=json.dumps(payload))
        except AlreadyExistsError:
            payload['upgrade_version'] = 'False'
            try:
                self.api_client.update(resource='apps', payload=json.dumps(payload))
            except UnknownParameterError as ex:
                print(ex)

        return payload['name']

    def provision_pipeline(self, environment_names, github_token):
        print('Provisioning {0} Pipeline.'.format(self.project['source']['provider']))
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
            self.api_client.create(resource='pipelines', payload=json.dumps(payload))
        except AlreadyExistsError:
            payload['upgrade_version'] = 'False'
            try:
                self.api_client.update(resource='pipelines', payload=json.dumps(payload))
            except UnknownParameterError as ex:
                print(ex)

    def provision_service(self, service):
        print('Provisioning Service: ' + service['name'])
        payload = {}

        payload['name'] = '{0}-{1}'.format(self.project['name'], service['name'])
        payload['type'] = service['type']
        payload['config'] = service['config']

        try:
            self.api_client.create(resource='services', payload=json.dumps(payload))
        except AlreadyExistsError:
            payload['upgrade_version'] = 'False'
            try:
                self.api_client.update(resource='services', payload=json.dumps(payload))
            except UnknownParameterError as ex:
                print(ex)

        return payload['name']
