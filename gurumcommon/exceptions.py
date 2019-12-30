"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""


class BaseAWSLogsException(Exception):

    code = 1

    def hint(self):
        return "Unknown Error."


class InvalidGurumManifestError(BaseAWSLogsException):
    """Raised when invalid service manifest has been passed"""
    pass


class UnknownError(BaseAWSLogsException):

    code = 0

    def hint(self):
        return "Unknown Error."


class ServerError(BaseAWSLogsException):

    code = 500

    def hint(self):
        return "Server Error."


class UrlNotFoundError(BaseAWSLogsException):

    code = 404

    def hint(self):
        return "URL not found."


class AuthenticationError(BaseAWSLogsException):

    code = 401

    def hint(self):
        return "Authentication Failed. Please login first."


class BadRequestError(BaseAWSLogsException):

    code = 400

    def hint(self):
        return "Bad Request."

class UnexpectedRedirectError(BaseAWSLogsException):

    code = 300

    def hint(self):
        return "Unexpected Redirect."


class EmptyResponseError(BaseAWSLogsException):

    code = 200

    def hint(self):
        return "The response was empty."


class RepositoryNotFoundError(BaseAWSLogsException):

    def hint(self):
        return "No such repository found. Validate that you have configured your configuration file properly."


class InvalidPersonalAccessTokenError(BaseAWSLogsException):

    def hint(self):
        return "Personal Access Token invalid or not enough permissions. Ensure you have permissions to the repository."


class AlreadyExistsError(BaseAWSLogsException):

    def hint(self):
        return "The requested resource already exists."


class UnknownParameterError(BaseAWSLogsException):

    def hint(self):
        return "Unknown Parameter provided."
