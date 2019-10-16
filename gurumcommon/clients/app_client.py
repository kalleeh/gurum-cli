"""
This is a sample, non-production-ready template.
© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.
This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import gurumcommon.connection_handler as connection_handler

from gurumcommon.clients.event_client import EventClient

"""
Application Client
"""

class AppClient():
    def __init__(self, api_uri, id_token):
        self._url = api_uri + '/apps'
        self._headers = {'Authorization': id_token}
        self._event_client = EventClient(api_uri, id_token)

    def create_app(self, payload):
        resp = connection_handler.request('post', self._url, self._headers, payload)

        return resp['apps']

    def describe_app(self):
        resp = connection_handler.request('get', self._url, self._headers)

        return resp['apps']

    def update_app(self, payload):
        resp = connection_handler.request('patch', self._url, self._headers, payload)

        return resp['apps']

    def delete_app(self):
        resp = connection_handler.request('delete', self._url, self._headers)

        return resp['apps']
