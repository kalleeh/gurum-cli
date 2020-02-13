"""
This is a sample, non-production-ready template.
© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.
This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

from configparser import ConfigParser

from gurumcommon.logger import configure_logger

LOGGER = configure_logger(__name__)

REQUIRED_VALUES = {
    'default': {
        'api_uri': None,
        'region': None,
        'cognito_user_pool_id': None,
        'cognito_identity_pool_id': None,
        'cognito_app_client_id': None
    }
}

class ConfigValidationException(Exception):
    pass


class ConfigManager(ConfigParser):
    def __init__(self, config_file):
        super(ConfigManager, self).__init__()

        self.read(config_file)
        self.validate_config()

    def validate_config(self):
        for section, keys in REQUIRED_VALUES.items():
            if section not in self:
                raise ConfigValidationException(
                    'Missing section %s' % section)

            for key, values in keys.items():
                if key not in self[section] or self[section][key] == '':
                    raise ConfigValidationException((
                        'Missing value for %s under section %s') % (key, section))

                if values:
                    if self[section][key] not in values:
                        raise ConfigValidationException((
                            'Invalid value for %s under section %s') % (key, section))
