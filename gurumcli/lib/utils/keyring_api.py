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

def get_github_secret(key):
    return _get_secret(GURUM_GITHUB_NAMESPACE, key)

def set_github_secret(key, value):
    _set_secret(GURUM_GITHUB_NAMESPACE, key, value)

def _get_secret(namespace, key):
    try:
        return secret = keyring.get_password(namespace, key)
    except keyring.errors.KeyringError as ex:
        LOGGER.debug(ex)
    except Exception as ex:
        LOGGER.debug(ex)
    
def _set_secret(namespace, key, value):
    keyring.set_password(
        namespace,
        key,
        value
    )