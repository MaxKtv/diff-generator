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


def get_meta(data1: Dict[str, Any], data2: Dict[str, Any]) -> str:
    if isinstance(data1, dict) and isinstance(data2, dict):
        return 'nested'
    elif data1 == data2:
        return 'original'
    elif data1 != data2:
        return 'changed'


def get_diff(data1: Dict[str, Any], data2: Dict[str, Any]) -> Dict[str, Any]:
    diff = {}
    for key in sorted(set(data1) | set(data2)):
        val1, val2 = data1.get(key), data2.get(key)
        if get_meta(val1, val2) == 'nested':
            nested_diff = get_diff(val1, val2)
            if nested_diff:
                diff[key] = nested_diff
        elif get_meta(val1, val2) == 'original':
            diff[key] = 'original'
        elif get_meta(val1, val2) == 'changed':
            diff[key] = 'changed'
    return diff


def format_diff(func, diff: Dict[str, Any],
                data1: Dict[str, Any],
                data2: Dict[str, Any]) -> Dict[str, Any] or str:
    variable = {}
    for key in sorted(diff):
        if isinstance(diff[key], dict):
            nested_diff = format_diff(func, diff[key], data1[key], data2[key])
            if nested_diff:
                variable[key] = nested_diff
        else:
            func(diff, data1, data2, variable)
    return variable


def generate_diff(path_file1: Path, path_file2: Path,
                  style: str = 'stylish') -> str:
    if style not in DIFF_STYLE and style not in FORMATTERS:
        raise ValueError(f'Invalid format: {style}')
    data1 = get_data(path_file1)
    data2 = get_data(path_file2)
    diff = get_diff(data1, data2)
    formatted_diff = format_diff(FORMATTERS[style], diff, data1, data2)
    return DIFF_STYLE[style](formatted_diff)
