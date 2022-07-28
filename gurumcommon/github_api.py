import requests

from gurumcommon.exceptions import InvalidPersonalAccessTokenError, RepositoryNotFoundError
from gurumcommon.logger import configure_logger

LOGGER = configure_logger(__name__)

def validate_pat(pat_token, owner, repo):
    url = 'https://api.github.com/repos/{}/{}'.format(owner, repo)
    headers = {'Authorization': 'token {}'.format(pat_token)}

    resp = requests.get(url, headers=headers)

    if resp.status_code == 401:
        raise InvalidPersonalAccessTokenError
    if resp.status_code == 404:
        raise RepositoryNotFoundError

def split_user_repo(user_repo_string):
    split = user_repo_string.split('/')

    return {'user': split[0], 'repo': split[1]}
