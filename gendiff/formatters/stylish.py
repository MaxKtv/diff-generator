def stylize(obj: dict, replacer: str = '    ', spaces_count: int = 1) -> str:
    def stringify_value(value, indent: str):
        if isinstance(value, (str, int, float)):
            return value
        elif isinstance(value, bool):
            return str(value).lower()
        elif value is None:
            return 'null'
        elif isinstance(value, dict):
            lines = []
            for key, val in value.items():
                format_value = stringify_value(val,
                                               indent + replacer * spaces_count)
                lines.append(
                    f'{indent + replacer * spaces_count}{key}: '
                    f'{format_value if not isinstance(format_value, bool) else str(format_value).lower()}'
                )
            if lines:
                return (
                        '{\n' + '\n'.join(lines) + '\n' + indent + '}'
                )

        else:
            pass

    return stringify_value(obj, replacer * spaces_count)
