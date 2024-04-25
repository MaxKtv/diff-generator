from typing import Dict, Any
from json import dumps
from gendiff.formatters.stylish import decoder


def make_json_diff(diff: Dict[str, Any], key: str,
                   data1: Dict[str, Any], data2: Dict[str, Any],
                   json_diff) -> Dict[str, Any]:
    diff_value = diff[key]
    if diff_value == 'original':
        json_diff[key] = f'{decoder(data1[key])}: {diff_value}'
    elif diff_value == 'changed':
        if key not in data1:
            diff_value = 'added'
            json_diff[key] = f'{decoder(data2[key])}: {diff_value}'
        elif key not in data2:
            diff_value = 'removed'
            json_diff[key] = f'{decoder(data1[key])}: {diff_value}'
        else:
            diff_value = 'updated'
            json_diff[key] = (f'{decoder(data1[key])}: '
                              f'{diff_value} -> {decoder(data2[key])}')
    return json_diff


def get_json_diff(formatted_diff: Dict[str, Any]) -> str:
    return dumps(formatted_diff, indent=4)
