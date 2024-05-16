from typing import Dict, Any, Tuple


def format_plain_diff(diff: Dict[str, Tuple[str, Any]],
                      path: str = '') -> list:
    """
     Formats diff dictionary to "plain" style list

     Args:
         diff (Dict[str, Tuple[str, Any]]): Dictionary of difference
                                            data1 and data2
        path (str, optional): Path to value based on keys. Defaults to ''.

     Returns:
         Dict[str, Any]: List of difference data1 and data2
                         in "plain" style
     """
    formatter_list = []
    for key, (meta, value) in diff.items():
        if meta == 'nested':
            nested = format_plain_diff(value, f'{path}{key}.')
            formatter_list.extend(nested)
        elif meta == 'added':
            formatter_list.append(f"Property '{path}{key}' "
                                  f"was added with value: "
                                  f"{format_value(value)}")
        elif meta == 'removed':
            formatter_list.append(f"Property '{path}{key}' "
                                  f"was removed")
        elif meta == 'updated':
            data1_value = value[0]
            data2_value = value[1]
            formatter_list.append(f"Property '{path}{key}' "
                                  f"was updated. From "
                                  f"{format_value(data1_value)} "
                                  f"to {format_value(data2_value)}")
    return formatter_list


def format_value(value: Any) -> str:
    """
    Formats value of diff to "plain" style value

    Args:
        value (Any): Value to format

    Returns:
        str: "plain" styled value
    """
    if isinstance(value, dict):
        return '[complex value]'
    if value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    return f"'{value}'" if isinstance(value, str) else str(value)


def get_plain_diff(diff: Dict[str, Tuple[str, Any]]) -> str:
    """
     Formats diff dictionary to "plain" style

     Args:
         diff (Dict[str, Tuple[str, Any]]): Dictionary of difference
                                            data1 and data2

     Returns:
         str: "plain" styled difference
     """
    formatter_diff = format_plain_diff(diff)
    plain_diff = '\n'.join(formatter_diff)
    return plain_diff
