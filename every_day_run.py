#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 10:47
# @Author  : liangxiao
# @Site    : 
# @File    : every_day_run.py.py
# @Software: PyCharm
a = [1,2,3,4,5,6,7,8,9,0]
def yielder(a):
    l = len(a)
    for i in range(l):
        if i % 2:
            if i+1<l:
                yield a[i: i+2]
            else:
                yield a[i: i+1]

for i in yielder(a):
    print i