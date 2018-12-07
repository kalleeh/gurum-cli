"""
Context information passed to each CLI command
"""

import logging
import boto3
import os
import configparser
import click


class Context(object):
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
        self._app_name = 'gureume'
        self._aws_region = None
        self._aws_profile = None
        self._config = None
        self._cfg_name = None
        self._cfg_path = None
        self._id_token = None
        self._api_uri = None

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
            logging.getLogger().setLevel(logging.DEBUG)

    @property
    def region(self):
        return self._aws_region

    @region.setter
    def region(self, value):
        """
        Set AWS region
        """
        self._aws_region = value
        self._refresh_session()

    @property
    def profile(self):
        return self._aws_profile

    @profile.setter
    def profile(self, value):
        """
        Set AWS profile for credential resolution
        """
        self._aws_profile = value
        self._refresh_session()

    def _refresh_session(self):
        """
        Update boto3's default session by creating a new session based on values set in the context. Some properties of
        the Boto3's session object are read-only. Therefore when Click parses new AWS session related properties (like
        region & profile), it will call this method to create a new session with latest values for these properties.
        """
        boto3.setup_default_session(region_name=self._aws_region,
                                    profile_name=self._aws_profile)

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
        self._cfg_name = os.path.join(self._cfg_path, '.' + self._app_name)
        if not os.path.exists(self._cfg_name):
            with open(self._cfg_name, 'a') as f:
                f.write(' \
                    [default] \
                    user = \
                ')
        
        self._config = configparser.ConfigParser()
        self._config.read(self._cfg_name)