import json

from gurumcommon.exceptions import AlreadyExistsError, BadRequestError, UnknownParameterError

from gurumcommon.clients.api_client import ApiClient


class DestroyOrchestrator:

    def __init__(self, config, project):
        self.config = config
        self.project = project
        self.api_client = self.init_api_client(config)

    def init_api_client(self, config):
        return ApiClient(
            api_uri = config.get('default', 'api_uri'),
            id_token = config.get('default', 'id_token')
        )

    def destroy_environment(self, environment):
        print('Destroying Environment: ' + environment['name'])
        payload = {}

        payload['name'] = '{0}-{1}'.format(self.project['name'], environment['name'])

        try:
            self.api_client.delete(resource='apps', payload=json.dumps(payload))
        except Exception:
            raise

    def destroy_pipeline(self):
        print('Destroying {0} Pipeline.'.format(self.project['source']['provider']))
        payload = {}

        payload['name'] = self.project['name']

        try:
            self.api_client.delete(resource='pipelines', payload=json.dumps(payload))
        except Exception:
            raise

    def destroy_service(self, service):
        print('Destroying Service: ' + service['name'])
        payload = {}

        payload['name'] = '{0}-{1}'.format(self.project['name'], service['name'])

        try:
            self.api_client.delete(resource='services', payload=json.dumps(payload))
        except Exception:
            raise
