#!/usr/bin/python

import unittest

from logmerge import parse_args


class TestArgparse(unittest.TestCase):

    def test_empty(self):
        parser = parse_args([])
        self.assertTrue(True)
    
