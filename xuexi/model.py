#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@project: AutoXue
@file: model.py
@author: kessil
@contact: https://github.com/kessil/AutoXue/
@time: 2019-10-27(星期天) 10:43
@Copyright © 2019. All rights reserved.
'''
import json
import requests
from .unit import cfg, logger

class Structure:
    _fields = []

    def __init__(self, *args, **kwargs):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # Set all of the positional arguments
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # Set the remaining keyword arguments
        for name in self._fields[len(args):]:
            setattr(self, name, kwargs.pop(name))

        # Check for any remaining unknown arguments
        if kwargs:
            raise TypeError('Invalid argument(s): {}'.format(','.join(kwargs)))

class Bank(Structure):
    _fields = ['id', 'category', 'content', 'options', 'answer', 'excludes', 'description']

    def __repr__(self):
        return f'{self.content}'

    def to_json(self):
        pass

    @classmethod
    def from_json(self, data):
        pass

class BankQuery:
    def __init__(self):
        self.url = cfg.get('api', 'url')

    def post(self, item):
        headers= {
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        res = requests.post(url=self.url, headers=headers, json=item)
        if 201 == res.status_code:
            return True
        return False

    def get(self, item):
        logger.debug(f'Query {item["content"]}...')
        headers= {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        res = requests.get(url=self.url, headers=headers, params=item)
        if 200 == res.status_code:
            return json.loads(res.text)
        return None
