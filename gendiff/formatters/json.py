from typing import Dict, Any
from json import dumps
from gendiff.formatters.stylish import decoder


def make_json_diff(diff: Dict[str, Any],
                   data1: Dict[str, Any], data2: Dict[str, Any],
                   json_diff) -> Dict[str, Any]:
    for key, value in diff.items():
        if value == 'original':
            json_diff[key] = f'{decoder(data1[key])}: {value}'
        elif value == 'changed':
            if key not in data1:
                value = 'added'
                json_diff[key] = f'{decoder(data2[key])}: {value}'
            elif key not in data2:
                value = 'removed'
                json_diff[key] = f'{decoder(data1[key])}: {value}'
            else:
                value = 'updated'
                json_diff[key] = (f'{decoder(data1[key])}: '
                                  f'{value} -> {decoder(data2[key])}')
    return json_diff


def get_json_diff(formatted_diff: Dict[str, Any]) -> str:
    return dumps(formatted_diff, indent=4)
