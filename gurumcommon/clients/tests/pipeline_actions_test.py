# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# pylint: skip-file


from pytest import fixture, raises
from gurumcommon.clients.api_client import ApiClient


@fixture
def client():
    return ApiClient(
        api_uri='https://test.com',
        id_token='ImAToken'
    )

def test_get_pipeline_states(client):
    assert client.pipelines.get_states('MyPipeline') == ''
