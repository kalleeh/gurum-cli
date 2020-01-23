# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# pylint: skip-file

import json
import os
import boto3

from pytest import fixture, raises
from unittest import mock, TestCase
from gurumcommon.exceptions import InvalidGurumManifestError
from gurumcommon.gurum_manifest import GurumManifest
from stubs import gurum_manifest_stub

class TestGurumManifest(TestCase):
    def setUp(self):
        self.manifest = GurumManifest()

    @mock.patch('yaml.safe_load', mock.MagicMock(return_value=gurum_manifest_stub.valid_manifest))
    @mock.patch('gurumcommon.gurum_manifest.GurumManifest._validate', mock.MagicMock())
    def test_it_loads(self):
        mock_open = mock.mock_open(read_data="dummydata")

        with mock.patch('builtins.open', mock_open):
            loaded = self.manifest.load()

    @mock.patch('yaml.safe_load', mock.MagicMock(return_value=gurum_manifest_stub.valid_manifest))
    @mock.patch('gurumcommon.gurum_manifest.GurumManifest._validate', mock.MagicMock())
    def test_load_project(self):
        mock_open = mock.mock_open(read_data="dummydata")

        with mock.patch('builtins.open', mock_open):
            loaded = self.manifest.load()
            self.assertEqual(loaded.project(), gurum_manifest_stub.valid_project)

    @mock.patch('yaml.safe_load', mock.MagicMock(return_value=gurum_manifest_stub.valid_manifest))
    @mock.patch('gurumcommon.gurum_manifest.GurumManifest._validate', mock.MagicMock())
    def test_load_environments(self):
        mock_open = mock.mock_open(read_data="dummydata")

        with mock.patch('builtins.open', mock_open):
            loaded = self.manifest.load()
            self.assertEqual(loaded.environments(), gurum_manifest_stub.valid_environments)

    @mock.patch('yaml.safe_load', mock.MagicMock(return_value=gurum_manifest_stub.valid_manifest))
    @mock.patch('gurumcommon.gurum_manifest.GurumManifest._validate', mock.MagicMock())
    def test_load_services(self):
        mock_open = mock.mock_open(read_data="dummydata")

        with mock.patch('builtins.open', mock_open):
            loaded = self.manifest.load()
            self.assertEqual(loaded.services(), gurum_manifest_stub.valid_services)
