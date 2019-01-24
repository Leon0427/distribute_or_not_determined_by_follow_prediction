#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/24 16:02
# @Author  : liangxiao
# @Site    : 
# @File    : run_xgb.py
# @Software: PyCharm

from ..config.config_loader import load_config
import xgboost as xgb
import pandas as pd
import os
from ..log.get_logger import G_LOG as LOG
from ..util.file_manage import FileManager

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

    xgb_config = config_dict.get("train_config").get("xgboost_config")
    xgb_config_dict = load_config(xgb_config)
    xgb_config_dict =  xgb_config_dict.get("param")

    train_data_file = os.path.join(output_dir, "train_data_%s_%s"%(train_start_date, train_end_date))
    test_data_file = os.path.join(output_dir, "test_data_%s_%s"%(test_start_date, test_end_date))

    file_name_base = config_dict.get("train_config").get("raw_train_feature_filename_base")

    FileManager.merge_files(input_dir, file_name_base,train_start_date, train_end_date, train_data_file)
    FileManager.merge_files(input_dir, file_name_base,test_start_date, test_end_date, test_data_file)

    LOG.info("reading train csv")
    df_train = pd.read_csv(train_data_file,sep="\t",header=None)
    LOG.info("reading test csv")
    df_test = pd.read_csv(test_data_file,sep="\t", header=None)

    print df_train.info()
    print df_test.info()

    LOG.info("transform dtrain")
    dtrain = xgb.DMatrix(df_train[range(1,df_train.shape[1])],df_train[0])
    del(df_train)
    LOG.info("transform dest")
    dtest = xgb.DMatrix(df_test[range(1,df_test.shape[1])],df_test[0])
    del(df_test)
    print dtrain.num_row(),dtrain.num_col()
    print dtest.num_row(),dtest.num_col()

    max_depth = xgb_config_dict['max_depth']
    eta = xgb_config_dict['eta']
    silent = xgb_config_dict['silent']
    objective = xgb_config_dict['objective']
    nthread = xgb_config_dict['nthread']
    num_round = int(xgb_config_dict['num_round'])
    eval_metric = xgb_config_dict['eval_metric']
    tree_method = xgb_config_dict['tree_method']

    param = {'max_depth': int(max_depth), 'eta': float(eta), 'silent': int(silent), 'objective': objective, 'tree_method':tree_method}
    param['nthread'] = int(nthread)
    param['eval_metric'] = [eval_metric]
    evallist = [(dtrain, 'eval_train'), (dtest, 'eval_test')]

    bst = xgb.train(param, dtrain, num_round, evallist)

