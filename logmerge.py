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
    parser.add_argument('-f', '--print_filename', help='print filename', action='store_true', default=False)
    parser.add_argument('-l', '--print_linenum', help='print line number', action='store_true', default=False)
    return parser.parse_args(args)



class LogFile:

    class DateReader:
        def __init__(self):
            self.func = None

        def get(self, line):
            if not self.func:
                self.func = self._get_dateformat(line)

            if self.func:
                try:
                    return self.func(line)
                except ValueError:
                    return None

            return None

        def _nova(self, line):
            return datetime.datetime.strptime(line[:23], '%Y-%m-%d %H:%M:%S.%f')

        def _ovs(self, line):
            return datetime.datetime.strptime(line[:23], '%Y-%m-%dT%H:%M:%S.%f')

        def _pacemaker(self, line):
            dt = datetime.datetime.strptime(line[:15], '%b %d %H:%M:%S')
            return dt.replace(year=datetime.date.today().year)

        def _messages(self, line):
            return datetime.datetime.strptime(line[:26], '%Y-%m-%dT%H:%M:%S.%f')

        def _chefclient(self, line):
            return datetime.datetime.strptime(line[:20], '[%Y-%m-%dT%H:%M:%S')

        def _apache(self, line):
            return datetime.datetime.strptime(line[5:32], '%b %d %H:%M:%S.%f %Y')

        def _crowbar_production(self, line):
            return datetime.datetime.strptime(line[4:30], '%Y-%m-%dT%H:%M:%S.%f')

        def _crowbar_join(self, line):
            return datetime.datetime.strptime(line[:19], '%Y-%m-%d %H:%M:%S')

        def _get_dateformat(self, line):
            if not line:
                return None

            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            if line[1:4] in days:
                return self._apache
               
            match = re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{2}:[0-9]{2}', line[1:26])
            if match:
                return self._chefclient
     
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            if line[:3] in months:
                return self._chefclient

            match = re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}', line)
            if match:
                return self._nova

            match = re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z', line)
            if match:
                return self._ovs

            match = re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}\+[0-9]{2}:[0-9]{2}', line)
            if match:
                return self._messages

            match = re.match(r'[ID], \[[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}', line)
            if match:
                return self._crowbar_production

            match = re.match(r'[[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} .[0-9]{4}', line)
            if match:
                return self._crowbar_join

            return None



    def __init__(self, file):
        self.file = file
        self.datetime = datetime.datetime.min
        self.line = ''
        self.linenum = 0
        self.dateread = self.DateReader()

    def update(self):
        self.line = ''
        while True:
            tmpline = self.file.readline()
            if not tmpline or tmpline == '\n':
                break

            self.line += tmpline

            tmpdatetime = self.dateread.get(tmpline)
            if tmpdatetime is not None:
                self.datetime = tmpdatetime
                self.linenum += 1
                break
            else:
                print "Found unknown date format in: {}:{}".format(self.file.name, self.linenum)
                break


    def output(self, print_filename=False, print_linenum=False):
        outstr = ''
        if print_filename:
            outstr += self.file.name.rsplit('/', 1)[-1] + " "
            
        if print_linenum and self.line:
            outstr += "{} ".format(self.linenum)

        outstr += self.line.rstrip()
        print outstr

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
        files[0].output(res.print_filename, res.print_linenum)
        if not files[0].has_lines():
            del files[0]


if __name__ == '__main__':
    main()

