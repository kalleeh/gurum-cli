"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

"""
Command group for "services" suite for commands. It provides common CLI arguments, template parsing capabilities,
setting up stdin/stdout etc
"""

import click

from .create.cli import cli as create_cli
from .describe.cli import cli as describe_cli
from .destroy.cli import cli as destroy_cli
from .logs.cli import cli as logs_cli
from .ls.cli import cli as ls_cli
from .update.cli import cli as update_cli


@click.group()
def cli():
    """
    Manage your services
    """
    pass  # pragma: no cover


# Add individual commands under this group
cli.add_command(create_cli)
cli.add_command(describe_cli)
cli.add_command(destroy_cli)
cli.add_command(logs_cli)
cli.add_command(ls_cli)
cli.add_command(update_cli)