import click
import os
import requests
import boto3
import botocore

from gureume.cli import pass_context
from warrant import Cognito, exceptions


@click.command('login', short_help='Log out of the platform')
@click.option('--user', prompt=True, help='Username (email)')
@click.option('--password', prompt=True, hide_input=True)
@pass_context
def cli(ctx, user, password):
    """Authenticates to the platform to access your apps."""
    click.echo('Logging in {}...'.format(user), nl=True)
    credentials = {}

    u = Cognito(
        'eu-west-1_MkM8NwiuN',
        '1ts0lglioorltjrs0j3k3bniv5',
        username=user)
    
    # Patch for clients without a ~./aws/credentials file or unconfigured AWS credentials
    u.client = boto3.client(
        'cognito-idp',
        region_name='eu-west-1',
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
                IdentityPoolId='eu-west-1:b56abbdb-9b9b-4fa0-a7fd-538e3fff97e7',
                Logins={
                    'cognito-idp.eu-west-1.amazonaws.com/eu-west-1_MkM8NwiuN': credentials['id_token']
                }
            )

            user_identity_id = response['IdentityId']
        except Exception as ex:
            click.echo(ex)
        
        try:
            response = client.get_credentials_for_identity(
                IdentityId=user_identity_id,
                Logins={
                    'cognito-idp.eu-west-1.amazonaws.com/eu-west-1_MkM8NwiuN': credentials['id_token']
                }
            )

            credentials['aws_access_key_id'] = response['Credentials']['AccessKeyId']
            credentials['aws_secret_access_key'] = response['Credentials']['SecretKey']
            credentials['aws_session_token'] = response['Credentials']['SessionToken']
            credentials['aws_token_expiration'] = response['Credentials']['Expiration']
        except Exception as ex:
            click.echo(ex)

        # Configure the config file with API URI and temporary credentials
        if not ctx.config.has_section('default'):
            ctx.config.add_section('default')
        if not ctx.config.has_option('default', 'api_uri'):
            ctx.config.set('default', 'api_uri', 'https://api.gureu.me')
        ctx.config.set('default', 'user', user)
        ctx.config.set('default', 'id_token', credentials['id_token'])
        ctx.config.set('default', 'refresh_token', credentials['refresh_token'])
        ctx.config.set('default', 'access_token', credentials['access_token'])
        ctx.config.set('default', 'aws_access_key_id', credentials['aws_access_key_id'])
        ctx.config.set('default', 'aws_secret_access_key', credentials['aws_secret_access_key'])
        ctx.config.set('default', 'aws_session_token', credentials['aws_session_token'])
        ctx.config.set('default', 'aws_region', 'eu-west-1')
        cfgfile = open(ctx.cfg_name, 'w+')
        ctx.config.write(cfgfile)
        cfgfile.close()

        click.echo('Logged in!')