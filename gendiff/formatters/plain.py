from typing import Dict, Any


def make_plain_diff(diff: Dict[str, Any], key: str,
                    data1: Dict[str, Any], data2: Dict[str, Any],
                    variable: Dict[str, Any]) -> Dict[str, Any]:

    if diff[key] == 'changed':
        if key not in data2:

            variable[key] = (f"Property '{format_path(key, data1)}' "
                             f"was removed")
        elif key not in data1:
            variable[key] = (
                f"Property '{format_path(key, data2)}' was added "
                f"with value: {format_value(data2[key])}"
            )
        else:
            variable[key] = (
                f"Property '{format_path(key, data2)}' was updated. "
                f"From {format_value(data1[key])} "
                f"to {format_value(data2[key])}"
            )

    return variable


def format_value(value: Any) -> str:
    if isinstance(value, dict):
        return '[complex value]'
    if value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    return f"'{value}'" if isinstance(value, str) else str(value)


def format_path(endpoint: str, data: str,
                path: list = []) -> str or None:

    if endpoint in data:
        return '.'.join(path + [endpoint])
    for key, value in data.items():
        if isinstance(value, dict):
            nested_path = format_path(endpoint, value, path + [key])
            if nested_path:
                return nested_path
    return None


def get_plain_diff(formatted_diff: Dict[str, Any]) -> str:
    def extract_values(dictionary: Dict[str, Any]) -> Dict[str, Any]:
        for value in dictionary.values():
            if isinstance(value, dict):
                yield from extract_values(value)
            else:
                yield value

    return '\n'.join(str(value) for value in extract_values(formatted_diff))
