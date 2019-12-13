import json

from gurumcommon.exceptions import AlreadyExistsError, BadRequestError, UnknownParameterError

from gurumcommon.clients.api_client import ApiClient
from gurumcli.lib.utils.github_api import split_user_repo


class UpOrchestrator:

    def __init__(self, config, project):
        self.config = config
        self.project = project
        self.api_client = self.init_api_client(config)

    def init_api_client(self, config):
        return ApiClient(
            api_uri = config.get('default', 'api_uri'),
            id_token = config.get('default', 'id_token')
        )

    def provision_environment(self, environment):
        print('Provisioning Environment: ' + environment['name'])
        payload = {}

        payload['name'] = '{0}-{1}'.format(self.project['name'], environment['name'])
        payload['config'] = environment['config']
        payload['env_vars'] = environment['env_vars']

        try:
            self.api_client.create_app(json.dumps(payload))
        except AlreadyExistsError:
            payload['upgrade_version'] = 'False'
            try:
                self.api_client.update_app(json.dumps(payload))
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
            self.api_client.create_pipeline(json.dumps(payload))
        except AlreadyExistsError:
            payload['upgrade_version'] = 'False'
            try:
                self.api_client.update_pipeline(json.dumps(payload))
            except UnknownParameterError as ex:
                print(ex)

    def provision_service(self, service):
        print('Provisioning Service: ' + service['name'])
        payload = {}

        payload['name'] = '{0}-{1}'.format(self.project['name'], service['name'])
        payload['type'] = service['type']
        payload['config'] = service['config']

        try:
            self.api_client.create_service(json.dumps(payload))
        except AlreadyExistsError:
            payload['upgrade_version'] = 'False'
            try:
                self.api_client.update_service(json.dumps(payload))
            except UnknownParameterError as ex:
                print(ex)

        return payload['name']
