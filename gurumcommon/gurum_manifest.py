# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

"""
Module used for working with the Service Manifest file.
"""

import os
import yaml
import yamale

from gurumcommon.exceptions import InvalidGurumManifestError, GurumManifestNotFoundError
from gurumcommon.logger import configure_logger

LOGGER = configure_logger(__name__)

GURUM_FILE = "gurum.yaml"
GURUM_SCHEMA_FILE = "gurum_manifest_schema.yaml"

class GurumManifest:
    def __init__(
            self
    ):
        base_dir = os.path.abspath(__file__ + "../../../gurumcommon")
        self.manifest_path = os.path.join(os.getcwd(), GURUM_FILE)
        self.manifest_schema_path = os.path.join(base_dir, GURUM_SCHEMA_FILE)

    def load(self):
        self.manifest_contents = self._contents()
        self._validate()
        return self

    def _read(self):
        try:
            LOGGER.info('Loading service_manifest file %s', self.manifest_path)
            with open(self.manifest_path, 'r') as stream:
                return yaml.safe_load(stream)
        except FileNotFoundError:
            LOGGER.info('No manifest file found at %s, continuing', self.manifest_path)
            return {}

    def _validate(self):
        """
        Validates the deployment map contains valid configuration
        """
        try:
            schema = yamale.make_schema(self.manifest_schema_path)
            data = yamale.make_data(self.manifest_path)

            yamale.validate(schema, data)
        except ValueError:
            raise InvalidGurumManifestError(
                "Gurum Manifest is invalid (ValueError)"
            )
        except KeyError:
            raise InvalidGurumManifestError(
                "Gurum Manifest is invalid (KeyError)"
            )
        except FileNotFoundError:
            raise GurumManifestNotFoundError(
                "No Gurum Manifest found, create a gurum.yaml file."
            )

    def _contents(self):
        manifest_contents = {}

        try:
            manifest_contents = self._read()
        except Exception as ex:
            raise InvalidGurumManifestError(
                "Unable to read manifest file: {}".format(ex)
            )

        return manifest_contents

    def project(self):
        return self.manifest_contents['project']

    def environments(self):
        return self.manifest_contents['environments']

    def services(self):
        if 'services' in self.manifest_contents:
            return self.manifest_contents['services']
        return {}
