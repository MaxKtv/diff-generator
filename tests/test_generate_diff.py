import pytest
from pathlib import Path
from gendiff import generate_diff


def get_path(file_name):
    p = Path(__file__)
    current_dir = p.absolute().parent
    return current_dir / 'fixtures' / file_name


def test_generate_diff():
    file1 = get_path('file1.json')
    file2 = get_path('file2.json')
    expected = get_path('expected.txt')
    with open(expected, 'r') as e:
        assert generate_diff.generate_diff(file1, file2) == e.read()