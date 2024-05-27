import sys
from gendiff.cli import parse_cli_args
from gendiff.diff_generator import generate_diff


def main():
    try:
        args = parse_cli_args()
        print(generate_diff(args.first_file, args.second_file, args.format))
        sys.exit(0)
    except (ValueError, KeyError) as err:
        print(err)
        sys.exit(1)
    except Exception as e:
        print(f'An ERROR occurred:{e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
