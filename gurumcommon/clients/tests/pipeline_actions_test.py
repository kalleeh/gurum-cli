# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# pylint: skip-file


from pytest import fixture, raises
from unittest import mock

from gurumcommon.clients.pipeline_actions import PipelineActions

from stubs import pipeline_actions_stub 

@fixture
def cls():
    return PipelineActions(
        api_uri='https://test.com',
        headers={'Authorization': 'IAmAToken'}
    )

@mock.patch('connection_handler.request', mock.MagicMock(return_value=pipeline_actions_stub.pipeline_states_response))
def test_it_gets_pipeline_states(cls):
    assert cls.get_states('MyPipeline') == pipeline_actions_stub.get_states_response

@mock.patch('connection_handler.request', mock.MagicMock(return_value=pipeline_actions_stub.pipeline_states_response))
def it_fails_to_get_pipeline_states(cls):
    mock.assert_called_once_with('other', bar='values')
    assert cls.get_states('MyPipeline') == pipeline_actions_stub.get_states_response
