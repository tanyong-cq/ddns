#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
etcd client
'''

import base64
from functools import reduce

import requests


class etcdc(object):
    '''
    class etcd client
    '''

    def __init__(self, url='http://localhost:2379', apiVer='v3beta'):
        self.__url = url
        self.__apiVer = apiVer

    def put(self, key, value):
        '''
        put
        '''
        keyb64 = str(base64.b64encode(key.encode('utf-8')), 'utf-8')
        valueb64 = str(base64.b64encode(value.encode('utf-8')), 'utf-8')
        reqData = '{"key": "%s", "value": "%s"}' % (keyb64, valueb64)
        r = requests.post(self.__url + '/' + self.__apiVer +
                          '/kv/put', data=reqData)
        return r.text

    def get(self, key):
        '''
        get
        '''
        keyb64 = str(base64.b64encode(key.encode('utf-8')), 'utf-8')
        reqData = '{"key": "%s"}' % (keyb64)
        r = requests.post(self.__url + '/' + self.__apiVer +
                          '/kv/range', data=reqData)
        return list(map(lambda x: {**x, 'key': str(base64.b64decode(x.get('key', '')), 'utf-8'), 'value': str(base64.b64decode(x.get('value', '')), 'utf-8')}, eval(r.text).get('kvs', [{}])))

    def dns(self, ip, name):
        '''
        update dns
        '''
        l = name.split('.')
        l.append('/skydns')
        l.reverse()
        key = reduce(lambda x, y: x + '/' + y, l)
        value = '{"host":"%s","ttl":300}' % ip
        self.put(key, value)
