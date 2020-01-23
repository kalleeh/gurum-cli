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
    @mock.patch('builtins.open', mock.MagicMock())
    @mock.patch('gurumcommon.gurum_manifest.GurumManifest._validate', mock.MagicMock())
    def test_it_loads(self):
        loaded = self.manifest.load()

    @mock.patch('yaml.safe_load', mock.MagicMock(return_value=gurum_manifest_stub.valid_manifest))
    @mock.patch('builtins.open', mock.MagicMock())
    @mock.patch('gurumcommon.gurum_manifest.GurumManifest._validate', mock.MagicMock())
    def test_load_project(self):
        loaded = self.manifest.load()
        self.assertEqual(loaded.project(), gurum_manifest_stub.valid_project)

    @mock.patch('yaml.safe_load', mock.MagicMock(return_value=gurum_manifest_stub.invalid_missing_project_manifest))
    @mock.patch('builtins.open', mock.MagicMock())
    @mock.patch('gurumcommon.gurum_manifest.GurumManifest._validate', mock.MagicMock())
    def test_it_throws_when_missing_the_project(self):
        loaded = self.manifest.load()

        with self.assertRaises(KeyError):
            loaded.project()

    @mock.patch('yaml.safe_load', mock.MagicMock(return_value=gurum_manifest_stub.valid_manifest))
    @mock.patch('builtins.open', mock.MagicMock())
    @mock.patch('gurumcommon.gurum_manifest.GurumManifest._validate', mock.MagicMock())
    def test_load_environments(self):
        loaded = self.manifest.load()
        self.assertEqual(loaded.environments(), gurum_manifest_stub.valid_environments)

    @mock.patch('yaml.safe_load', mock.MagicMock(return_value=gurum_manifest_stub.invalid_missing_environments_manifest))
    @mock.patch('builtins.open', mock.MagicMock())
    @mock.patch('gurumcommon.gurum_manifest.GurumManifest._validate', mock.MagicMock())
    def test_it_throws_when_missing_environments(self):
        loaded = self.manifest.load()

        with self.assertRaises(KeyError):
            loaded.environments()

    @mock.patch('yaml.safe_load', mock.MagicMock(return_value=gurum_manifest_stub.valid_manifest))
    @mock.patch('builtins.open', mock.MagicMock())
    @mock.patch('gurumcommon.gurum_manifest.GurumManifest._validate', mock.MagicMock())
    def test_it_loads_services(self):
        loaded = self.manifest.load()
        self.assertEqual(loaded.services(), gurum_manifest_stub.valid_services)

    @mock.patch('yaml.safe_load', mock.MagicMock(return_value=gurum_manifest_stub.valid_missing_services_manifest))
    @mock.patch('builtins.open', mock.MagicMock())
    @mock.patch('gurumcommon.gurum_manifest.GurumManifest._validate', mock.MagicMock())
    def test_it_works_with_no_services(self):
        expected_services = {}
        loaded = self.manifest.load()
        self.assertEqual(loaded.services(), expected_services)
