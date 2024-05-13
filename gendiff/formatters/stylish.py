from typing import Dict, Any, Tuple

STYLISH_META = {
    'added': '+ ',
    'original': '  ',
    'removed': '- ',
    'updated': ('- ', '+ ')
}


def format_stylish_diff(diff: Dict[str, Tuple[str, Any]]) -> Dict[str, Any]:
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
    if isinstance(obj, str | int | float):
        return obj if not isinstance(obj, bool) else str(obj).lower()
    elif obj is None:
        return 'null'
    else:
        return obj


def stringify_stylish_diff(formatter_dict: Dict[str, Any],
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


def get_stylish_diff(diff: Dict[str, Tuple[str, Any]]) -> str:
    formatter_dict = format_stylish_diff(diff)
    stylish_diff = stringify_stylish_diff(formatter_dict)
    return stylish_diff
