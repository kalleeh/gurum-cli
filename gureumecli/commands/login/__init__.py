# -*- coding: utf-8 -*-
"""
Login to the platform
"""
import logging
import click
import os
import requests
import boto3
import botocore

from warrant import Cognito, exceptions
from gureumecli.cli.main import pass_context, common_options
from gureumecli.commands.exceptions import UserException

LOG = logging.getLogger(__name__)

# export COGNITO_USER_POOL_ID="eu-west-1_Mkfe1asNSAMPLE"
# export COGNITO_IDENTITY_POOL_ID="b5bbdabdb-9b9b-4fa0-a7fd-533222aeSAMPLE"
# export COGNITO_APP_CLIENT_ID="1ts042gliofewaadsas0j3k3bbrwSAMPLE"

@click.command(context_settings=dict(help_option_names=[u'-h', u'--help']))
@click.option('--user', prompt=True, help='Username (email)')
@click.option('--password', prompt=True, hide_input=True)
@common_options
@pass_context
def cli(ctx, user, password):
    """ \b
        Login to the GUREUME platform using your Cognito credentials.
        This will populate your temporary session tokens in your configuration file.
        Usually this is located with the application data directory.

    \b
    Common usage:

        \b
        Logs in to the platform.
        \b
        $ gureume login
    """
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx, user, password)  # pragma: no cover


def do_cli(ctx, user, password):
    if not ctx._config.has_option('default', 'cognito_user_pool_id'):
        user_pool_id = click.prompt('No user pool configured. Enter Cognito User Pool ID:')
        ctx._config.set('default', 'cognito_user_pool_id', user_pool_id)
    else:
        user_pool_id = ctx._config.get('default', 'cognito_user_pool_id')
    
    if not ctx._config.has_option('default', 'cognito_identity_pool_id'):
        identity_pool_id = click.prompt('No identity pool configured. Enter Cognito Identity Pool ID:')
        ctx._config.set('default', 'cognito_identity_pool_id', identity_pool_id)
    else:
        identity_pool_id = ctx._config.get('default', 'cognito_identity_pool_id')
    
    if not ctx._config.has_option('default', 'cognito_app_client_id'):
        app_client_id = click.prompt('No user pool configured. Enter Cognito App Client ID:')
        ctx._config.set('default', 'cognito_app_client_id', app_client_id)
    else:
        app_client_id = ctx._config.get('default', 'cognito_app_client_id')
    
    if not ctx._config.has_option('default', 'region'):
        region = click.prompt('No region configured. Enter region (eu-west-1):')
        ctx._config.set('default', 'region', region)
    else:
        region = ctx._config.get('default', 'region')

    """Authenticates to the platform to access your apps."""
    click.echo('Logging in {}...'.format(user), nl=True)
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
            click.echo('Password has been set. Please login again.')
    except Exception as ex:
        click.echo(ex)
    else:
        credentials['id_token'] = u.id_token
        credentials['refresh_token'] = u.refresh_token
        credentials['access_token'] = u.access_token

        click.echo('Getting temporary STS credentials...')
        client = boto3.client('cognito-identity')
        user_identity_id = ""

        try:
            response = client.get_id(
                IdentityPoolId='{}:{}'.format(region, identity_pool_id),
                Logins={
                    'cognito-idp.{}.amazonaws.com/{}'.format(region, user_pool_id): credentials['id_token']
                }
            )

            user_identity_id = response['IdentityId']
        except Exception as ex:
            click.echo(ex)
        
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

        # Configure the config file with API URI and temporary credentials
        if not ctx._config.has_section('default'):
            ctx._config.add_section('default')
        if not ctx._config.has_option('default', 'api_uri'):
            ctx._config.set('default', 'api_uri', 'https://api.gureu.me')
        ctx._api_uri = 'https://api.gureu.me'
        ctx._config.set('default', 'user', user)
        ctx._config.set('default', 'id_token', credentials['id_token'])
        ctx._id_token = credentials['id_token']
        ctx._config.set('default', 'refresh_token', credentials['refresh_token'])
        ctx._config.set('default', 'access_token', credentials['access_token'])
        ctx._config.set('default', 'aws_access_key_id', credentials['aws_access_key_id'])
        ctx._config.set('default', 'aws_secret_access_key', credentials['aws_secret_access_key'])
        ctx._config.set('default', 'aws_session_token', credentials['aws_session_token'])
        ctx._config.set('default', 'aws_region', 'eu-west-1')
        cfgfile = open(ctx._cfg_name, 'w+')
        ctx._config.write(cfgfile)
        cfgfile.close()

        click.echo('Logged in!')