#!/usr/bin/python

import unittest

from logmerge import LogFile


class TestDateformat(unittest.TestCase):

    def test_empty(self):
        res = LogFile.get_dateformat('')
        self.assertEquals(res, 'empty')


    def test_ovs(self):
        res = LogFile.get_dateformat('2016-06-02T20:39:51.876Z|')
        self.assertEquals(res, 'ovs')


    def test_neutron(self):
        res = LogFile.get_dateformat('2016-06-02 20:42:23.325 0000')
        self.assertEquals(res, 'nova')


    def test_chefclient(self):
        res = LogFile.get_dateformat('[2016-06-02T19:58:58+00:00] INFO')
        self.assertEquals(res, 'chefclient')


    def test_messages(self):
        res = LogFile.get_dateformat('2016-06-27T06:00:11.386456+00:00 hostname')
        self.assertEquals(res, 'messages')


    def test_novacompute(self):
        res = LogFile.get_dateformat('2016-06-02 20:45:28.166 0000')
        self.assertEquals(res, 'nova')


    def test_pacemaker(self):
        res = LogFile.get_dateformat('Jun 26 06:00:22 [13084]')
        self.assertEquals(res, 'pacemaker')
