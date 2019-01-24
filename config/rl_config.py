#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 16:11
# @Author  : liangxiao
# @Site    : 
# @File    : rl_config.py
# @Software: PyCharm
import numpy as np
def time_slot_on_span(time_span_on_min = 5):
    slots_per_hour = 60 / time_span_on_min
    time_slot = np.zeros([24,60],dtype=int)
    hours = range(24)
    mins = range(60)
    slot = 0
    for hour in hours:
        for min in mins:
            if min % time_span_on_min == 0:
                slot += 1
            time_slot[hour][min] = slot
    return time_slot
TIME_SLOT_ON_SPAN = time_slot_on_span(5)