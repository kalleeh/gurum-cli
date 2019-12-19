"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import keyring
import logging

LOGGER = logging.getLogger(__name__)

GURUM_GITHUB_NAMESPACE = "gurum.github"

def get_secret(key):
    try:
        secret = keyring.get_password(GURUM_GITHUB_NAMESPACE, key)

        return secret
    except keyring.errors.KeyringError as ex:
        LOGGER.debug(ex)
    except Exception as ex:
        LOGGER.debug(ex)
    
def set_secret(key, value):
    keyring.set_password(
        GURUM_GITHUB_NAMESPACE,
        key,
        value
    )