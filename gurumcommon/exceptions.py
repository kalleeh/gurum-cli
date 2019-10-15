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


class UnknownDateError(BaseAWSLogsException):

    code = 3

    def hint(self):
        return "awslogs doesn't understand '{0}' as a date.".format(self.args[0])


class TooManyStreamsFilteredError(BaseAWSLogsException):

    code = 6

    def hint(self):
        return ("The number of streams that match your pattern '{0}' is '{1}'. "
                "AWS API limits the number of streams you can filter by to {2}."
                "It might be helpful to you to not filter streams by any "
                "pattern and filter the output of awslogs.").format(*self.args)


class NoStreamsFilteredError(BaseAWSLogsException):

    code = 7

    def hint(self):
        return ("No streams match your pattern '{0}' for the given time period.").format(*self.args)


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