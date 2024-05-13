from typing import Dict, Any, Tuple
from json import dumps
from gendiff.formatters.plain import format_value


def make_json_diff(diff: Dict[str, Tuple[str, Any]]) -> Dict[str, Any]:
    formatter_dict = {}
    for key, (meta, value) in diff.items():
        if meta == 'nested':
            nested = make_json_diff(value)
            formatter_dict[key] = nested
        elif meta == 'updated':
            data1_value = value[0]
            data2_value = value[1]
            formatter_dict[key] = (f'{format_value(data1_value)}: '
                                   f'{meta} -> {format_value(data2_value)}')
        else:
            formatter_dict[key] = f'{format_value(value)}: {meta}'
    return formatter_dict


def get_json_diff(diff: Dict[str, Tuple[str, Any]]) -> str:
    formatter_dict: Dict[str, Any] = make_json_diff(diff)
    json_diff = dumps(formatter_dict, indent=4)
    return json_diff
