import click
from warrant import Cognito

from gurumcli.cli.main import pass_context


@click.command('reset-password', short_help='Initiate forgot password for a user')
@click.option('--user', prompt=True, help='Username (email)')
@click.option('--confirmation-code', prompt=True, help='Confirmation Code')
@pass_context
def cli(ctx, user, confirmation_code):
    """Confirm user signup."""
    click.echo('Initiating forgot password process for {}...'.format(user), nl=True)

    user_pool_id = ctx.config.get(ctx.profile, 'cognito_user_pool_id')
    app_client_id = ctx.config.get(ctx.profile, 'cognito_app_client_id')

    u = Cognito(
        user_pool_id,
        app_client_id,
        username=user)

    try:
        u.confirm_sign_up(confirmation_code, username=user)
        click.echo('Successfully confirmed signup.')
    except Exception as ex:
        click.echo(ex)
