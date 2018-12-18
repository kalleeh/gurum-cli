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
            row.append(value)

        table.add_row(row)
    
    return table