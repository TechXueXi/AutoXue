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
from argparse import ArgumentParser
import time
from . import App
from .unit import logger
from .secureRandom import SecureRandom as random

parse = ArgumentParser(description="Accept username and password if necessary!")

parse.add_argument("-u", "--username", metavar="username", type=str, default='', help='User Name')
parse.add_argument("-p", "--password", metavar="password", type=str, default='', help='Pass Word')
args = parse.parse_args()
app = App(args.username, args.password)

def shuffle(funcs):
    random.shuffle(funcs)
    for func in funcs:
        func()
        time.sleep(5)

def start():
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
    app.logout_or_not()
    
    logger.info(f'大功告成，功成身退')

def test():
    app.daily()
    logger.info(f'测试完毕')

if __name__ == "__main__":
    start()
    # test()