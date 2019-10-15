"""
This is a sample, non-production-ready template.

© 2019 Amazon Web Services, In​c. or its affiliates. All Rights Reserved.

This AWS Content is provided subject to the terms of the
AWS Customer Agreement available at http://aws.amazon.com/agreement
or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""


from exceptions import EmptyResponseError

from prettytable import PrettyTable
from haikunator import Haikunator


def haikunate():
    haikunator = Haikunator()
    return haikunator.haikunate()


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

    if not events:
        raise EmptyResponseError

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
    response = {}
    str_list = []

    str_list.append("=== " + data['name'], fg='blue')
    str_list.append("Description: " + data['description'])

    # print status yellow if in progress, completed is green
    if data['status'].endswith('_IN_PROGRESS'):
        str_list.append("Status: " + data['status'], fg='yellow')
    elif data['status'].endswith('_COMPLETE'):
        str_list.append("Status: " + data['status'], fg='green')
    else:
        str_list.append("Status: " + data['status'], fg='red')

    if 'endpoint' in data:
        str_list.append("Endpoint: " + data['endpoint'], fg='green')
    if 'repository' in data:
        str_list.append("Repository: " + data['repository'], fg='green')

    if 'params' in data:
        response['params'] = iterate_key_value_pairs(data['params'])
    if 'outputs' in data:
        response['outputs'] = iterate_key_value_pairs(data['outputs'])
    if 'tags' in data:
        response['tags'] = iterate_key_value_pairs(data['tags'])

    response['message'] = ''.join(str_list)

    return response


def iterate_key_value_pairs(kv_dict):
    response = {}

    for key, val in kv_dict.items():
        return "- {}: {}".format(key, val)

    return response
