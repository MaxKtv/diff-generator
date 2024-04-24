from gendiff.parser import get_data
from typing import Dict, Any
from pathlib import Path


def format_plain_diff(diff: Dict[str, Any],
                      data1: Dict[str, Any], data2: Dict[str, Any],
                      path_file1: Path, path_file2: Path) -> str:
    text = []
    for key in sorted(diff):
        if isinstance(diff[key], dict):
            nested_diff = format_plain_diff(diff[key], data1[key], data2[key],
                                            path_file1, path_file2)
            if nested_diff:
                text.append(nested_diff)
        else:
            make_plain_diff(diff, key, data1, data2,
                            path_file1, path_file2, text)
    return '\n'.join(text)


def make_plain_diff(diff: Dict[str, Any], key: str,
                    data1: Dict[str, Any], data2: Dict[str, Any],
                    path_file1: Path, path_file2: Path, text: list) -> str:
    full_data1 = get_data(path_file1)
    full_data2 = get_data(path_file2)
    if diff[key] == 'changed':
        if key not in data2:
            text.append(f"Property '{format_path(key, full_data1)}' "
                        f"was removed")
        elif key not in data1:
            text.append(
                f"Property '{format_path(key, full_data2)}' was added "
                f"with value: {format_value(data2[key])}"
            )
        else:
            text.append(
                f"Property '{format_path(key, full_data1)}' was updated. "
                f"From {format_value(data1[key])} "
                f"to {format_value(data2[key])}")
    return text


def format_value(value: Any) -> str:
    if isinstance(value, dict):
        return '[complex value]'
    if value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    return f"'{value}'" if isinstance(value, str) else str(value)


def format_path(endpoint: str, data: Dict[str, Any],
                path: list = []) -> str or None:
    if endpoint in data:
        return '.'.join(path + [endpoint])
    for key, value in data.items():
        if isinstance(value, dict):
            nested_path = format_path(endpoint, value, path + [key])
            if nested_path:
                return nested_path
    return None
