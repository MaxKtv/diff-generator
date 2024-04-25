from typing import Dict, Any


def make_stylish_diff(diff: Dict[str, Any], key: str,
                      data1: Dict[str, Any], data2: Dict[str, Any],
                      dictionary: Dict[str, Any]) -> Dict[str, Any]:
    if diff[key] == 'original':
        dictionary[f'  {key}'] = data1[key]
    elif diff[key] == 'changed':
        if key not in data2:
            dictionary[f'- {key}'] = data1[key]
        elif key not in data1:
            dictionary[f'+ {key}'] = data2[key]
        else:
            dictionary[f'- {key}'] = data1[key]
            dictionary[f'+ {key}'] = data2[key]
    return dictionary


def decoder(obj: Any) -> str:
    if isinstance(obj, str | int | float):
        return obj if not isinstance(obj, bool) else str(obj).lower()
    elif obj is None:
        return 'null'
    else:
        return obj


def get_stylish_diff(formatted_diff: Dict[str, Any],
                     replacer: str = ' ', spaces_count: int = 2) -> str:

    def stringify_value(value: Any, indent: str) -> str:
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
                    f'{" " if len(str(format_value)) >= 1 else ""}'
                    f'{format_value}'
                )
            if lines:
                return ('{\n' + '\n'.join(lines) + '\n'
                        + indent[:-spaces_count * len(replacer)] + '}')

    return stringify_value(formatted_diff, replacer * spaces_count)
