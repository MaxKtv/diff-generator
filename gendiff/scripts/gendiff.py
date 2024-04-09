#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser(description='\n\nCompares two configuration files and shows a difference.')
parser.add_argument('first_file')
parser.add_argument('second_file')
parser.add_argument('-f', '--format', help='set format of output')

args = parser.parse_args()

