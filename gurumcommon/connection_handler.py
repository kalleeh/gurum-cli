
"""
This is a sample, non-production-ready template.
© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.
This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""


import json

from .exceptions import UnknownError, ServerError, UrlNotFoundError, AuthenticationError, BadRequestError, UnexpectedRedirectError
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
        raise
    except requests.exceptions.Timeout:
        raise
    except requests.exceptions.RequestException:
        raise
    else:
        response = json.loads(response.text)

        if 'statusCode' not in response:
            raise UnknownError(response)

        if response['statusCode'] == 200:
            return json.loads(response['body'])
        else:
            raise UnknownError(response)