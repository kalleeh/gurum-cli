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

user_pool_id = os.environ['COGNITO_USER_POOL_ID']
identity_pool_id = os.environ['COGNITO_IDENTITY_POOL_ID']
app_client_id = os.environ['COGNITO_APP_CLIENT_ID']
region = os.environ['REGION']

@click.command(context_settings=dict(help_option_names=[u'-h', u'--help']))
@click.option('--user', prompt=True, help='Username (email)')
@click.option('--password', prompt=True, hide_input=True)
@common_options
@pass_context
def cli(ctx, user, password):
    """ \b
        Initialize a serverless application with a GUREUME template, folder
        structure for your Lambda functions, connected to an event source such as APIs,
        S3 Buckets or DynamoDB Tables. This application includes everything you need to
        get started with serverless and eventually grow into a production scale application.
        \b
        This command can initialize a boilerplate serverless app. If you want to create your own
        template as well as use a custom location please take a look at our official documentation.

    \b
    Common usage:

        \b
        Initializes a new GUREUME project using Python 3.6 default template runtime
        \b
        $ sam init --runtime python3.6
        \b
        Initializes a new GUREUME project using custom template in a Git/Mercurial repository
        \b
        # gh being expanded to github url
        $ sam init --location gh:aws-samples/cookiecutter-aws-sam-python
        \b
        $ sam init --location git+ssh://git@github.com/aws-samples/cookiecutter-aws-sam-python.git
        \b
        $ sam init --location hg+ssh://hg@bitbucket.org/repo/template-name

        \b
        Initializes a new GUREUME project using custom template in a Zipfile
        \b
        $ sam init --location /path/to/template.zip
        \b
        $ sam init --location https://example.com/path/to/template.zip

        \b
        Initializes a new GUREUME project using custom template in a local path
        \b
        $ sam init --location /path/to/template/folder

    """
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx, user, password)  # pragma: no cover


def do_cli(ctx, user, password):
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