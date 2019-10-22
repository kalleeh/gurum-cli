"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import requests

def validate_pat(pat_token, owner, repo):
    url = 'https://api.github.com/repos/{}/{}'.format(owner, repo)
    headers = {'Authorization': 'token {}'.format(pat_token)}
 
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return True
    else:
        return False

def split_user_repo(user_repo_string):
    split = user_repo_string.split('/')

    return {'user': split[0], 'repo': split[1]}
