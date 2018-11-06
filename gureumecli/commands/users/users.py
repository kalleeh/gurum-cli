"""
Command group for "local" suite for commands. It provides common CLI arguments, template parsing capabilities,
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