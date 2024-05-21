from typing import Dict, Any, Tuple
from json import dumps
from gendiff.formatters.plain import normalize_plain_value


def format_json_diff(diff: Dict[str, Tuple[str, Any]]) -> Dict[str, Any]:
    """
     Formats diff dictionary to "json" style dictionary

     Args:
         diff (Dict[str, Tuple[str, Any]]): Dictionary of difference
                                            data1 and data2

     Returns:
         Dict[str, Any]: Dictionary of difference "json" style
     """
    formatter_dict = {}
    for key, (meta, value) in diff.items():
        if meta == 'nested':
            nested = format_json_diff(value)
            formatter_dict[key] = nested
        elif meta == 'updated':
            data1_value = value[0]
            data2_value = value[1]
            formatter_dict[key] = (f'{normalize_plain_value(data1_value)}: '
                                   f'{meta} -> '
                                   f'{normalize_plain_value(data2_value)}')
        else:
            formatter_dict[key] = f'{normalize_plain_value(value)}: {meta}'
    return formatter_dict


def get_json_diff(diff: Dict[str, Tuple[str, Any]]) -> str:
    """
    Formats diff dictionary to "json" style

    Args:
         diff (Dict[str, Tuple[str, Any]]): Dictionary of difference
                                            data1 and data2

    Returns:
        str: "json" styled difference
    """
    formatter_dict: Dict[str, Any] = format_json_diff(diff)
    json_diff = dumps(formatter_dict, indent=4)
    return json_diff
