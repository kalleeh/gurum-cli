"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

"""
Command group for "users" suite for commands. It provides common CLI arguments, template parsing capabilities,
setting up stdin/stdout etc
"""

import click

from .change_password.cli import cli as change_password_cli
from .confirm_signup.cli import cli as confirm_signup_cli
from .forgot_password.cli import cli as forgot_password_cli


@click.group()
def cli():
    """
    Manage your users
    """
    pass  # pragma: no cover


# Add individual commands under this group
cli.add_command(change_password_cli)
cli.add_command(confirm_signup_cli)
cli.add_command(forgot_password_cli)