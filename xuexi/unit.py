#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@project: AutoXue
@file: unit.py
@author: kessil
@contact: https://github.com/kessil/AutoXue/
@time: 2019-10-25(星期五) 21:44
@Copyright © 2019. All rights reserved.
'''
import time
import logging
from pathlib import Path
from configparser import ConfigParser

class Timer:
    ''' 简易计时器
        使用形如：
            with Timer() as t:
                pass...
            print(t.elapsed)
    '''
    def __init__(self, func=time.perf_counter):
        self.elapsed = 0.0
        self._func = func
        self._start = None
    
    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()

    def stop(self):
        if self._start is None:
            raise RuntimeError('Not started')
        end = self._func()
        self.elapsed += end - self._start
        self._start = None

    def reset(self):
        self.elapsed = 0.0

    @property
    def running(self):
        return self._start is not None
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, *args):
        self.stop()


cfg = ConfigParser()
cfg.read('./xuexi/default.ini', encoding='utf-8')
cfg.read('./xuexi/custom.ini', encoding='utf-8')


def create_logger(loggername:str='logger', levelname:str='DEBUG', console_levelname='INFO'):
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    logger = logging.getLogger(loggername)
    logger.setLevel(levels[levelname])

    logger_format = logging.Formatter("[%(asctime)s][%(levelname)s][%(filename)s][%(funcName)s][%(lineno)03s]: %(message)s")
    console_format = logging.Formatter("[%(levelname)s] %(message)s")

    handler_console = logging.StreamHandler()
    handler_console.setFormatter(console_format)
    handler_console.setLevel(levels[console_levelname])

    path = Path(__file__).parent/'logs' # 日志目录
    path.mkdir(parents=True, exist_ok=True)
    today = time.strftime("%Y-%m-%d")     # 日志文件名
    common_filename = path / f'{today}.log'
    handler_common = logging.FileHandler(common_filename , mode='a+', encoding='utf-8')
    handler_common.setLevel(levels[levelname])
    handler_common.setFormatter(logger_format)

    logger.addHandler(handler_console)
    logger.addHandler(handler_common)

    return logger


configs = dict(cfg._sections)
caps = dict(configs['capability'])
for key, value in caps.items():
    if "true" == value.lower():
        caps[key] = True
    elif 'false' == value.lower():
        caps[key] = False
    else:
        pass

# prefers = dict(configs['prefers'])
# for key, value in prefers.items():
#     if "true" == value.lower():
#         prefers[key] = True
#     elif 'false' == value.lower():
#         prefers[key] = False
#     else:
#         pass

rules = dict(configs['rules'])
logger = create_logger('xuexi', console_levelname=cfg.get("prefers", "console_levelname"))


if __name__ == "__main__":
    for k,v in caps.items():
        print(k,v)