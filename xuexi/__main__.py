#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@project: AutoXue
@file: __main__.py
@author: kessil
@contact: https://github.com/kessil/AutoXue/
@time: 2019-10-26(星期六) 10:22
@Copyright © 2019. All rights reserved.
'''
import random
import time
from . import App
from .unit import logger


app = App()

def shuffle(funcs):
    random.shuffle(funcs)
    for func in funcs:
        func()
        time.sleep(5)

if random.random() > 0.5:
    logger.debug(f'视听学习优先')
    app.watch()
    app.music()
    shuffle([app.read, app.daily, app.challenge])
else:
    logger.debug(f'视听学习置后')
    app.music()
    shuffle([app.read, app.daily, app.challenge])
    app.watch()

logger.info(f'大功告成，功成身退')