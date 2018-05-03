import requests
import json

from prettytable import PrettyTable


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
        # Throw exception if request does not return 2xx
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 422:
            # Unprocessable Entity
            json_response = json.loads(response.text)
            if json_response['errors'][0]['code'] == 'error_code':
                print('Error!')

        # Unprocessable for some other reason or other HTTP error != 422
        print('HTTP Error: {}'.format(e))
        raise
    except requests.exceptions.RequestException as e:
        print('Connection error: {}'.format(e))
        raise
    
    return response


def json_to_table(events):
    table = PrettyTable()

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