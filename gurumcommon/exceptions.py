"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""


class BaseGurumException(Exception):
    pass

class InvalidGurumManifestError(BaseGurumException):
    code = 400
    message = "Invalid Service Manifest."


class UnknownError(BaseGurumException):
    code = 0
    message = "Unknown Error."


class ServerError(BaseGurumException):
    code = 500
    message = "Server Error."


class UrlNotFoundError(BaseGurumException):
    code = 404
    message = "URL not found."


class AuthenticationError(BaseGurumException):
    code = 401
    message = "Authentication Failed. Please login first."


class BadRequestError(BaseGurumException):
    code = 400
    message = "Bad Request."

class UnexpectedRedirectError(BaseGurumException):
    code = 300
    message = "Unexpected Redirect."


class EmptyResponseError(BaseGurumException):
    code = 200
    message = "The response was empty."


class RepositoryNotFoundError(BaseGurumException):
    code = 404
    message = "No such repository found. Validate that you have configured your configuration file properly."


class InvalidPersonalAccessTokenError(BaseGurumException):
    code = 401
    message = "Personal Access Token invalid or not enough permissions. Ensure you have permissions to the repository."


class AlreadyExistsError(BaseGurumException):
    code = 409
    message = "The requested resource already exists."


class UnknownParameterError(BaseGurumException):
    code = 400
    message = "Unknown Parameter provided."
