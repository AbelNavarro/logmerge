#!/usr/bin/python

import unittest

from logmerge import LogFile


class TestDateformat(unittest.TestCase):
    def setUp(self):
        self.datereader = LogFile.DateReader()

    def assertDateReader(self, string, function_name):
        reader = self.datereader._get_dateformat(string)
        self.assertEquals(reader.__name__, function_name)

    def test_empty(self):
        reader = self.datereader._get_dateformat('')
        self.assertIsNone(reader)

    def test_ovs(self):
        self.assertDateReader('2016-06-02T20:39:51.876Z|', '_ovs')


    def test_neutron(self):
        self.assertDateReader('2016-06-02 20:42:23.325 0000', '_nova')


    def test_chefclient(self):
        self.assertDateReader('[2016-06-02T19:58:58+00:00] INFO', '_chefclient')


    def test_messages(self):
        self.assertDateReader('2016-06-27T06:00:11.386456+00:00 hostname', '_messages')


    def test_novacompute(self):
        self.assertDateReader('2016-06-02 20:45:28.166 0000', '_nova')


    def test_pacemaker(self):
        self.assertDateReader('Jun 26 06:00:22 [13084]', '_pacemaker')


    def test_crowbar_production(self):
        self.assertDateReader('I, [2016-07-12T13:45:20.128115 #2515:0x007fccab486f28]', '_crowbar_production')


    def test_crowbar_join(self):
        self.assertDateReader('2016-07-18 08:11:56 -0700', '_crowbar_join')

