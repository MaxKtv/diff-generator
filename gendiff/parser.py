from json import load
from yaml import safe_load
from pathlib import Path
from typing import Dict, Any


EXTENSIONS = {
    'json': load,
    'yaml': safe_load,
    'yml': safe_load
}


def get_data(file: Path, ext: str) -> Dict[str, Any]:
    with open(file) as open_file:
        if ext in EXTENSIONS:
            data = EXTENSIONS[ext](open_file)
            return data
        else:
            extensions = ', '.join(EXTENSIONS.keys())
            raise ValueError(f'Oh no, something went wrong'
                             f'\nSupported extensions are:'
                             f'\n>>> {extensions}')
