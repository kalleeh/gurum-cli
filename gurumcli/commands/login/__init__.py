import logging
import os
import click
import requests
import boto3
import botocore

from warrant import Cognito, exceptions
from gurumcli.cli.main import pass_context, common_options
from gurumcommon.logger import configure_logger

LOGGER = configure_logger(__name__)

@click.command(context_settings=dict(help_option_names=[u'-h', u'--help']))
@click.option('--user', prompt=True, help='Username (email)')
@click.option('--password', prompt=True, hide_input=True)
@common_options
@pass_context
def cli(ctx, user, password):
    """ \b
        Login to the GURUM platform using your Cognito credentials.
        This will populate your temporary session tokens in your configuration file.
        Usually this is located with the application data directory.

    \b
    Common usage:

        \b
        Logs in to the platform.
        \b
        $ gurum login
    """
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx, user, password)  # pragma: no cover


def do_cli(ctx, user, password):
    region = ctx.config.get(ctx.profile, 'region')
    user_pool_id = ctx.config.get(ctx.profile, 'cognito_user_pool_id')
    identity_pool_id = ctx.config.get(ctx.profile, 'cognito_identity_pool_id')
    app_client_id = ctx.config.get(ctx.profile, 'cognito_app_client_id')

    click.echo('Logging in {}...'.format(user), nl=True)
    client = boto3.client('cognito-identity', region_name=region)
    credentials = {}

    u = Cognito(
        user_pool_id,
        app_client_id,
        username=user)

    # Patch for clients without a ~./aws/credentials file or unconfigured AWS credentials
    u.client = boto3.client(
        'cognito-idp',
        region_name=region,
        config=botocore.config.Config(
            signature_version=botocore.UNSIGNED
        )
    )

    try:
        u.authenticate(password)
    except exceptions.ForceChangePasswordException as ex:
        click.echo('Password change required.')
        new_password = click.prompt('Please enter your new password', hide_input=True)
        try:
            u.new_password_challenge(password, new_password)
        except Exception as ex:
            click.echo(ex)
        else:
            click.echo('Password has been set. Please login.')

            # Update config file with Cognito properies if it's not set
            cfgfile = open(ctx.cfg_name, 'w+')
            ctx.config.write(cfgfile)
            cfgfile.close()
    except Exception as ex:
        click.echo(ex)
    else:
        credentials['id_token'] = u.id_token
        credentials['refresh_token'] = u.refresh_token
        credentials['access_token'] = u.access_token

        user_identity_id = get_user_identity_id(client, region, identity_pool_id, user_pool_id, credentials['id_token'])
        credentials = get_sts_credentials(client, region, user_identity_id, user_pool_id, credentials)
        store_credentials_file(ctx, user, region, credentials)

        click.echo('Logged in!')

def get_sts_credentials(client, region, user_identity_id, user_pool_id, credentials):
    try:
        response = client.get_credentials_for_identity(
            IdentityId=user_identity_id,
            Logins={
                'cognito-idp.{}.amazonaws.com/{}'.format(region, user_pool_id): credentials['id_token']
            }
        )

        credentials['aws_access_key_id'] = response['Credentials']['AccessKeyId']
        credentials['aws_secret_access_key'] = response['Credentials']['SecretKey']
        credentials['aws_session_token'] = response['Credentials']['SessionToken']
        credentials['aws_token_expiration'] = response['Credentials']['Expiration']
    except Exception as ex:
        click.echo(ex)
    else:
        return credentials

def get_user_identity_id(client, region, identity_pool_id, user_pool_id, id_token):
    click.echo('Getting temporary STS credentials...')

    try:
        response = client.get_id(
            IdentityPoolId='{}:{}'.format(region, identity_pool_id),
            Logins={
                'cognito-idp.{}.amazonaws.com/{}'.format(region, user_pool_id): id_token
            }
        )
    except Exception as ex:
        LOGGER.debug(ex)

    return response['IdentityId']

def store_credentials_file(ctx, user, region, credentials):
    # Configure the config file with API URI and temporary credentials
    if not ctx.config.has_section(ctx.profile):
        ctx.config.add_section(ctx.profile)
    ctx.config.set(ctx.profile, 'user', user)
    ctx.config.set(ctx.profile, 'id_token', credentials['id_token'])
    ctx.id_token = credentials['id_token']
    ctx.config.set(ctx.profile, 'refresh_token', credentials['refresh_token'])
    ctx.config.set(ctx.profile, 'access_token', credentials['access_token'])
    ctx.config.set(ctx.profile, 'aws_access_key_id', credentials['aws_access_key_id'])
    ctx.config.set(ctx.profile, 'aws_secret_access_key', credentials['aws_secret_access_key'])
    ctx.config.set(ctx.profile, 'aws_session_token', credentials['aws_session_token'])
    ctx.config.set(ctx.profile, 'region', region)
    cfgfile = open(ctx.cfg_name, 'w+')
    ctx.config.write(cfgfile)
    cfgfile.close()
