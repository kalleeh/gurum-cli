"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import os
import logging
import click

from gurumcli.libs.config_manager import ConfigManager, ConfigValidationException
from gurumcommon.logger import configure_logger

LOGGER = configure_logger(__name__)

DEFAULT_CONFIG_CONTENTS = ' \
    [default] \
    user = '

class Context():
    """
    Top level context object for the CLI. Exposes common functionality required by a CLI, including logging,
    environment config parsing, debug logging etc.

    This object is passed by Click to every command that adds the proper annotation.
    Read this for more details on Click Context - http://click.pocoo.org/5/commands/#nested-handling-and-contexts
    Each command gets its own context object, but linked to both parent and child command's context, like a Linked List.

    This class itself does not rely on how Click works. It is just a plain old Python class that holds common
    properties used by every CLI command.
    """

    def __init__(self):
        """
        Initialize the context with default values
        """
        self._debug = False
        self._app_name = 'gurum'
        self._api_uri = None
        self._id_token = None
        self._cfg_path = None
        self.cfg_name = None
        self.profile = None
        self.config = None

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        """
        Turn on debug logging if necessary.

        :param value: Value of debug flag
        """
        self._debug = value

        if self._debug:
            # Turn on debug logging
            LOGGER.setLevel(logging.DEBUG)

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, value):
        """
        Set profile for credential resolution
        """
        self._profile = value

        if not self._profile:
            self._profile = 'default'

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        """
        Manage configuration file
        """
        self._config = value
        self._refresh_config()

    def _refresh_config(self):
        """
        Update the configuration properties read from configuration file based on values set in the context.
        """
        self._cfg_path = click.get_app_dir(self._app_name)

        if not os.path.exists(self._cfg_path):
            os.makedirs(self._cfg_path)
        self.cfg_name = os.path.join(self._cfg_path, '.' + self._app_name)
        if not os.path.exists(self.cfg_name):
            click.echo('No config file present. Run gurum login to configure.')
            with open(self.cfg_name, 'a') as f:
                f.write(DEFAULT_CONFIG_CONTENTS)

        try:
            self._config = ConfigManager(self.cfg_name)
        except ConfigValidationException as ex:
            click.echo('Invalid configuration: {}'.format(ex))
            raise SystemExit(0)
