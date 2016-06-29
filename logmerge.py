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
        return datetime.datetime.strptime(line[:23], '%Y-%m-%d %H:%M:%S.%f')

    if datetype == 'ovs':
        return datetime.datetime.strptime(line[:23], '%Y-%m-%dT%H:%M:%S.%f')

    if datetype == 'pacemaker':
        dt = datetime.datetime.strptime(line[:15], '%b %d %H:%M:%S')
        return dt.replace(year=datetime.date.today().year)

    if datetype == 'messages':
        return datetime.datetime.strptime(line[:26], '%Y-%m-%dT%H:%M:%S.%f')

    if datetype == 'chefclient':
        return datetime.datetime.strptime(line[:20], '[%Y-%m-%dT%H:%M:%S')


class LogFile:
    def __init__(self, file):
        self.file = file
        self.datetime = datetime.datetime.min
        self.line = ''

    def update(self):
        self.line = self.file.readline()
        self.datetime = get_dateread(self.line)
        while self.line and self.datetime is None:
            self.line = self.file.readline()
            self.datetime = get_dateread(self.line)


    def output(self):
        print self.line.rstrip()
        self.update()

    def has_lines(self):
        return self.line


def main():
    res = parse_args(sys.argv[1:])

    if res == argparse.Namespace():
        print 'usage'
        return 0
    
    if len(res.files) < 2:
        print 'Need at least two files to merge'
        return 1
   
    files = []
    for filename in res.files:
        file = LogFile(open(filename, 'r'))
        file.update()
        files.append(file)

    while files:
        files = sorted(files, key=lambda logfile: logfile.datetime)
        files[0].output()
        if not files[0].has_lines():
            del files[0]
            print 'deleted file'


if __name__ == '__main__':
    main()

