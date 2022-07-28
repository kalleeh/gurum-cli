import json

from gurumcommon.logger import configure_logger
import gurumcommon.connection_handler as connection_handler

LOGGER = configure_logger(__name__)

class ServiceActions():
    def __init__(self, api_uri, headers):
        self._api_uri = api_uri
        self._headers = headers

    def list(self):
        uri = '{0}/services/'.format(self._api_uri)
        resp = connection_handler.request('get', uri, self._headers)
        return json.loads(resp['body'])

    def create(self, payload):
        uri = '{0}/services/'.format(self._api_uri)
        resp = connection_handler.request('post', uri, self._headers, payload)
        return json.loads(resp['body'])['services']

    def describe(self, name):
        uri = '{0}/services/{1}'.format(self._api_uri, name)
        resp = connection_handler.request('get', uri, self._headers)
        return json.loads(resp['body'])

    def update(self, name, payload):
        uri = '{0}/services/{1}'.format(self._api_uri, name)
        resp = connection_handler.request('patch', uri, self._headers, payload)
        return json.loads(resp['body'])

    def delete(self, name):
        uri = '{0}/services/{1}'.format(self._api_uri, name)
        connection_handler.request('delete', uri, self._headers)
        return {}
