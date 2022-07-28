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
