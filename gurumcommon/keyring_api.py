import keyring

from gurumcommon.logger import configure_logger

LOGGER = configure_logger(__name__)

GURUM_GITHUB_NAMESPACE = "gurum.github"

def get_github_secret(key):
    return _get_secret(GURUM_GITHUB_NAMESPACE, key)

def set_github_secret(key, value):
    _set_secret(GURUM_GITHUB_NAMESPACE, key, value)

def _get_secret(namespace, key):
    try:
        return keyring.get_password(namespace, key)
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
