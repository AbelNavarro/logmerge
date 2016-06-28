#!/usr/bin/python

import argparse

def parse_args(args):
    parser = argparse.ArgumentParser(description='logmerge - merge multiple log files chronologically')
    
    return parser.parse_args(args)


def main():
    parser = parse_args(sys.argv[1:])


if __name__ == '__main__':
    main()

