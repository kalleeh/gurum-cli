import click

from .describe import cli as describe_cli
from .logs import cli as logs_cli
from .ls import cli as ls_cli
from .put_approval import cli as put_approval_cli
from .status import cli as status_cli


@click.group()
def cli():
    """
    Manage your pipelines
    """
    pass  # pragma: no cover


# Add individual commands under this group
cli.add_command(describe_cli)
cli.add_command(logs_cli)
cli.add_command(ls_cli)
cli.add_command(put_approval_cli)
cli.add_command(status_cli)
