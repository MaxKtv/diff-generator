def format_value(value):
    if isinstance(value, dict):
        return '[complex value]'
    if value is None:
        value = 'null'
    elif isinstance(value, bool):
        value = str(value).lower()
    return f"'{value}'" if isinstance(value, str) else str(value)


def format_path(target, data):
    pass
