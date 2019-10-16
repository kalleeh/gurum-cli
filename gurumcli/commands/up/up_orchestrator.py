from gurumcommon.clients.app_client import AppClient

class UpOrchestrator:

    def __init__(self, config, project):
        self.config = config
        self.project = project
        self.app_client = self.init_app_client(config)

    def init_app_client(self, config):
        return AppClient(
            api_uri = config.get('default', 'api_uri'),
            id_token = config.get('default', 'id_token')
        )

    def provision_environment(self, environment):
        print('Provisioning Environment: ' + environment['name'])

        payload = {}

        # self.app_client.create_app(payload)

    def provision_service(self, service):
        print('Provisioning Service: ' + service['name']) 