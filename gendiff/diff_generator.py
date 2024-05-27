from gendiff import diff, parser
from gendiff.formatters import stylish, plain, json
from pathlib import Path

DIFF_STYLE = {
    'stylish': stylish.get_stylish_diff,
    'plain': plain.get_plain_diff,
    'json': json.get_json_diff
}


def read_file(file):
    """
     Opens and reads a file

     Args:
         file: Path to the file

     Returns
         Contents of the file
     """
    with open(file, 'r') as f:
        return f.read()


def get_extension(file: str | Path) -> str:
    """
     Gets file extension without a dot

     Args:
         file (str | Path): path to file

     Returns
         str: Extension of file without a dot
     """
    if isinstance(file, str):
        return file.split('.')[-1]
    elif isinstance(file, Path):
        extension = file.suffix
        return extension[1:]


def generate_diff(path_file1: Path, path_file2: Path,
                  style: str = 'stylish') -> str:
    """
    The engine of utility program
    Generates the diff in accordance with style

    Args:
        path_file1 (Path): path to file1
        path_file2 (Path): path to file2
        style (str): style of difference-information.
                    Defines which formatter should be used.
                    Set by user. By default, style is stylish

    Returns
        str: Styled difference of file1 and file2
    """
    if style not in DIFF_STYLE:
        raise ValueError(f'Oh no, something went wrong'
                         f'Unsupported format: {style} '
                         f'supported formats are -> '
                         f'{", ".join(list(DIFF_STYLE))}\n')
    file_ext1 = get_extension(path_file1)
    file_ext2 = get_extension(path_file2)
    data1 = read_file(path_file1)
    data2 = read_file(path_file2)
    parsed_data1 = parser.parse_data(data1, file_ext1)
    parsed_data2 = parser.parse_data(data2, file_ext2)
    diff_dict = diff.get_diff(parsed_data1, parsed_data2)
    return DIFF_STYLE[style](diff_dict)
