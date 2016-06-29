#!/usr/bin/python

import argparse
import sys
import re
import datetime


def parse_args(args):
    parser = argparse.ArgumentParser(
            description='logmerge - merge multiple log files chronologically',
            argument_default=argparse.SUPPRESS)
    parser.add_argument('files', nargs='*', help='files to merge')
    parser.add_argument('-v', '--verbose', help='increase verbosity', action='count')
    return parser.parse_args(args)


def get_dateformat(line):
    if not line:
        return 'empty'

    if line.startswith('['):
        return 'chefclient'
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    if line[:3] in months:
        return 'pacemaker'

    match = re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}', line)
    if match:
        return 'nova'

    match = re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z', line)
    if match:
        return 'ovs'

    match = re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}\+[0-9]{2}:[0-9]{2}', line)
    if match:
        return 'messages'

    return 'unknown'


def get_dateread(line):
    datetype = get_dateformat(line)
    if datetype == 'nova':
        dt1 = datetime.datetime.strptime(line[:23], '%Y-%m-%d %H:%M:%S.%f')
        return dt1


def main():
    res = parse_args(sys.argv[1:])

    if res == argparse.Namespace():
        print 'usage'
        return 0
    
    if len(res.files) < 2:
        print 'Need at least two files to merge'
        return 1
   
    files = []
    for file in res.files:
        files.append(open(file, 'r'))

    for file in files:
        print file.readline()


if __name__ == '__main__':
    main()

