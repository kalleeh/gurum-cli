# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# pylint: skip-file

import os

from pytest import fixture, raises

from exceptions import UnknownError, ServerError, UrlNotFoundError, AuthenticationError, BadRequestError, UnexpectedRedirectError
import connection


def test_invalid_url():
    url = 'https://myinvaliddomain.com/apps'
    headers = {'Authorization': '123456789'}
    payload = '{0}/stubs/connection_apps_create_stub.json'.format(
            os.path.dirname(os.path.realpath(__file__))
        )

    with raises(UrlNotFoundError):
        connection.request('post', url, headers, payload)
