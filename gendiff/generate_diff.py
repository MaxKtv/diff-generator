from gendiff.parser import get_data
from gendiff.formatters import stylish, plain, json
from pathlib import Path
from typing import Dict, Any


FORMATTERS = {
    'stylish': stylish.make_stylish_diff,
    'plain': plain.make_plain_diff,
    'json': json.make_json_diff
}

DIFF_STYLE = {
    'stylish': stylish.get_stylish_diff,
    'plain': plain.get_plain_diff,
    'json': json.get_json_diff
}


def get_meta(data1: Any, data2: Any, key) -> str:
    if isinstance(data1, dict) and isinstance(data2, dict):
        return 'nested'
    elif data1 == data2:
        return 'original'
    elif data1 != data2:
        return 'changed'


def get_metachanges(data1: Any, data2: Any, key):
    if key not in data1:
        return 'added'
    elif key not in data2:
        return 'removed'
    else:
        return 'updated'


def get_diff(data1: Dict[str, Any], data2: Dict[str, Any]) -> Dict[str, tuple]:
    diff = {}
    for key in sorted(set(data1) | set(data2)):
        val1, val2 = data1.get(key), data2.get(key)
        if get_meta(val1, val2, key) == 'nested':
            nested_diff = get_diff(val1, val2)
            if nested_diff:
                diff[key] = 'nested', nested_diff
        elif get_meta(val1, val2, key) == 'original':
            diff[key] = 'original', val1
        elif get_meta(val1, val2, key) == 'changed':
            diff[key] = get_metachanges(data1, data2, key), (val1, val2)
    return diff


def format_diff(style: str, diff: Dict[str, Any],
                path: str = '') -> Dict[str, Any] or str:
    variable = {}
    for key, (meta, value) in diff.items():
        if meta == 'nested':
            nested_diff = format_diff(style, value, path + key + '.')
            if nested_diff:
                variable[key] = nested_diff
        else:
            FORMATTERS[style](diff, variable, path)
    return variable


def generate_diff(path_file1: Path, path_file2: Path,
                  style: str = 'stylish') -> str:
    if style not in DIFF_STYLE and style not in FORMATTERS:
        raise ValueError(f'Invalid format: {style}')
    data1 = get_data(path_file1)
    data2 = get_data(path_file2)
    diff = get_diff(data1, data2)
    formatted_diff = format_diff(style, diff)
    result = DIFF_STYLE[style](formatted_diff)
    return result
