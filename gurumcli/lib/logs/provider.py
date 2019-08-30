"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

"""
Discover & provide the log group name
"""


class LogGroupProvider(object):
    """
    Resolve the name of log group given the name of the resource
    """

    @staticmethod
    def for_lambda_function(function_name):
        """
        Returns the CloudWatch Log Group Name created by default for the AWS Lambda function with given name

        Parameters
        ----------
        function_name : str
            Name of the Lambda function

        Returns
        -------
        str
            Default Log Group name used by this function
        """
        return "/aws/lambda/{}".format(function_name)
