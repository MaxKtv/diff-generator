import sys
from gendiff.cli import create_parser
from gendiff.diff_generator import generate_diff


def main():
    try:
        args = create_parser()
        print(generate_diff(args.first_file, args.second_file, args.format))
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
