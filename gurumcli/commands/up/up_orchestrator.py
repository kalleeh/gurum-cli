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
        except Exception as ex:
            payload['upgrade_version'] = 'False'
            self.api_client.update_app(json.dumps(payload))

    def provision_pipeline(self):
        print('Provisioning {0} Pipeline.'.format(self.project['source']['provider']))

    def provision_service(self, service):
        print('Provisioning Service: ' + service['name'])
