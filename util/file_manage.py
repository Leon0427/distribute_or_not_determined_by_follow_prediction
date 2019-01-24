#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/24 16:44
# @Author  : liangxiao
# @Site    : 
# @File    : file_manage.py
# @Software: PyCharm
import os
from ..log.get_logger import G_LOG as LOG

class FileManager(object):

    def __init__(self):
        pass

    @staticmethod
    def merge_files(input_dir, file_name_base, start_date, end_date, output_file):
        start_file_name = file_name_base % start_date
        end_file_name = file_name_base % end_date
        file_list = os.listdir(input_dir)
        file_list.sort()
        if len(file_list) <= 0:
            raise Exception("not existing file to merge")
        filter_list = [os.path.join(input_dir, file_name) for file_name in file_list if
                       start_file_name <= file_name <= end_file_name]
        cmd = 'cat %s > %s' % (" ".join(filter_list), output_file)
        LOG.info("Execute cmd :\n" + cmd)
        os.system(cmd)