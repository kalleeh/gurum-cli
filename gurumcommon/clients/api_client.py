"""
This is a sample, non-production-ready template.
© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.
This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import json

import gurumcommon.connection_handler as connection_handler

from gurumcommon.clients.event_client import EventClient

"""
Gurum API Client
"""

class ApiClient():
    def __init__(self, api_uri, id_token):
        self._url = api_uri + 'apps'
        self._headers = {'Authorization': id_token}
        self._event_client = EventClient(api_uri, id_token)

    def create_app(self, payload):
        try:
            resp = connection_handler.request('post', self._url, self._headers, payload)
        except Exception:
            raise
        else:
            return resp['apps']

    def describe_app(self):
        resp = connection_handler.request('get', self._url, self._headers)

        return resp['apps']

    def update_app(self, payload):
        data = json.loads(payload)
        uri = '{0}/{1}'.format(self._url, data['name'])

        try:
            resp = connection_handler.request('patch', uri, self._headers, payload)
        except Exception as ex:
            print(ex)
        else:
            return resp['apps']

    def delete_app(self):
        resp = connection_handler.request('delete', self._url, self._headers)

        return resp['apps']
