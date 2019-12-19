# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

"""
Module used for working with the Service Manifest file.
"""

import os

from .exceptions import InvalidGurumManifestError

import yaml
import yamale

from .logger import configure_logger
LOGGER = configure_logger(__name__)

GURUM_SCHEMA_FILE = "gurum_manifest_schema.yaml"
GURUM_FILE = "gurum.yaml"

class GurumManifest:
    def __init__(
            self,
            manifest_schema_path,
            manifest_path=None
    ):
        self.manifest_path = manifest_path or GURUM_FILE
        self.manifest_dir_path = manifest_path or 'gurum_manifest'
        self.manifest_schema_path = manifest_schema_path or GURUM_SCHEMA_FILE
        self.manifest_contents = self._contents()
        self._validate()

    def _read(self, file_path=None):
        if file_path is None:
            file_path = self.manifest_path
        try:
            LOGGER.info('Loading service_manifest file %s', file_path)
            with open(file_path, 'r') as stream:
                return yaml.load(stream, Loader=yaml.FullLoader)
        except FileNotFoundError:
            LOGGER.info('No manifest file found at %s, continuing', file_path)
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
                "Deployment Map specification is invalid (ValueError)"
            )
        except KeyError:
            raise InvalidGurumManifestError(
                "Deployment Map specification is invalid (KeyError)"
            )
        except FileNotFoundError:
            raise InvalidGurumManifestError(
                "No Service Map files found, create a gurum.yaml file."
            )

    def _contents(self):
        manifest_contents = {}

        try:
            manifest_contents = self._read(GURUM_FILE)
        except Exception as ex:
            print(ex) #TODO raise UnableToReadManifestException()

        return manifest_contents

    def project(self):
        return self.manifest_contents['project']
        
    def environments(self):
        return self.manifest_contents['environments']

    def services(self):
        return self.manifest_contents['services']
