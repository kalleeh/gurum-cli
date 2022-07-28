import click
from warrant import Cognito

from gurumcli.cli.main import pass_context


@click.command('forgot-password', short_help='Initiate forgot password for a user')
@click.option('--user', prompt=True, help='Username (email)')
@pass_context
def cli(ctx, user):
    """Initiates a forgot password."""
    click.echo('Initiating forgot password process for {}...'.format(user), nl=True)

    user_pool_id = ctx.config.get(ctx.profile, 'cognito_user_pool_id')
    app_client_id = ctx.config.get(ctx.profile, 'cognito_app_client_id')

    u = Cognito(
        user_pool_id,
        app_client_id,
        username=user)

    try:
        u.initiate_forgot_password()
        click.echo('Successful. Check your inbox for confirmation code.')
    except Exception as ex:
        click.echo(ex)

    confirmation_code = click.prompt('Confirmation Code')
    new_password = click.prompt('New Password', hide_input=True)

    try:
        u.confirm_forgot_password(confirmation_code, new_password)
        click.echo('Successfully set new password. Please login.')
    except Exception as ex:
        click.echo(ex)
