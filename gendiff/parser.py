from json import load
from yaml import safe_load
from pathlib import Path
from typing import Dict, Any

EXTENSIONS = {'.json': load, '.yaml': safe_load, '.yml': safe_load}


def get_file_extension(file: Path) -> str:
    file = Path(file)
    return file.suffix


def get_data(file: Path) -> Dict[str, Any]:
    with open(file) as open_file:
        ext = get_file_extension(file)
        if ext in EXTENSIONS:
            data = EXTENSIONS[ext](open_file)
            return data
        else:
            raise ValueError('Oh no, something went wrong'
                             '\nSupported extensions are:'
                             '\n>>> .json, .yaml and .yml')
