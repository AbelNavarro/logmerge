#!/usr/bin/python

import unittest
import argparse

from logmerge import parse_args


class TestArgparse(unittest.TestCase):

    def test_empty(self):
        res = parse_args([])
        self.assertEquals(res, argparse.Namespace(print_linenum=False))


    def test_onefile(self):
        args = ['file']
        res = parse_args(args)
        self.assertEquals(res.files, args)


    def test_twofiles(self):
        args = ['file1', 'file2']
        res = parse_args(args)
        self.assertEquals(res.files, args)


    def test_flagnfile(self):
        flags = ['-v']
        files = ['file']
        args = flags + files
        res = parse_args(args)
        self.assertEquals(res.files, files)
        self.assertEquals(res.verbose, 1)


    def test_filenflag(self):
        flags = ['-v']
        files = ['file']
        args = files + flags
        res = parse_args(args)
        self.assertEquals(res.files, files)
        self.assertEquals(res.verbose, 1)


    def test_flagnfiles(self):
        flags = ['-v']
        files = ['file1', 'file2', 'file3', 'file4']
        args = flags + files
        res = parse_args(args)
        self.assertEquals(res.files, files)
        self.assertEquals(res.verbose, 1)


    def test_filesnflag(self):
        flags = ['-v']
        files = ['file']
        args = files + flags
        res = parse_args(args)
        self.assertEquals(res.files, files)
        self.assertEquals(res.verbose, 1)



