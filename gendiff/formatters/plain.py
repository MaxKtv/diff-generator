from typing import Dict, Any, Tuple


def format_plain_diff(diff: Dict[str, Tuple[str, Any]],
                      path: str = '') -> Dict[str, Any]:
    """
     Formats diff dictionary to "plain" style dictionary

     Args:
         diff (Dict[str, Tuple[str, Any]]): Dictionary of difference
                                            data1 and data2
        path (str, optional): Path to value based on keys. Defaults to ''.

     Returns:
         Dict[str, Any]: Dictionary of difference data1 and data2
                         in "plain" style
     """
    formatter_dict = {}
    for key, (meta, value) in diff.items():
        if meta == 'nested':
            nested = format_plain_diff(value, f'{path}{key}.')
            formatter_dict[key] = nested
        elif meta == 'added':
            formatter_dict[key] = (f"Property '{path}{key}' "
                                   f"was added with value: "
                                   f"{format_value(value)}")
        elif meta == 'removed':
            formatter_dict[key] = (f"Property '{path}{key}' "
                                   f"was removed")
        elif meta == 'updated':
            data1_value = value[0]
            data2_value = value[1]
            formatter_dict[key] = (f"Property '{path}{key}' "
                                   f"was updated. From "
                                   f"{format_value(data1_value)} "
                                   f"to {format_value(data2_value)}")

    return formatter_dict


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


def stringify_plain_diff(formatted_diff: Dict[str, Any]) -> str:
    """
    Turns "plain" styled diff dictionary into string

    Args:
       formatted_diff (Dict[str, Any]): Formatted diff dictionary

    Returns:
        str: "plain" styled difference
    """
    def extract_values(dictionary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts values from formatted diff dictionary

        Args:
          dictionary (Dict[str, Any]): Dictionary to extract values

        Yields:
            str: Extracted value
        """
        for value in dictionary.values():
            if isinstance(value, dict):
                yield from extract_values(value)
            else:
                yield value

    return '\n'.join(str(value) for value in extract_values(formatted_diff))


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
    plain_diff = stringify_plain_diff(formatter_diff)
    return plain_diff
