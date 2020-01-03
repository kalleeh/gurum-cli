# Gurum CLI

This CLI provides the main developer interface for the Gurum Container Platform.
It provides capabilities for basic app management, creation of pipelines and user management.
Basic log viewing and filtering can exist for troubleshooting.

## What's Here

* README.md - this file
* Pipfile - requrements file for usage with Pipenv
* setup.py - module/package definition for Distutils
* gurumcli/ - this directory contains the Click CLI files and entrypoint referenced from setup.py
* tests/ - this directory contains unit tests for your application

## Installation

It is recommended to use pipenv to install and edit the CLI.
It automatically creates and manages a virtualenv for your projects, as well as adds/removes packages from your Pipfile as you install/uninstall packages. It also generates the ever–important Pipfile.lock, which is used to produce deterministic builds.
The CLI is also built using [Click](http://click.pocoo.org/6/) so you might want to check that out.

If you're on MacOS, you can install Pipenv easily with Homebrew:

```bash
brew install pipenv
```

Otherwise, just use pip:

```bash
pip3 install pipenv
```

When you have pipenv installed you can just run the following command in the folder to install dependencies and enter into editable mode. This is beneficial if you develop since changes to the code will be reflected directly in the CLI as you use it.

```bash
pipenv install -e .
```

Then enter the venv shell to start using the CLI.

```bash
pipenv shell
```

## Quickstart Guide

### First Run

If you haven't run the CLI before you will be prompted to configure the Cognito configuration to login to the platform. Ask your platform administrator for the correct settings, they should look similar to this;

```yaml
COGNITO_USER_POOL_ID = "eu-west-1_ZaPg126AbSAMPLE"
COGNITO_IDENTITY_POOL_ID = "b3df4e00-4548-4e69-8b60-85ec387feaw1SAMPLE"
COGNITO_APP_CLIENT_ID = "7o5p3h44bba6u9pfewaaf7ldf9kk"
REGION = "eu-west-1"
```

After you've entered the settings they should be saved in the configuration file for future use. If you ever need to switch the platform you need to manually edit the configuration file with the updated properties.

### Logging in

The CLI has two main functions to enable you to interact with the platform.
Start by logging in to the platform which configures your `.gurum` local configuration file placed in your OS' application support folder.
For MacOS this is `~/Library/Application Support/gurum/`.

```bash
$ gurum login
User: myuser@email.com
Password:
Logging in myuser@email.com..
Getting temporary STS credentials...
Logged in!
```

This generated temporary Cognito and STS credentials for you valid for 1 hour. After this you will need to log in again.

### Initialize your Gurum Manifest (gurum.yaml)

In the folder where you host your source code run the following command and follow the prompts to initialize a manifest file.

```bash
gurum init
```

### Deploy your app

Use the up command to deploy your app according to your manifest file.

```bash
gurum up
```

This will validate your manifest schema and provision the resources declared.

### Describe your app

To watch the deployment details and current status of your app, use the `describe` command.

```bash
$ gurum apps describe <app-name>
=== my-app
Description: Platform App on Shared Load Balancer
Status: UPDATE_COMPLETE
Endpoint: my-app.apps.gureu.me
Tags:
- gurum-groups: team1
- gurum-owner: myuser@email.com
- gurum-platform-version: 0.2
- gurum-region: eu-west-1
- gurum-platform-type: app
...
```

You can now visit the endpoint using your browser.
*Currently only HTTPS port 443 traffic is supported*

### Troubleshooting

To view the logs of your running containers you can use the logs command. By default it queries the last 5 minutes of logs but this can be customized using the `--start` option. You can also follow the logs using the `--watch` switch.

```bash
gurum apps logs my-app --start '30m' --watch
```

## Usage Guide

### Commands

gurum --help

* login
* signout
* up
* destroy
* apps
  * describe
  * logs
  * ls
* pipelines
  * describe
  * logs
  * ls
* services
  * describe
  * logs
  * ls
* users
  * change_password
  * confirm_signup
  * forgot_password

### Sample Deploy

```bash
gurum init
gurum up
git push
# Watch the logs for the stocks service and filter out health checks
gurum apps logs MyApp --watch | grep -v "/health"
