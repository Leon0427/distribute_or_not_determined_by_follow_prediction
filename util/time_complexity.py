#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/25 15:10
# @Author  : liangxiao
# @Site    : 
# @File    : time_complexity.py
# @Software: PyCharm
import functools
import time
def time_func(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        time1 = time.time()
        func(*args, **kw)
        print "used %s seconds..." % (time.time() - time1)
    return wrapper

@time_func
def printtt():
    i = 3
    while(i>0):
        time.sleep(1)
        i -= 1

if __name__ == '__main__':
    printtt()
