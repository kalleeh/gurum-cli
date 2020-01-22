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

class EventActions():
    def __init__(self, api_uri, headers):
        self._api_uri = api_uri
        self._headers = headers

    def list(self, name):
        uri = '{0}/events/{1}'.format(self._api_uri, name)
        resp = connection_handler.request('get', uri, self._headers)
        return json.loads(resp['body'])
