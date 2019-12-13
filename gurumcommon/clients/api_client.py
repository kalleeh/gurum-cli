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

from gurumcommon.exceptions import BadRequestError, AlreadyExistsError, UnknownParameterError, UnknownError
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
        except AlreadyExistsError:
            raise
        except Exception as ex:
            print(ex)
        else:
            return json.loads(resp['body'])['apps']

    def describe_app(self):
        resp = connection_handler.request('get', self._app_url, self._headers)

        return resp['apps']

    def update_app(self, payload):
        data = json.loads(payload)
        uri = '{0}/{1}'.format(self._app_url, data['name'])

        try:
            resp = connection_handler.request('patch', uri, self._headers, payload)
        except BadRequestError:
            raise UnknownParameterError
        else:
            return json.loads(resp['body'])

    def delete_app(self):
        resp = connection_handler.request('delete', self._app_url, self._headers)

        return resp['apps']


    def create_pipeline(self, payload):
        try:
            resp = connection_handler.request('post', self._pipeline_url, self._headers, payload)
        except Exception:
            raise
        else:
            return json.loads(resp['body'])['pipelines']

    def describe_pipeline(self):
        resp = connection_handler.request('get', self._pipeline_url, self._headers)

        return resp['pipelines']

    def update_pipeline(self, payload):
        data = json.loads(payload)
        uri = '{0}/{1}'.format(self._pipeline_url, data['name'])

        try:
            resp = connection_handler.request('patch', uri, self._headers, payload)
        except BadRequestError:
            raise UnknownParameterError
        else:
            return json.loads(resp['body'])['pipelines']

    def delete_pipeline(self):
        resp = connection_handler.request('delete', self._pipeline_url, self._headers)

        return resp['pipelines']


    def create_service(self, payload):
        try:
            resp = connection_handler.request('post', self._service_url, self._headers, payload)
        except AlreadyExistsError:
            raise
        except Exception as ex:
            print(ex)
        else:
            return json.loads(resp['body'])['services']

    def describe_service(self):
        resp = connection_handler.request('get', self._service_url, self._headers)

        return resp['services']

    def update_service(self, payload):
        data = json.loads(payload)
        uri = '{0}/{1}'.format(self._service_url, data['name'])

        try:
            resp = connection_handler.request('patch', uri, self._headers, payload)
        except BadRequestError:
            raise UnknownParameterError
        else:
            return json.loads(resp['body'])

    def delete_service(self):
        resp = connection_handler.request('delete', self._service_url, self._headers)

        return resp['services']