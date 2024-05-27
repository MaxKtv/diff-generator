import sys
from gendiff.cli import argumentize
from gendiff.diff_generator import generate_diff

ERRORS = (ValueError, KeyError, FileNotFoundError)


def main():
    try:
        args = argumentize()
        print(generate_diff(args.first_file, args.second_file, args.format))
        sys.exit(0)
    except ERRORS as e:
        print(f"An ERROR occurred: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
