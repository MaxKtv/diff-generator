from gendiff.parser import get_data
from gendiff.formatters import plain, stylish
from pathlib import Path


def get_diff(d1: dict, d2: dict) -> tuple:
    diff = dict()
    flat_diff = list()
    for key in sorted(set(d1) | set(d2)):
        val1, val2 = d1.get(key), d2.get(key)
        if isinstance(val1, dict) and isinstance(val2, dict):
            nested_diff, nested_flat_diff = get_diff(val1, val2)
            if nested_diff:
                diff[key] = nested_diff
                flat_diff.extend(nested_flat_diff)
        else:
            if key not in d1:
                diff[f'+ {key}'] = val2
                flat_diff.append(
                    f"Property '{plain.format_path(d2[key], d2)}' "
                    f"was added with value: {plain.format_value(val2)}\n"
                )
            elif key not in d2:
                diff[f'- {key}'] = val1
                flat_diff.append(
                    f"Property '{plain.format_path(d1[key], d1)}' "
                    f"was removed\n"
                )
            elif val1 == val2:
                diff[f'  {key}'] = val1
            elif val1 != val2:
                diff[f'- {key}'] = val1
                diff[f'+ {key}'] = val2
                flat_diff.append(
                    f"Property '{plain.format_path(d1[key], d1)}' "
                    f"was updated. From {plain.format_value(val1)} "
                    f"to {plain.format_value(val2)}\n"
                )

    return stylish.stylize(diff), ''.join(flat_diff)


def generate_diff(file1: Path, file2: Path, style: str = 'stylish') -> str:
    data1, data2 = get_data(file1, file2)
    stylish_diff, plain_diff = get_diff(data1, data2)
    if style == 'stylish':
        return stylish_diff
    elif style == 'plain':
        return plain_diff
    elif style == 'json':
        pass
    else:
        raise ValueError(f'Invalid format: {style}')
