import argparse


def argumentize():
    """
    Creates a command-line argument parser for comparing files.

    Returns:
        An argparse.ArgumentParser instance ready
        to parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description='\n\nCompares two configuration files'
                    ' and shows a difference.')
    parser.add_argument('first_file', help='first configuration file')
    parser.add_argument('second_file', help='second configuration file')
    parser.add_argument('-f', '--format', help='set format of output',
                        default='stylish',
                        choices=['stylish', 'plain', 'json'])

    return parser.parse_args()
