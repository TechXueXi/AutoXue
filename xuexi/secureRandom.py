#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@project: AutoXue
@file: secureRandom.py
@author: wongsyrone
@Copyright © 2019. All rights reserved.
'''

import secrets

# 从 secrets 模块获取 SystemRandom 实例
_inst = secrets.SystemRandom()

class SecureRandom:
    seed = _inst.seed
    random = _inst.random
    uniform = _inst.uniform
    triangular = _inst.triangular
    randint = _inst.randint
    choice = _inst.choice
    randrange = _inst.randrange
    sample = _inst.sample
    shuffle = _inst.shuffle
    normalvariate = _inst.normalvariate
    lognormvariate = _inst.lognormvariate
    expovariate = _inst.expovariate
    vonmisesvariate = _inst.vonmisesvariate
    gammavariate = _inst.gammavariate
    gauss = _inst.gauss
    betavariate = _inst.betavariate
    paretovariate = _inst.paretovariate
    weibullvariate = _inst.weibullvariate
    getstate = _inst.getstate
    setstate = _inst.setstate
    getrandbits = _inst.getrandbits

def notice():
    raise NotImplementedError('The library does not support execution. Please import to another py file')

if __name__ == '__main__':
    notice()