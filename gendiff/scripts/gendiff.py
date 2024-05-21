#!/usr/bin/env python3
import sys
from gendiff.scripts.cli import parser
from gendiff.diff_generator import generate_diff

args = parser.parse_args()


def main():
    try:
        print(generate_diff(args.first_file, args.second_file, args.format))
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
