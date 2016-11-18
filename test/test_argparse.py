#!/usr/bin/python

import argparse
import sys
import unittest

from logmerge import parse_args


class TestArgparse(unittest.TestCase):
    def checkBuffered(self):
        if not hasattr(sys.stderr, "getvalue"):
            self.fail("need to run in buffered mode")


    def assertInsufficientArgs(self, args):
        self.checkBuffered()
        with self.assertRaises(SystemExit) as exc_context:
            opts = parse_args(args)
        exc = exc_context.exception
        self.assertEquals(exc.code, 2)
        output = sys.stderr.getvalue().strip() # because stderr is an StringIO instance
        self.assertRegexpMatches(output, "Need at least two files to merge")


    def test_empty(self):
        self.assertInsufficientArgs([])


    def test_onefile(self):
        self.assertInsufficientArgs(['file'])


    def test_twofiles(self):
        args = ['file1', 'file2']
        opts = parse_args(args)
        self.assertEquals(opts.files, args)


    def test_flagnfile(self):
        flags = ['-v']
        files = ['file']
        args = flags + files
        self.assertInsufficientArgs(args)


    def test_filenflag(self):
        flags = ['-v']
        files = ['file']
        args = files + flags
        self.assertInsufficientArgs(args)


    def test_flagnfiles(self):
        flags = ['-v']
        files = ['file1', 'file2', 'file3', 'file4']
        args = flags + files
        opts = parse_args(args)
        self.assertEquals(opts.files, files)
        self.assertEquals(opts.verbose, 1)


    def test_filesnflag(self):
        flags = ['-v']
        files = ['file1', 'file2', 'file3', 'file4']
        args = files + flags
        opts = parse_args(args)
        self.assertEquals(opts.files, files)
        self.assertEquals(opts.verbose, 1)

