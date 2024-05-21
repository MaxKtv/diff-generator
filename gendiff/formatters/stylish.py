from itertools import chain
from typing import Dict, Any, Tuple


REPLACER = ' '
SPACE_COUNT = 4
STYLISH_META = {
    'added': '+ ',
    'original': '  ',
    'removed': '- ',
    'updated': ('- ', '+ '),
    'nested': '  '
}
INBORN_INDENT = len(STYLISH_META[next(iter(STYLISH_META))])


def stringify_value(node: Any, depth: int = 0) -> str:
    """
    Turns node to "stylish" style string

    Args:
        node (Any): variable to be stringified
        depth (int, optional): Dictionary's level of depth. Defaults to 0.

    Returns:
        str: "stylish" style difference
    """
    if not isinstance(node, dict):
        return normalize_value(node, depth)
    lines = []
    indent = get_indents(depth)
    base_indent = get_indents(depth + 1)
    for key, value in sorted(node.items()):
        if isinstance(value, tuple):
            meta, val = value
            if meta == 'updated':
                old_val, new_val = val
                lines.append(f"{base_indent}{STYLISH_META['removed']}{key}: "
                             f"{normalize_value(old_val, depth + 1)}")
                lines.append(f"{base_indent}{STYLISH_META['added']}{key}: "
                             f"{normalize_value(new_val, depth + 1)}")
            else:
                formatted_value = stringify_value(val, depth + 1) \
                    if meta == 'nested' else normalize_value(val, depth + 1)
                lines.append(f"{base_indent}{STYLISH_META[meta]}{key}: "
                             f"{formatted_value}")
        else:
            lines.append(f"{base_indent}{STYLISH_META['original']}{key}: "
                         f"{normalize_value(value, depth + 1)}")
    result = chain(
        '{', lines, [
            (indent + '}') if len(indent) < 1 else (indent + '  ' + '}')
        ]
    )
    return '\n'.join(result)


def normalize_value(obj: Any, depth: int) -> str:
    """
    Converts object(values) to string

    Args:
        obj (Any): Object to be converted
        depth (int, optional): Dictionary's level of depth

    Returns:
        str: Converted string
    """
    if isinstance(obj, bool):
        return str(obj).lower()
    elif obj is None:
        return 'null'
    elif isinstance(obj, (str | int | float)):
        return str(obj)
    elif isinstance(obj, dict):
        return stringify_value(obj, depth)


def get_indents(depth: int) -> str:
    """
    Builds indent in accordance with depth

    Args:
        depth (int, optional): Dictionary's level of depth

    Returns:
        str: indent
    """
    if depth <= 0:
        return ''
    return REPLACER * (depth * SPACE_COUNT - INBORN_INDENT)


def get_stylish_diff(diff: Dict[str, Tuple[str, Any]]) -> str:
    """
    Formats diff dictionary to "stylish" style string

    Args:
        diff (Dict[str, Tuple[str, Tuple[str, Any]]): Dictionary of difference

    Returns:
        str: "stylish" styled difference
    """
    return stringify_value(diff)
