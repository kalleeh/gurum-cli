
"""
This is a sample, non-production-ready template.
© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.
This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""


import json

from .exceptions import UnknownError, ServerError, UrlNotFoundError, AuthenticationError, AlreadyExistsException, BadRequestError, UnexpectedRedirectError
import requests


def request(method, url, headers, *payload):
    try:
        if method == 'get':
            response = requests.get(url, headers=headers)
        elif method == 'post':
            response = requests.post(url, json=payload, headers=headers)
        elif method == 'put':
            response = requests.put(url, json=payload, headers=headers)
        elif method == 'delete':
            response = requests.delete(url, headers=headers)
        elif method == 'patch':
            response = requests.patch(url, json=payload, headers=headers)

        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if response.status_code >= 500:
            raise ServerError(response.text)
        if response.status_code == 404:
            raise UrlNotFoundError(response.text)
        if response.status_code == 401:
            raise AuthenticationError(response.text)
        if response.status_code == 400:
            raise BadRequestError(response.text)
        if response.status_code >= 300:
            raise UnexpectedRedirectError(response.text)
    except requests.exceptions.ConnectionError:
        raise UnknownError(response.text)
    except requests.exceptions.Timeout:
        raise UnknownError(response.text)
    except requests.exceptions.RequestException:
        raise UnknownError(response.text)
    else:
        response = json.loads(response.text)

        return response
