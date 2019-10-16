"""
This is a sample, non-production-ready template.
© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.
This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import gurumcommon.connection_handler as connection_handler

"""
Event Client
"""


class EventClient():
    def __init__(self, api_uri, id_token):
        self._url = api_uri + '/events'
        self._headers = {'Authorization': id_token}

    def list_events(self, name):
        # Get CloudFormation Events
        self._url = self._url + name

        resp = connection_handler.request('get', self._url, self._headers)

        return resp['events']
