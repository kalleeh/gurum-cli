import click
from warrant import Cognito

from gurumcli.cli.main import pass_context


@click.command('change-password', short_help='Change password for current user')
@click.option('--password', prompt=True, hide_input=True)
@click.option('--new-password', prompt=True, hide_input=True, confirmation_prompt=True)
@pass_context
def cli(ctx, password, new_password):
    """Change password."""
    user = ctx.config.get(ctx.profile, 'user')
    click.echo('Changing password for {}...'.format(user), nl=True)

    id_token = ""
    refresh_token = ""
    access_token = ""
    id_token = ctx.config.get(ctx.profile, 'id_token')
    refresh_token = ctx.config.get(ctx.profile, 'refresh_token')
    access_token = ctx.config.get(ctx.profile, 'access_token')

    user_pool_id = ctx.config.get(ctx.profile, 'cognito_user_pool_id')
    app_client_id = ctx.config.get(ctx.profile, 'cognito_app_client_id')

    u = Cognito(
        user_pool_id,
        app_client_id,
        username=user,
        id_token=id_token,
        refresh_token=refresh_token,
        access_token=access_token)

    try:
        u.change_password(password, new_password)
        click.echo('Successfully updated password.')
    except Exception as ex:
        click.echo(ex)
