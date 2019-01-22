#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 10:22
# @Author  : liangxiao
# @Site    : 
# @File    : get_follow_status_according_to_alignment_file.py
# @Software: PyCharm
from ..config.global_config import PARENT_DATA_DIR
from ..config.raw_file_path_config import RawFilePathConfig
from ..sql_query.fetch_db_data_2_file_process import db_fetch_db_process
from ..sql_query.sql_mapper import GET_ALIGNMENT_FOLLOW_STATUS
from ..config.global_config import NEW_SKYNET_MYSQL_CONFIG_FILE
from ..log.get_logger import G_LOG as LOG
import sys
from datetime import date as dt
from ..util.my_dateutil import DateUtil
print RawFilePathConfig.RAW_ALIGNMENT.get_dir_path()
print RawFilePathConfig.RAW_ALIGNMENT.get_path(dt.strftime(dt.today(),"%Y%m%d"))
def get_one_day_dist_info_of_alignment(date):
    if "-" in date:
        date.replace("-","")
    alignment_file = RawFilePathConfig.RAW_ALIGNMENT.get_path(date)
    opp_dist_info = []
    with open(alignment_file, "r") as fin:
        lines = fin.readlines()
        for line in lines:
            arr = line.split("\t")
            opp_id = arr[1]
            account = arr[2]
            operator_time = arr[8]
            opp_dist_info.append((opp_id, account,operator_time))
    return opp_dist_info

def opp_info_yielder(opp_dist_info, info_span=500):
    l = len(opp_dist_info)
    for i in range(l):
        if i % info_span == 0:
            if i + info_span - 1 < l:
                yield opp_dist_info[i: i + info_span]
            else:
                yield opp_dist_info[i: i + info_span - 1]

def get_opp_follow_status(opp_dist_info):
    opp_follow_status = []
    for opp_info_piece in opp_info_yielder(opp_dist_info):
        sql = GET_ALIGNMENT_FOLLOW_STATUS.format(",".join(["\"%s\""%x[0] for x in opp_info_piece]))
        opp_follower_times = db_fetch_db_process(sql,config_file=NEW_SKYNET_MYSQL_CONFIG_FILE)
        dic = dict([(str(x[0]),(x[1],str(x[2]))) for x in opp_follower_times])
        for opp_info in opp_info_piece:
            opp_id = opp_info[0]
            dist_account = opp_info[1]
            dist_time = opp_info[2]
            followed, self_followed, self_followed_intime = 0,0,0
            if not dic.has_key(opp_id):
                # first_self_follow, self_follow, follow
                opp_follow_status.append((opp_id, self_followed_intime,self_followed,followed))
                continue
            follow_account = dic.get(opp_id)[0]
            follow_time = dic.get(opp_id)[1]
            followed = 1
            if follow_account == dist_account:
                self_followed = 1
                follow_date = follow_time[:10]
                dist_date = dist_time[:10]
                if follow_date == dist_date:
                    self_followed_intime = 1
            opp_follow_status.append((opp_id, self_followed_intime, self_followed, followed))
    return opp_follow_status




def get_follow_file(date):
    LOG.info("generating %s follow file..." % date)
    opp_dist_info = get_one_day_dist_info_of_alignment(date)
    opp_follow_status = get_opp_follow_status(opp_dist_info)
    raw_alignment_follow_file = RawFilePathConfig.RAW_ALIGNMENT_FOLLOW.get_path(date)
    with open(raw_alignment_follow_file, "w") as fout:
        for i in opp_follow_status:
            line = "%s\t%s\t%s\t%s\n"%i
            fout.write(line)

if __name__ == '__main__':
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    date_ls = DateUtil.get_every_day(start_date, end_date)
    for date in date_ls:
        get_follow_file(date)