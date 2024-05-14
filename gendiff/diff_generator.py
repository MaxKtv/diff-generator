from gendiff.parser import get_data
from gendiff.formatters import stylish, plain, json
from pathlib import Path
from typing import Dict, Any, Tuple

DIFF_STYLE = {
    'stylish': stylish.get_stylish_diff,
    'plain': plain.get_plain_diff,
    'json': json.get_json_diff
}


def get_extension(file: Path) -> str:
    """
     Gets file extension

     Args:
         file (Path): path to file

     Returns
         str: Extension of file without a dot
     """
    file_extension = file.suffix
    undot_file_extension = file_extension[1:]
    return undot_file_extension


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
    keys = sorted(set(data1) | set(data2))
    for key in keys:
        val1, val2 = data1.get(key), data2.get(key)
        if isinstance(val1, dict) and isinstance(val2, dict):
            nested_diff = get_diff(val1, val2)
            diff[key] = ('nested', nested_diff) \
                if nested_diff else ('original', val1)
        elif val1 == val2:
            diff[key] = ('original', val1)
        elif key not in data1:
            diff[key] = ('added', val2)
        elif key not in data2:
            diff[key] = ('removed', val1)
        else:
            diff[key] = ('updated', (val1, val2))
    return diff


def generate_diff(path_file1: Path, path_file2: Path,
                  style: str = 'stylish') -> str:
    """
    The engine of utility program
    Generates the diff in accordance with style

    Args:
        path_file1 (Path): path to file1
        path_file2 (Path): path to file2
        style (str): style of difference-information.
                    Defines which formatter should be used.
                    Set by user. By default, style is stylish

    Returns
        str: Styled difference of file1 and file2
    """
    if style not in DIFF_STYLE:
        raise ValueError(f'Invalid format: {style}')
    file_ext1 = get_extension(path_file1)
    file_ext2 = get_extension(path_file2)
    data1 = get_data(path_file1, file_ext1)
    data2 = get_data(path_file2, file_ext2)
    diff = get_diff(data1, data2)

    return DIFF_STYLE[style](diff)
