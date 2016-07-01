#!/usr/bin/python

import unittest
import datetime

from logmerge import LogFile


class TestDateread(unittest.TestCase):

    def test_empty(self):
        res = LogFile.get_dateread('')
        self.assertIsNone(res)

    def test_ovs(self):
        res = LogFile.get_dateread('2016-06-02T20:39:51.876Z|')
        self.assertEquals(res, datetime.datetime(2016, 06, 02, 20, 39, 51, 876000))

    def test_neutron(self):
        res = LogFile.get_dateread('2016-06-02 20:42:23.325 0000')
        self.assertEquals(res, datetime.datetime(2016, 06, 02, 20, 42, 23, 325000))

    def test_chefclient(self):
        res = LogFile.get_dateread('[2016-06-02T19:58:58+00:00] INFO')
        self.assertEquals(res, datetime.datetime(2016, 06, 02, 19, 58, 58, 000000))

    def test_messages(self):
        res = LogFile.get_dateread('2016-06-27T06:00:11.386456+00:00 hostname')
        self.assertEquals(res, datetime.datetime(2016, 06, 27, 06, 00, 11, 386456))

    def test_novacompute(self):
        res = LogFile.get_dateread('2016-06-02 20:45:28.166 0000')
        self.assertEquals(res, datetime.datetime(2016, 06, 02, 20, 45, 28, 166000))

    def test_pacemaker(self):
        res = LogFile.get_dateread('Jun 26 06:00:22 [13084]')
        self.assertEquals(res, datetime.datetime(2016, 06, 26, 06, 00, 22, 000000))
