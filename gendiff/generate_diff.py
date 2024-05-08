from gendiff.parser import get_data
from gendiff.formatters import stylish, plain, json
from pathlib import Path
from typing import Dict, Any, Tuple


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


def get_meta(data1: Any, data2: Any) -> str:
    """"
    Compares value of data1 and data2

    Args:
        data1 (Any): Value of data1
        data2 (Any): Value of data2

    Returns:
        str: meta of data1 in reference of data2
    """
    if isinstance(data1, dict) and isinstance(data2, dict):
        return 'nested'
    elif data1 == data2:
        return 'original'
    elif data1 != data2:
        return 'changed'


def get_meta_changes(data1: Any, data2: Any, key):
    """
    Gives exactly information about changes in data1 and data2

    Args:
        data1 (Any): changed Value of data1
        data2 (Any): changed Value of data2
        key (str): key from union-keys of data1 and data2
            which was changed or which value was changed

    Returns:
        str: meta of data1 in reference of data2
    """
    if key not in data1:
        return 'added'
    elif key not in data2:
        return 'removed'
    else:
        return 'updated'


def get_diff(data1: Dict[str, Any],
             data2: Dict[str, Any]) -> Dict[str, Tuple[str, Any]]:
    """
    Builds the new "diff" dictionary
    which contains all keys-values
    (from data1 and data2) and meta
    of data1 in reference of data2

    Args:
        data1 (Dict[str, Any]): Parsed data from file1
        data2 (Dict[str, Any]): Parsed data from file2

    Returns
        Dict[str, Tuple[str, Any]]: Dictionary of difference data1 and data2
    """
    diff = {}
    for key in sorted(set(data1) | set(data2)):
        val1, val2 = data1.get(key), data2.get(key)
        if get_meta(val1, val2) == 'nested':
            nested_diff = get_diff(val1, val2)
            if nested_diff:
                diff[key] = 'nested', nested_diff
        elif get_meta(val1, val2) == 'original':
            diff[key] = 'original', val1
        elif get_meta(val1, val2) == 'changed':
            diff[key] = get_meta_changes(data1, data2, key), (val1, val2)

    return diff


def format_diff(style: str, diff: Dict[str, Tuple[str, Any]],
                path: str = '') -> Dict[str, Any] or str:
    """
    Builds the dictionary for one of formatters
    in accordance with style

    Args:
        style (str): style of difference-information.
                    Defines which formatter should be used.
                    Set by user. By default, style is stylish
        diff (Dict[str, Tuple[str, Any]]): Dictionary of difference
                                          data of file1 and file2
        path (str, optional): path to file presented in way of enum of keys

    Returns:
        Dict[str, Any]: Difference data of file1 and file2 in set style.
                        Presented in Dictionary
    """
    formatter_dict = {}
    for key, (meta, value) in diff.items():
        if meta == 'nested':
            nested_diff = format_diff(style, value, path + key + '.')
            if nested_diff:
                formatter_dict[key] = nested_diff
        else:
            FORMATTERS[style](diff, formatter_dict, path)

    return formatter_dict


def generate_diff(path_file1: Path, path_file2: Path,
                  style: str = 'stylish') -> str:
    """
    DIFF_STYLE[style]() определяет какой форматтер должен быть использован.
    Применяет функцию соответствующего форматтера, которая обрабатывает данные
    из словаря formatted_diff т.е. конвертирует различия представленные ввиде словаря
    в строку в заданном стиле.
    """
    if style not in DIFF_STYLE and style not in FORMATTERS:
        raise ValueError(f'Invalid format: {style}')
    data1 = get_data(path_file1)
    data2 = get_data(path_file2)
    diff = get_diff(data1, data2)
    formatted_diff = format_diff(style, diff)
    result = DIFF_STYLE[style](formatted_diff)
    return result
