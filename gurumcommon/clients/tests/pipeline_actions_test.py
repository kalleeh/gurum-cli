# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# pylint: skip-file


from pytest import fixture, raises
from unittest import mock
import json

from gurumcommon.clients.pipeline_actions import PipelineActions
from stubs import pipeline_actions_stub 

@fixture
def cls():
    return PipelineActions(
        api_uri='https://test.com',
        headers={'Authorization': 'IAmAToken'}
    )

def test_it_fails_to_get_pipeline_states(cls):
    with mock.patch('gurumcommon.connection_handler.request', mock.MagicMock(return_value=pipeline_actions_stub.valid_connection_handler_raw_response)) as mock_request:
        expected_method = 'get'
        expected_uri = 'https://test.com/pipelines/MyPipeline/states'
        expected_headers = {'Authorization': 'IAmAToken'}

        result = cls.get_states('MyPipeline')

        assert result == pipeline_actions_stub.valid_pipeline_actions_get_states_response
        # assert mock_request.assert_called_once_with(expected_method, expected_uri, expected_headers)
