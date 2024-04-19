from json import load
from yaml import safe_load
from pathlib import Path

FORMATTER = {'json': load, 'yaml': safe_load, 'yml': safe_load}


def get_data(file1: Path, file2: Path) -> tuple:
    with (open(file1, 'r') as f1,
          open(file2, 'r') as f2):
        ext1 = f1.name.split('.')[-1]
        ext2 = f2.name.split('.')[-1]
        if ext1 and ext2 in FORMATTER:
            data1 = FORMATTER[ext1](f1)
            data2 = FORMATTER[ext2](f2)
            return data1, data2
        else:
            raise ValueError('Oh no, something went wrong'
                             '\nSupported extensions are:'
                             '\n>>> .json, .yaml and .yml')
