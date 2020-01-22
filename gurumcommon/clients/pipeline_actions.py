"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import json

from gurumcommon.logger import configure_logger
import gurumcommon.connection_handler as connection_handler

LOGGER = configure_logger(__name__)

class PipelineActions():
    def __init__(self, api_uri, headers):
        self._api_uri = api_uri
        self._headers = headers

    def list(self):
        uri = '{0}/pipelines/'.format(self._api_uri)
        resp = connection_handler.request('get', uri, self._headers)
        return json.loads(resp['body'])

    def create(self, payload):
        uri = '{0}/pipelines/'.format(self._api_uri)
        resp = connection_handler.request('post', uri, self._headers, payload)
        return json.loads(resp['body'])['pipelines']

    def describe(self, name):
        uri = '{0}/pipelines/{1}'.format(self._api_uri, name)
        resp = connection_handler.request('get', uri, self._headers)
        return json.loads(resp['body'])

    def update(self, name, payload):
        uri = '{0}/pipelines/{1}'.format(self._api_uri, name)
        resp = connection_handler.request('patch', uri, self._headers, payload)
        return json.loads(resp['body'])

    def delete(self, name):
        uri = '{0}/pipelines/{1}'.format(self._api_uri, name)
        connection_handler.request('delete', uri, self._headers)
        return {}

    def get_states(self, name):
        uri = '{0}/pipelines/{1}/states'.format(self._api_uri, name)
        resp = connection_handler.request('get', uri, self._headers)
        return json.loads(resp['body'])

    def put_approval(self, name, approval_response, approval_message):
        uri = '{0}/pipelines/{1}/states'.format(self._api_uri, name)

        payload = {
            'status': approval_response,
            'summary': approval_message
        }

        resp = connection_handler.request('put', uri, self._headers, json.dumps(payload))
        return json.loads(resp['body'])
