from typing import Dict, Any
from json import dumps
from gendiff.formatters.plain import format_value


def make_json_diff(diff: Dict[str, Any], variable: Dict[str, Any],
                   _) -> Dict[str, Any]:
    for key, (meta, value) in diff.items():
        if meta == 'original':
            variable[key] = f'{format_value(value)}: {meta}'
        else:
            if meta == 'added':
                variable[key] = f'{format_value(value[1])}: {meta}'
            elif meta == 'removed':
                variable[key] = f'{format_value(value[0])}: {meta}'
            elif meta == 'updated':
                variable[key] = (f'{format_value(value[0])}: '
                                 f'{meta} -> {format_value(value[1])}')
    return variable


def get_json_diff(formatted_diff: Dict[str, Any]) -> str:
    return dumps(formatted_diff, indent=4)
