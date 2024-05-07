from typing import Dict, Any


def make_stylish_diff(diff: Dict[str, Any], variable: Dict[str, Any],
                      _) -> Dict[str, Any]:
    for key, [meta, value] in diff.items():
        if meta == 'original':
            variable[f'  {key}'] = value
        elif meta == 'removed':
            variable[f'- {key}'] = value[0]
        elif meta == 'added':
            variable[f'+ {key}'] = value[1]
        elif meta == 'updated':
            variable[f'- {key}'] = value[0]
            variable[f'+ {key}'] = value[1]
    return variable


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
