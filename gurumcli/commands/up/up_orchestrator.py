import json

from gurumcommon.clients.api_client import ApiClient


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
        payload['health_check_path'] = environment['config']['health_check_path']
        payload['tasks'] = environment['config']['tasks']
        payload['image'] = 'nginx:latest'
        payload['subtype'] = self.project['type']
        payload['version'] = 'latest'

        try:
            self.api_client.create_app(json.dumps(payload))
        except Exception: #TODO: Handle different exceptions, now just assumes "already exists"
            payload['upgrade_version'] = 'False'
            self.api_client.update_app(json.dumps(payload))

        return payload['name']

    def provision_pipeline(self, environment_names, github_token):
        print('Provisioning {0} Pipeline.'.format(self.project['source']['provider']))
        payload = {}

        payload['name'] = self.project['name']

        if environment_names[0]: payload['app_dev'] = environment_names[0]
        if environment_names[1]: payload['app_name'] = environment_names[1]

        source = self.project['source']
        payload['github_branch'] = source['branch'] if 'branch' in source else 'master'
        payload['github_token'] = github_token

        source_details = self.split_user_repo(source['repo'])
        payload['github_user'] = source_details['user']
        payload['github_repo'] = source_details['repo']

        try:
            self.api_client.create_pipeline(json.dumps(payload))
        except Exception: #TODO: Handle different exceptions, now just assumes "already exists"
            payload['upgrade_version'] = 'False'
            self.api_client.update_pipeline(json.dumps(payload))

    def provision_service(self, service):
        print('Provisioning Service: ' + service['name'])

    def split_user_repo(self, user_repo_string):
        split = user_repo_string.split('/')

        return {'user': split[0], 'repo': split[1]}
