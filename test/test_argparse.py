#!/usr/bin/python

import unittest
import argparse

from logmerge import parse_args


class TestArgparse(unittest.TestCase):

    def test_empty(self):
        opts = parse_args([])
        self.assertEquals(opts, argparse.Namespace(print_linenum=False))


    def test_onefile(self):
        args = ['file']
        opts = parse_args(args)
        self.assertEquals(opts.files, args)


    def test_twofiles(self):
        args = ['file1', 'file2']
        opts = parse_args(args)
        self.assertEquals(opts.files, args)


    def test_flagnfile(self):
        flags = ['-v']
        files = ['file']
        args = flags + files
        opts = parse_args(args)
        self.assertEquals(opts.files, files)
        self.assertEquals(opts.verbose, 1)


    def test_filenflag(self):
        flags = ['-v']
        files = ['file']
        args = files + flags
        opts = parse_args(args)
        self.assertEquals(opts.files, files)
        self.assertEquals(opts.verbose, 1)


    def test_flagnfiles(self):
        flags = ['-v']
        files = ['file1', 'file2', 'file3', 'file4']
        args = flags + files
        opts = parse_args(args)
        self.assertEquals(opts.files, files)
        self.assertEquals(opts.verbose, 1)


    def test_filesnflag(self):
        flags = ['-v']
        files = ['file']
        args = files + flags
        opts = parse_args(args)
        self.assertEquals(opts.files, files)
        self.assertEquals(opts.verbose, 1)

