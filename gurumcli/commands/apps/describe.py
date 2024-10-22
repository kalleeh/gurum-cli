import time
import click
import click_spinner

from gurumcli.cli.main import pass_context, common_options
from gurumcli.libs.formatter import json_to_table, prettyprint
from gurumcommon.clients.api_client import ApiClient


@click.command('describe', short_help='Displays details about app')
@click.argument('name')
@click.option('--watch', is_flag=True, help='Automatically update the stauts every 5s')
@pass_context
@common_options
def cli(ctx, name, watch):
    """ \b
        Display detailed information about the application

    \b
    Common usage:

        \b
        Display detailed information about an application.
        \b
        $ gurum apps describe myApp
    """
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx, name, watch)  # pragma: no cover


def do_cli(ctx, name, watch):
    """Display detailed information about the application."""
    apps = {}
    payload = {}
    payload['name'] = name

    api_client = ApiClient(
        api_uri=ctx.config.get(ctx.profile, 'api_uri'),
        id_token=ctx.config.get(ctx.profile, 'id_token')
    )

    # Start a loop that checks for stack creation status
    with click_spinner.spinner():
        while True:

            resp = api_client.apps.describe(name)
            apps = resp['apps'][0]

            resp = api_client.events.list(name)
            events = resp['events']

            if watch:
                click.clear()

            prettyprint(apps)
            click.echo(json_to_table(events))

            if not watch:
                break

            click.echo('Working on: {}'.format(name))
            click.echo('This usually takes a couple of minutes...')
            click.echo('This call is asynchrounous so feel free to Ctrl+C ' \
                        'anytime and it will continue running in background.')

            # Stop loop if task is complete
            if apps['status'].endswith('_COMPLETE') and not watch:
                break

            # refresh every 5 seconds
            time.sleep(5)
