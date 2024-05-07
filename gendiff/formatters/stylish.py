from typing import Dict, Any, Tuple


def make_stylish_diff(diff: Dict[str, Tuple[str, Any]],
                      formatter_dict: Dict[str, Any], _) -> Dict[str, Any]:

    for key, [meta, value] in diff.items():
        if meta == 'original':
            formatter_dict[f'  {key}'] = value
        elif meta == 'removed':
            formatter_dict[f'- {key}'] = value[0]
        elif meta == 'added':
            formatter_dict[f'+ {key}'] = value[1]
        elif meta == 'updated':
            formatter_dict[f'- {key}'] = value[0]
            formatter_dict[f'+ {key}'] = value[1]

    return formatter_dict


def decoder(obj: Any) -> str:
    if isinstance(obj, str | int | float):
        return obj if not isinstance(obj, bool) else str(obj).lower()
    elif obj is None:
        return 'null'
    else:
        return obj


def get_stylish_diff(formatter_dict: Dict[str, Any],
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
                    f'{" " if len(str(format_value)) >= len(replacer) else ""}'
                    f'{format_value}'
                )
            if lines:
                return ('{\n' + '\n'.join(lines) + '\n'
                        + indent[:-spaces_count * len(replacer)] + '}')

    return stringify_value(formatter_dict, replacer * spaces_count)
