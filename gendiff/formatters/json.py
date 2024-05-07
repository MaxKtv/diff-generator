from typing import Dict, Any, Tuple
from json import dumps
from gendiff.formatters.plain import format_value


def make_json_diff(diff: Dict[str, Tuple[str, Any]],
                   formatter_dict: Dict[str, Any], _) -> Dict[str, Any]:

    for key, (meta, value) in diff.items():
        if meta == 'original':
            formatter_dict[key] = f'{format_value(value)}: {meta}'
        else:
            if meta == 'added':
                formatter_dict[key] = f'{format_value(value[1])}: {meta}'
            elif meta == 'removed':
                formatter_dict[key] = f'{format_value(value[0])}: {meta}'
            elif meta == 'updated':
                formatter_dict[key] = (f'{format_value(value[0])}: '
                                       f'{meta} -> {format_value(value[1])}')

    return formatter_dict


def get_json_diff(formatter_dict: Dict[str, Any]) -> str:
    return dumps(formatter_dict, indent=4)
