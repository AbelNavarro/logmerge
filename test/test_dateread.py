#!/usr/bin/python

import unittest
import datetime

from logmerge import LogFile


class TestDateread(unittest.TestCase):

    def setUp(self):
        self.datereader = LogFile.DateReader()

    def assertDateRead(self, string, *date):
        reader = self.datereader._get_dateformat(string)
        res = reader(string)
        self.assertEquals(res, datetime.datetime(*date))

    def test_ovs(self):
        self.assertDateRead('2016-06-02T20:39:51.876Z|',
                            2016, 06, 02, 20, 39, 51, 876000)

    def test_neutron(self):
        self.assertDateRead('2016-06-02 20:42:23.325 0000',
                            2016, 06, 02, 20, 42, 23, 325000)

    def test_chefclient(self):
        self.assertDateRead('[2016-06-02T19:58:58+00:00] INFO',
                            2016, 06, 02, 19, 58, 58, 000000)

    def test_messages(self):
        self.assertDateRead('2016-06-27T06:00:11.386456+00:00 hostname',
                            2016, 06, 27, 06, 00, 11, 386456)

    def test_novacompute(self):
        self.assertDateRead('2016-06-02 20:45:28.166 0000',
                            2016, 06, 02, 20, 45, 28, 166000)

    def test_pacemaker(self):
        self.assertDateRead('Jun 26 06:00:22 [13084]',
                            2016, 06, 26, 06, 00, 22, 000000)

    def test_apache(self):
        self.assertDateRead('[Wed Jun 22 15:12:20.427073 2016] [wsgi:error]',
                            2016, 06, 22, 15, 12, 20, 427073)

    def test_crowbar_production(self):
        self.assertDateRead('I, [2016-07-12T13:45:20.130379 #2515:0x007fccab486f28]',
                            2016, 07, 12, 13, 45, 20, 130379)

    def test_crowbar_join(self):
        self.assertDateRead('2016-07-18 08:11:56 -0700',
                            2016, 07, 18, 8, 11, 56, 000000)

    def test_bash_history(self):
        self.assertDateRead('#1478876044',
                            2016, 11, 11, 14, 54, 04, 000000)

