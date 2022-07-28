import json

from gurumcommon.logger import configure_logger
import gurumcommon.connection_handler as connection_handler

LOGGER = configure_logger(__name__)

class EventActions():
    def __init__(self, api_uri, headers):
        self._api_uri = api_uri
        self._headers = headers

    def list(self, name):
        uri = '{0}/events/{1}'.format(self._api_uri, name)
        resp = connection_handler.request('get', uri, self._headers)
        return json.loads(resp['body'])
