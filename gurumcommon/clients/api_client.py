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


class ApiClient():
    def __init__(self, api_uri, id_token):
        self._api_uri = api_uri
        self._headers = {'Authorization': id_token}

    def list(self, resource):
        uri = '{0}{1}'.format(self._api_uri, resource)

        resp = connection_handler.request('get', uri, self._headers)

        return json.loads(resp['body'])

    def create(self, resource, payload):
        uri = '{0}{1}'.format(self._api_uri, resource)

        resp = connection_handler.request('post', uri, self._headers, payload)

        return json.loads(resp['body'])[resource]

    def describe(self, resource, payload):
        data = json.loads(payload)
        uri = '{0}{1}/{2}'.format(self._api_uri, resource, data['name'])

        resp = connection_handler.request('get', uri, self._headers)

        return json.loads(resp['body'])

    def update(self, resource, payload):
        data = json.loads(payload)
        uri = '{0}{1}/{2}'.format(self._api_uri, resource, data['name'])

        resp = connection_handler.request('patch', uri, self._headers, payload)

        return json.loads(resp['body'])

    def delete(self, resource, payload):
        data = json.loads(payload)
        uri = '{0}{1}/{2}'.format(self._api_uri, resource, data['name'])

        connection_handler.request('delete', uri, self._headers)

        return {}
