from typing import Dict, Any, Tuple


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
        if val1 == val2:
            diff[key] = ('original', val1)
        elif isinstance(val1, dict) and isinstance(val2, dict):
            nested_diff = get_diff(val1, val2)
            diff[key] = ('nested', nested_diff)
        elif key not in data1:
            diff[key] = ('added', val2)
        elif key not in data2:
            diff[key] = ('removed', val1)
        elif data1[key] != data2[key]:
            diff[key] = ('updated', (val1, val2))

    return diff
