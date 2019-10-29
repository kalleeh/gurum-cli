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

from gurumcommon.exceptions import BadRequestError, AlreadyExistsException, UnknownError
from gurumcommon.clients.event_client import EventClient

"""
Gurum API Client
"""

class ApiClient():
    def __init__(self, api_uri, id_token):
        self._app_url = api_uri + 'apps'
        self._pipeline_url = api_uri + 'pipelines'
        self._service_url = api_uri + 'services'
        self._headers = {'Authorization': id_token}
        self._event_client = EventClient(api_uri, id_token)

    def create_app(self, payload):
        try:
            resp = connection_handler.request('post', self._app_url, self._headers, payload)
        except Exception as ex:
            print(ex)
        else:
            """ Handling of custom Lambda errors until native passthrough
            is updated in API Gateway configuration """
            if 'statusCode' in resp and resp['statusCode'] == 200:
                return json.loads(resp['body'])['apps']
            if 'statusCode' in resp and resp['statusCode'] == 400:
                raise AlreadyExistsException

    def describe_app(self):
        resp = connection_handler.request('get', self._app_url, self._headers)

        return resp['apps']

    def update_app(self, payload):
        data = json.loads(payload)
        uri = '{0}/{1}'.format(self._app_url, data['name'])

        try:
            resp = connection_handler.request('patch', uri, self._headers, payload)
        except Exception as ex:
            print(ex)
        else:
            """ Handling of custom Lambda errors until native passthrough
            is updated in API Gateway configuration """
            if 'statusCode' in resp and resp['statusCode'] == 200:
                return json.loads(resp['body'])['apps']
            if 'statusCode' in resp and resp['statusCode'] == 400:
                raise AlreadyExistsException

    def delete_app(self):
        resp = connection_handler.request('delete', self._app_url, self._headers)

        return resp['apps']


    def create_pipeline(self, payload):
        try:
            resp = connection_handler.request('post', self._pipeline_url, self._headers, payload)
        except Exception as ex:
            print(ex)
        else:
            return resp['pipelines']

    def describe_pipeline(self):
        resp = connection_handler.request('get', self._pipeline_url, self._headers)

        return resp['pipelines']

    def update_pipeline(self, payload):
        data = json.loads(payload)
        uri = '{0}/{1}'.format(self._pipeline_url, data['name'])

        try:
            resp = connection_handler.request('patch', uri, self._headers, payload)
        except Exception as ex:
            print(ex)
        else:
            return resp['pipelines']

    def delete_pipeline(self):
        resp = connection_handler.request('delete', self._pipeline_url, self._headers)

        return resp['pipelines']
