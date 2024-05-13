import pytest
from pathlib import Path
from gendiff import diff_generator


def get_path(file_name):
    p = Path(__file__)
    current_dir = p.absolute().parent
    return current_dir / 'fixtures' / file_name


def test_generate_stylish_diff():
    file1_j, file1_y = get_path('file1.json'), get_path('file1.yml')
    file2_j, file2_y = get_path('file2.json'), get_path('file2.yaml')
    expected = get_path('expected_stylish.txt')
    with open(expected, 'r') as e:
        assert diff_generator.generate_diff(file1_j, file2_j) == e.read()
    with open(expected, 'r') as e:
        assert diff_generator.generate_diff(file1_y, file2_y) == e.read()


def test_generate_plain_diff():
    file1_j, file1_y = get_path('file1.json'), get_path('file1.yml')
    file2_j, file2_y = get_path('file2.json'), get_path('file2.yaml')
    expected = get_path('expected_plain.txt')
    with open(expected, 'r') as e:
        assert diff_generator.generate_diff(file1_j, file2_j, 'plain') == e.read()
    with open(expected, 'r') as e:
        assert diff_generator.generate_diff(file1_y, file2_y, 'plain') == e.read()


def test_generate_json_diff():
    file1_j, file1_y = get_path('file1.json'), get_path('file1.yml')
    file2_j, file2_y = get_path('file2.json'), get_path('file2.yaml')
    expected = get_path('expected_json.json')
    with open(expected, 'r') as e:
        assert diff_generator.generate_diff(file1_j, file2_j, 'json') == e.read()
    with open(expected, 'r') as e:
        assert diff_generator.generate_diff(file1_y, file2_y, 'json') == e.read()
