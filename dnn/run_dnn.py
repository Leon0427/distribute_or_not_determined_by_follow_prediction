#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/25 16:56
# @Author  : liangxiao
# @Site    : 
# @File    : run_dnn.py
# @Software: PyCharm
from DCNClassifier import DCNClassifier
from ..config.config_loader import load_config
import pandas as pd
import os
from ..log.get_logger import G_LOG as LOG
from ..util.file_manage import FileManager
import os

os.environ["CUDA_VISIBLE_DEVICES"]="1"

if __name__ == '__main__':
    config_dict = load_config("/home/liangxiao/distribute_or_not_determined_by_follow_prediction/config/exp_config.ini")
    train_start_date = config_dict.get("train_config").get("start_date")
    train_end_date = config_dict.get("train_config").get("end_date")
    test_start_date = config_dict.get("test_config").get("start_date")
    test_end_date = config_dict.get("test_config").get("end_date")

    input_dir = config_dict.get("file_path").get("input_dir")
    output_dir = config_dict.get("file_path").get("output_dir")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    train_data_file = os.path.join(output_dir, "train_data_%s_%s"%(train_start_date, train_end_date))
    test_data_file = os.path.join(output_dir, "test_data_%s_%s"%(test_start_date, test_end_date))

    file_name_base = config_dict.get("train_config").get("raw_train_feature_filename_base")

    # FileManager.merge_files(input_dir, file_name_base,train_start_date, train_end_date, train_data_file)
    # FileManager.merge_files(input_dir, file_name_base,test_start_date, test_end_date, test_data_file)


    LOG.info("reading train csv")
    df_trains = pd.read_csv(train_data_file,sep="\t",header=None,chunksize=102400)
    input_size = os.system("head -1 %s | awk -F\"\t\" '{print NF}' " % train_data_file)

    clf_created = False
    clf = None
    for i,df_train in enumerate(df_trains):
        print "in chunk %s:" % i
        if not clf_created:
            clf = DCNClassifier(df_train.shape[1] - 1, epoch=30,batch_size=1024)
        X_train = df_train[range(1,df_train.shape[1])]
        y_train = df_train[0]
        clf.fit(X_train,y_train)
    LOG.info("reading test csv")
    df_test = pd.read_csv(test_data_file,sep="\t", header=None)
    X_test = df_test[range(1, df_test.shape[1])]
    y_test = df_test[0]
    print clf.evaluate(X_test, y_test)