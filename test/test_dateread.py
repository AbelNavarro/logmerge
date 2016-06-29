#!/usr/bin/python

import unittest

from logmerge import get_dateread


class TestDateread(unittest.TestCase):

    def test_empty(self):
        res = get_dateread('')
        print res


    def test_ovs(self):
        res = get_dateread('2016-06-02T20:39:51.876Z|')
        print res


    def test_neutron(self):
        res = get_dateread('2016-06-02 20:42:23.325 0000')
        print res


    def test_chefclient(self):
        res = get_dateread('[2016-06-02T19:58:58+00:00] INFO')
        print res


    def test_messages(self):
        res = get_dateread('2016-06-27T06:00:11.386456+00:00 hostname')
        print res


    def test_novacompute(self):
        res = get_dateread('2016-06-02 20:45:28.166 0000')
        print res


    def test_pacemaker(self):
        res = get_dateread('Jun 26 06:00:22 [13084]')
        print res
