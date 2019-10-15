"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import json

import utils.connection_handler
import config

from logger import configure_logger

LOGGER = configure_logger(__name__)


"""
Event Client
"""


class EventClient():
    def __init__(self):
        self._url = config.api_uri + '/events'
        self._headers = {'Authorization': config.id_token}

    def list_events(self, name):
        # Get CloudFormation Events
        self._url = self._url + name

        resp = connection_handler.request('get', self._url, self._headers)

        return resp['events']
