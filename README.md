# Gureume CLI

This CLI provides the main developer interface for the Gureume Container Platform.
It provides capabilities for basic app management, creation of pipelines and user management.
Basic log viewing and filtering can exist for troubleshooting.

## What's Here

* README.md - this file
* Pipfile - requrements file for usage with Pipenv
* setup.py - module/package definition for Distutils
* gureumecli/ - this directory contains the Click CLI files and entrypoint referenced from setup.py
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
Start by logging in to the platform which configures your `.gureume` local configuration file placed in your OS' application support folder.
For MacOS this is `~/Library/Application Support/gureume/`.

```bash
$ gureume login
User: myuser@email.com
Password:
Logging in myuser@email.com..
Getting temporary STS credentials...
Logged in!
```

This generated temporary Cognito and STS credentials for you valid for 1 hour. After this you will need to log in again.

### Creating an app

The CLI allows you to create an app using an existing container image that will be downloaded from the web.
*Currently this only supports unauthenticated Docker registries*

```bash
gureume apps create [--name <app-name>]
                    [--image <docker-image>] [--health-check-path <path>]
                    [--tasks <number-tasks>] [--env <key=value>]
```

All options are optional, however, if you don't specify a `name` it will be randomly generated herokuish-style.

### Describe your app

To watch the deployment details and current status of your app, use the `describe` command.

```bash
$ gureume apps describe <app-name>
=== karl
Description: Platform App on Shared Load Balancer
Status: UPDATE_COMPLETE
Endpoint: my-app.apps.gureu.me
Tags:
- gureume-groups: team1
- gureume-owner: myuser@email.com
- gureume-platform-version: 0.2
- gureume-region: eu-west-1
- gureume-platform-type: app
...
```

You can now visit the endpoint using your browser.
*Currently only HTTP port 80 traffic is supported*

### Troubleshooting

To view the logs of your running containers you can use the logs command. By default it queries the last 5 minutes of logs but this can be customized using the `--start` option. You can also follow the logs using the `--watch` switch.

```bash
gureume apps logs my-app --start '30m' --watch
```

## Usage Guide

### Commands

gureume

* login
* signout
* apps
  * create
  * describe
  * destroy
  * logs
  * ls
  * update
* pipelines
  * create
  * describe
  * destroy
  * ls
  * update
* services
  * create
  * describe
  * destroy
  * logs
  * ls
  * update
* users
  * change_password
  * confirm_signup
  * forgot_password

### Sample Deploy

```bash
gureume apps create --image alexwhen/docker-2048 --health-check-path '/'

gureume apps create
> portal
gureume pipelines create
> Name: portal-pipeline
> App name: portal
> Github repo: portal
> Github branch: master
> Github token: TOKEN
> Github user: kalleeh

gureume apps create
> stocks
gureume pipelines create
> Name: stocks-pipeline
> App name: stocks
> Github repo: stocks
> Github branch: master
> Github token: TOKEN
> Github user: kalleeh

# Watch the logs for the stocks service and filter out health checks
gureume apps logs stocks --watch | grep -v "/health"