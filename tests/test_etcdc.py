#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
etcd client test
'''
import unittest
from etcdc import etcdc

class Test(unittest.TestCase):
    def setUp(self):
        self.ec = etcdc.etcdc('http://10.181.138.195:2379')

    def test(self):
        ec = self.ec
        print(ec.put('/skydns/com/test/test', '192.168.1.1'))
        print(ec.dns('192.168.1.2', 'test1.test.com'))
        print(ec.get('/skydns/com/test/test'))
        print(ec.get('/skydns/com/test/test1'))

if __name__ == '__main__':
    unittest.main()
