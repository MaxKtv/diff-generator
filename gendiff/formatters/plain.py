from typing import Dict, Any, Tuple


def make_plain_diff(diff: Dict[str, Tuple[str, Any]],
                    formatter_dict: Dict[str, Any],
                    path: str) -> Dict[str, Any]:

    for key, (meta, value) in diff.items():

        if meta == 'added':
            formatter_dict[key] = (f"Property '{path}{key}' "
                                   f"was added with value: "
                                   f"{format_value(value[1])}")
        elif meta == 'removed':
            formatter_dict[key] = (f"Property '{path}{key}' "
                                   f"was removed")
        elif meta == 'updated':
            formatter_dict[key] = (f"Property '{path}{key}' "
                                   f"was updated. From "
                                   f"{format_value(value[0])} "
                                   f"to {format_value(value[1])}")

    return formatter_dict


def format_value(value: Any) -> str:
    if isinstance(value, dict):
        return '[complex value]'
    if value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    return f"'{value}'" if isinstance(value, str) else str(value)


def get_plain_diff(formatted_diff: Dict[str, Any]) -> str:

    def extract_values(dictionary: Dict[str, Any]) -> Dict[str, Any]:
        for value in dictionary.values():
            if isinstance(value, dict):
                yield from extract_values(value)
            else:
                yield value

    return '\n'.join(str(value) for value in extract_values(formatted_diff))
