from typing import Dict, Any, Tuple

STYLISH_META = {
    'added': '+ ',
    'original': '  ',
    'removed': '- ',
    'updated': ('- ', '+ ')
}


def format_stylish_diff(diff: Dict[str, Tuple[str, Any]]) -> Dict[str, Any]:
    """
     Formats diff dictionary to "stylish" style dictionary

     Args:
         diff (Dict[str, Tuple[str, Any]]): Dictionary of difference
                                            data1 and data2

     Returns:
         Dict[str, Any]: Dictionary of difference data1 and data2
                         in "stylish" style
     """
    formatter_dict = {}
    for key, [meta, value] in diff.items():
        if meta == 'nested':
            nested = format_stylish_diff(value)
            if nested:
                formatter_dict[key] = nested
        elif meta == 'updated':
            data1_value, stylish_meta1 = value[0], STYLISH_META[meta][0]
            data2_value, stylish_meta2 = value[1], STYLISH_META[meta][1]
            formatter_dict[f'{stylish_meta1}{key}'] = data1_value
            formatter_dict[f'{stylish_meta2}{key}'] = data2_value
        else:
            formatter_dict[f'{STYLISH_META[meta]}{key}'] = value

    return formatter_dict


def decoder(obj: Any) -> str:
    """
    Converts object(values) to string

    Args:
        obj (Any): Object to be converted

    Returns:
        str: Converted string
    """
    if isinstance(obj, str | int | float):
        return obj if not isinstance(obj, bool) else str(obj).lower()
    elif obj is None:
        return 'null'
    else:
        return obj


def stringify_stylish_diff(formatter_dict: Dict[str, Any],
                           replacer: str = ' ', spaces_count: int = 2) -> str:
    """
    Turns dictionary to "stylish" style string

    Args:
        formatter_dict (Dict[str, Any]): formatted dictionary of difference
        replacer (str, optional): replacement character. Defaults to ' '.
        spaces_count (int, optional): number of spaces to replace.
                                      Defaults to 2.

    Returns:
        str: "stylish" style difference
    """
    def stringify_value(value: Any, indent: str) -> str:
        """
        Turns value of dictionary to "stylish" style value

        Args:
            value (Any): Value to be converted
            indent (str): indentation


        Returns:
            str: "stylish" styled value
        """
        if not isinstance(value, dict):
            return decoder(value)
        else:
            lines = []
            for key, val in value.items():
                inborn_indent_count = 2
                format_value = stringify_value(val, indent + replacer
                                               * spaces_count
                                               * inborn_indent_count)
                lines.append(
                    f'{indent}'
                    f'{key if not key[0].isalpha() else f"  {key}"}:'
                    f'{" "}'
                    f'{format_value}'
                )
            if lines:
                return ('{\n' + '\n'.join(lines) + '\n'
                        + indent[:-spaces_count * len(replacer)] + '}')

    return stringify_value(formatter_dict, replacer * spaces_count)


def get_stylish_diff(diff: Dict[str, Tuple[str, Any]]) -> str:
    """
    Formats diff dictionary to "stylish" style string

    Args:
        diff (Dict[str, Tuple[str, Any]]): Dictionary of difference

    Returns:
        str: "stylish" styled difference
    """
    formatter_dict = format_stylish_diff(diff)
    stylish_diff = stringify_stylish_diff(formatter_dict)
    return stylish_diff
