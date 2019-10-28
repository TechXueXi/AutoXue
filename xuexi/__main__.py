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
from . import App
from .unit import logger
logger.debug(f'__MAIN__ running...')
app = App()
app.view_score()
app.quiz()