#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 17:29
# @Author  : liangxiao
# @Site    : 
# @File    : get_real_time_acc_state.py
# @Software: PyCharm
from ..config.raw_file_path_config import RawFilePathConfig
from ..util.my_dateutil import DateUtil

def get_acc_state(date):
    """
    acc date consists of:

    :param date:date String like "20190115"
    :return:
    """
    state_name_list = [
    'recycle_opp_limit_num',
    'recycle_opp_distribution_num',
    'recycle_opp_distribution_saturation',
    'online_opp_limit_num',
    'online_opp_distribution_num',
    'online_opp_distribution_saturation',
    'message_opp_limit_num',
    'message_opp_distribution_num',
    'message_opp_distribution_saturation',
    'opp_following_num',
    'opp_today_following_num',
    ]
    merged_feature = RawFilePathConfig.MERGED_FEATURE.get_path(date)
    real_time_acc_state = RawFilePathConfig.REAL_TIME_ACC_STATE.get_path(date)
    with open(merged_feature, "r") as mf, open(real_time_acc_state,"w") as rs:
        lines = mf.readlines()

        for line in lines:
            states = ""
            for state_name in state_name_list:
                start_idx = line.find(state_name)
                if start_idx!=-1:
                    states += line[start_idx: line.find(" ",start_idx)] + "\t"
                else:
                    states += state_name + ":0\t"
            rs.write(states+"\n")

if __name__ == '__main__':
    import sys
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    date_list = DateUtil.get_every_day(start_date, end_date)
    for date in date_list:
        get_acc_state(date)

