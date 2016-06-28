#!/usr/bin/python

import argparse

def parse_args(args):
    parser = argparse.ArgumentParser(
            description='logmerge - merge multiple log files chronologically',
            argument_default=argparse.SUPPRESS)
    parser.add_argument('files', nargs='*', help='files to merge')
    parser.add_argument('-v', '--verbose', help='increase verbosity', action='count')
    return parser.parse_args(args)


def main():
    parser = parse_args(sys.argv[1:])


if __name__ == '__main__':
    main()

