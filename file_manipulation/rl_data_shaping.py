#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/24 11:18
# @Author  : liangxiao
# @Site    : 
# @File    : rl_data_shaping.py
# @Software: PyCharm
from ..config.raw_file_path_config import RawFilePathConfig
from ..config.rl_config import TIME_SLOT_ON_SPAN
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from ..log.get_logger import G_LOG as LOG
from time import time

time_slot_enc = OneHotEncoder(sparse=False)
day_of_week_enc = OneHotEncoder(sparse=False)
slots_number = np.unique(TIME_SLOT_ON_SPAN).size
time_slot_enc.fit(np.array(range(1, slots_number + 1)).reshape(-1,1))
day_of_week_enc.fit(np.array(range(1,8)).reshape(-1,1))

def shape_rl_data(date):
    raw_alignment_follow_file = RawFilePathConfig.RAW_ALIGNMENT_FOLLOW.get_path(date)
    real_time_acc_state = RawFilePathConfig.REAL_TIME_ACC_STATE.get_path(date)
    states_and_rewards_file = RawFilePathConfig.STATES_AND_REWARDS_FILE.get_path(date)

    with open(raw_alignment_follow_file, "r") as fl, open(real_time_acc_state, "r") as s:
        follow_lines = fl.readlines()
        state_lines = s.readlines()
        assert len(follow_lines) == len(state_lines)
        reward_and_states = []
        day_of_weeks = []
        time_slots = []
        for i in range(len(follow_lines)):
            time1 = time()
            state_line = state_lines[i]
            follow_line = follow_lines[i]
            state_arr = state_line.strip().split("\t")
            follow_arr = follow_line.strip().split("\t")
            day_of_week = int(follow_arr[1])
            time_slot = int(follow_arr[2])
            day_of_weeks.append([day_of_week])
            time_slots.append([time_slot])
            self_followed_intime, self_followed, followed = follow_arr[3:]
            limit_dis_follow = []
            for state in state_arr:
                limit_dis_follow.append(float(state.split(":")[1]))
            ldf_feat = np.array(limit_dis_follow)
            reward = int(self_followed)
            # reward = int(self_followed) + int(self_followed_intime) + int(followed)
            reward_and_state = [reward, ldf_feat]
            reward_and_states.append(reward_and_state)
        dw_feats = day_of_week_enc.transform(day_of_weeks)
        ts_feats = time_slot_enc.transform(time_slots)

    with open(states_and_rewards_file, "w") as sr:
        for i in range(len(reward_and_states)):
            reward = str(reward_and_states[i][0])
            dw_feat = dw_feats[i]
            ts_feat =ts_feats[i]
            ldf_feat = reward_and_states[i][1]
            line = reward
            for j in dw_feat:
                line += "\t%s" % j
            for j in ts_feat:
                line += "\t%s" % j
            for j in ldf_feat:
                line += "\t%s" % j
            sr.write(line + "\n")


if __name__ == '__main__':
    import sys
    from ..util.my_dateutil import DateUtil
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    date_ls = DateUtil.get_every_day(start_date, end_date)
    for date in date_ls:
        LOG.info("shaping rl data %s" % date)
        shape_rl_data(date)