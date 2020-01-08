"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import click

from .describe import cli as describe_cli
from .logs import cli as logs_cli
from .ls import cli as ls_cli


@click.group()
def cli():
    """
    Manage your services
    """
    pass  # pragma: no cover


# Add individual commands under this group
cli.add_command(describe_cli)
cli.add_command(logs_cli)
cli.add_command(ls_cli)
