import pytest
from pathlib import Path
from gendiff.diff_generator import generate_diff


def get_path(file_name: str) -> Path:
    p = Path(__file__)
    current_dir = p.absolute().parent
    return current_dir / 'fixtures' / file_name


@pytest.mark.parametrize(
    'fixtures_n_style',
    [
        pytest.param(('stylish', 'file1.json', 'file2.json', 'expected_stylish.txt'),
                     id='Generate stylish-style diff'),
        pytest.param(('plain', 'file1.json', 'file2.yaml', 'expected_plain.txt'),
                     id='Generate plain-style diff'),
        pytest.param(('json', 'file1.yml', 'file2.json', 'expected_json.json'),
                     id='Generate json-style diff')
    ]
)
def test_generate_diff(fixtures_n_style):
    style, file1, file2, expected_result = fixtures_n_style
    path_file1 = get_path(file1)
    path_file2 = get_path(file2)
    path_expected = get_path(expected_result)
    expected = path_expected.read_text()
    assert generate_diff(path_file1, path_file2, style) == expected
