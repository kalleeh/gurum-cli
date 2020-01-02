"""
This is a sample, non-production-ready template.
© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.
This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import click

from prettytable import PrettyTable


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
            value = format_message(str(value), 80)
            row.append(value)

        table.add_row(row)

    return table


def prettyprint(data):
    click.secho("=== " + data['name'], fg='blue')
    click.secho("Description: " + data['description'])

    # print status yellow if in progress, completed is green
    if data['status'].endswith('_IN_PROGRESS'):
        click.secho("Status: " + data['status'], fg='yellow')
    elif data['status'].endswith('_COMPLETE'):
        click.secho("Status: " + data['status'], fg='green')
    else:
        click.secho("Status: " + data['status'], fg='red')

    if 'endpoint' in data:
        click.secho("Endpoint: " + data['endpoint'], fg='green')
    if 'repository' in data:
        click.secho("Repository: " + data['repository'], fg='green')

    # iterate over and print outputs
    if 'params' in data and len(data['params']) > 0:
        click.secho("Parameters: ")
        for key, val in data['params'].items():
            click.secho("- {}: {}".format(key, val))

    # iterate over and print outputs
    if 'outputs' in data and len(data['outputs']) > 0:
        click.secho("Outputs: ")
        for key, val in data['outputs'].items():
            click.secho("- {}: {}".format(key, val))

    # iterate over and print tags
    if 'tags' in data and len(data['tags']) > 0:
        click.secho("Tags: ")
        for key, val in data['tags'].items():
            click.secho("- {}: {}".format(key, val))
