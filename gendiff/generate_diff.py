from gendiff.parser import get_data
from gendiff.formatters import stylish, plain
from pathlib import Path
from typing import Dict, Any


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


def generate_diff(path_file1: Path, path_file2: Path,
                  style: str = 'stylish') -> str:
    data1 = get_data(path_file1)
    data2 = get_data(path_file2)
    diff = get_diff(data1, data2)
    if style == 'stylish':
        stylish_diff_dict = stylish.format_stylish_diff(diff, data1, data2)
        return stylish.stylize(stylish_diff_dict)
    elif style == 'plain':
        plain_diff = plain.format_plain_diff(diff, data1, data2,
                                             path_file1, path_file2)
        return plain_diff
    elif style == 'json':
        pass
    else:
        raise ValueError(f'Invalid format: {style}')
