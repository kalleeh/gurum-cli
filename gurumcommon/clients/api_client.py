"""
This is a sample, non-production-ready template.
© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.
This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

from gurumcommon.clients.app_actions import AppActions
from gurumcommon.clients.event_actions import EventActions
from gurumcommon.clients.pipeline_actions import PipelineActions
from gurumcommon.clients.service_actions import ServiceActions


class ApiClient():
    def __init__(self, api_uri, id_token):
        self._api_uri = api_uri
        self._headers = {'Authorization': id_token}
        self.apps = AppActions(self._api_uri, self._headers)
        self.events = EventActions(self._api_uri, self._headers)
        self.pipelines = PipelineActions(self._api_uri, self._headers)
        self.services = ServiceActions(self._api_uri, self._headers)
