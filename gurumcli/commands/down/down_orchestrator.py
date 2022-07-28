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

        name = '{0}-{1}'.format(self.project['name'], environment['name'])

        try:
            self.api_client.apps.delete(name)
        except Exception:
            raise UnknownError

    def down_pipeline(self):
        LOGGER.info('Destroying %s Pipeline.', format(self.project['source']['provider']))

        try:
            self.api_client.pipelines.delete(self.project['name'])
        except Exception:
            raise UnknownError

    def down_service(self, service):
        LOGGER.info('Destroying Service: %s', service['name'])

        name = '{0}-{1}'.format(self.project['name'], service['name'])

        try:
            self.api_client.services.delete(name)
        except Exception:
            raise UnknownError
