
"""
This is a sample, non-production-ready template.
© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.
This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import json
import requests

from gurumcommon.exceptions import UnknownError, ServerError, UrlNotFoundError, AuthenticationError, AlreadyExistsError, BadRequestError, UnexpectedRedirectError


def request(method, url, headers, *payload):
    router = {
        'get': get(url, headers),
        'post': post(url, payload, headers),
        'put': put(url, payload, headers),
        'delete': delete(url, headers),
        'patch': patch(url, payload, headers)
    }

    try:
        response = router[method]

        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if response.status_code >= 500:
            raise ServerError(response.text)
        if response.status_code == 409:
            raise AlreadyExistsError(response.text)
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

def get(url, headers):
    return requests.get(url, headers=headers)

def post(url, payload, headers):
    return requests.post(url, json=payload, headers=headers)

def put(url, payload, headers):
    return requests.put(url, json=payload, headers=headers)

def delete(url, headers):
    return requests.delete(url, headers=headers)

def patch(url, payload, headers):
    return requests.patch(url, json=payload, headers=headers)
