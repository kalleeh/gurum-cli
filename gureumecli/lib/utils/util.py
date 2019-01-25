import requests
import json
import sys
import click

from prettytable import PrettyTable
from haikunator import Haikunator


def haikunate():
    haikunator = Haikunator()
    return haikunator.haikunate()

def request(method, url, headers, *payload):
    try:
        if method == 'get':
            response = requests.get(url, headers=headers)
        elif method == 'post':
            response = requests.post(url, json=payload, headers=headers)
        elif method == 'delete':
            response = requests.delete(url, headers=headers)
        elif method == 'patch':
            response = requests.patch(url, json=payload, headers=headers)

        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code >= 500:
            click.echo('[{0}] Server Error'.format(response.status_code))
            click.echo('Message: {0}'.format(response.text))
            sys.exit(1)
        elif response.status_code == 404:
            click.echo('[{0}] URL not found: [{1}]'.format(response.status_code, url))
            click.echo('Message: {0}'.format(response.text))
            sys.exit(1)
        elif response.status_code == 401:
            click.echo('[{0}] Authentication Failed. Please login first.'.format(response.status_code))
            click.echo('Message: {0}'.format(response.text))
            sys.exit(1)
        elif response.status_code == 400:
            click.echo('[{0}] Bad Request'.format(response.status_code))
            click.echo('Message: {0}'.format(response.text))
            sys.exit(1)
        elif response.status_code >= 300:
            click.echo('[{0}] Unexpected Redirect'.format(response.status_code))
            click.echo('Message: {0}'.format(response.text))
            sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        click.echo ("Error Connecting:", e)
        click.echo('Message: {0}'.format(response.text))
        sys.exit(1)
    except requests.exceptions.Timeout as e:
        click.echo ("Timeout Error:", e)
        click.echo('Message: {0}'.format(response.text))
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        click.echo('Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
        sys.exit(1)
    else:
        response = json.loads(response.text)
        
        if response['statusCode'] == '200':
            return response
        else:
            click.echo('[{0}] Server Error'.format(response['statusCode']))
            click.echo('{0}'.format(response['body']))
            sys.exit(1)


def format_message(message, max_line_length):
    line_length = 0
    words = message.split(" ")
    formatted_message = ""
    for word in words:
        if line_length + (len(word) + 1) <= max_line_length:
            formatted_message = formatted_message + word + " "
            line_length = line_length + len(word) + 1
        else:
            #append a line break, then the word and a space
            formatted_message = formatted_message + "\n" + word + " "
            line_length = len(word) + 1
    
    return formatted_message


def json_to_table(events):
    table = PrettyTable()

    if len(events) < 1:
        return 'Theres nothing here :('
    
    for index, event in enumerate(events):
        if index == 0:
            columns = []
            for key in event.keys():
                columns.append(key)
            table.field_names = columns
        row = []
        for value in event.values():
            value = format_message(value, 80)
            row.append(value)

        table.add_row(row)
    
    return table


def prettyprint(data):
    click.secho("=== " + data['name'], fg='blue')
    click.secho("Description: " + data['description'])

    # print status yellow if in progress, completed is green
    if(data['status'].endswith('_IN_PROGRESS')):
        click.secho("Status: " + data['status'], fg='yellow')
    elif(data['status'].endswith('_COMPLETE')):
        click.secho("Status: " + data['status'], fg='green')
    else:
        click.secho("Status: " + data['status'], fg='red')

    if 'endpoint' in data:
        click.secho("Endpoint: " + data['endpoint'], fg='green')
    if 'repository' in data:
        click.secho("Repository: " + data['repository'], fg='green')

    # iterate over and print outputs
    if 'params' in data:
        click.secho("Parameters: ")
        for key, val in data['params'].items():
            click.secho("- {}: {}".format(key, val))
    
    # iterate over and print outputs
    if 'outputs' in data:
        click.secho("Outputs: ")
        for key, val in data['outputs'].items():
            click.secho("- {}: {}".format(key, val))
    
    # iterate over and print tags
    if 'tags' in data:
        click.secho("Tags: ")
        for key, val in data['tags'].items():
            click.secho("- {}: {}".format(key, val))