

class UpOrchestrator:

    def __init__(self, project):
        self.project = project

    def provision_environment(self, environment):
        print('Provisioning Environment: ' + environment['name'])

    def provision_service(self, service):
        print('Provisioning Service: ' + service['name']) 