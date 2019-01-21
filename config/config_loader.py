# -*- coding: utf-8 -*-
"""
Filename:
Author:
"""
import ConfigParser
from configobj import ConfigObj
import os


def load_config(config_file):
    dict_config = {}
    conf = ConfigParser.ConfigParser()
    conf.read(config_file)
    all_sections = conf.sections()
    for section in all_sections:
        dict_config[section] = {}
        options = conf.options(section)
        for option in options:
            dict_config[section][option] = conf.get(section, option)
    return dict_config


def prepare_aggregation_file(input_dir, time_expr, output_file_name, file_pattern_filter=None):
    file_name_list = os.listdir(input_dir)
    if file_pattern_filter:
        filter_name_list = [i for i in file_name_list if eval(time_expr.format("'{0}'".format(i.split("_")[-1])))
                            and i.startswith(file_pattern_filter)]
    else:
        filter_name_list = [i for i in file_name_list if eval(time_expr.format("'{0}'".format(i.split("_")[-1])))]
    filter_name_list.sort()
    # if not filter_name_list:
    #    raise IOError("can't aggregate to a legal file, please check the path and condition")
    cmd = "cat %s > %s" % (
        " ".join([os.path.join(input_dir, file_name) for file_name in filter_name_list]), output_file_name)
    os.system(cmd)
    print cmd


def prepare_aggr_input(key, dir_section, input_file_pattern, start_date, end_date):
    dir_key = key[:key.rfind("_")] + "_dir"
    input_dir = dir_section[dir_key]
    input_file_name = format_input_file_name(input_file_pattern, start_date, end_date)
    if not os.path.exists(input_file_name):
        prepare_aggregation_file(input_dir, """'%s' <= {0} <= '%s'""" % (start_date, end_date), input_file_name,
                                 key[:key.rfind("_")])


def format_input_file_name(pattern, start_date, end_date):
    if "{$start_date}" in pattern:
        pattern = pattern.replace("{$start_date}", start_date)
    if "{$end_date}" in pattern:
        pattern = pattern.replace("{$end_date}", end_date)
    return pattern


def parse_jar_args(config, section, jar_args):
    re_str = ""
    input_section = config.get("input_file")
    if isinstance(jar_args, type([])):
        for x in jar_args:
            if x in input_section:
                value = input_section[x]
                prepare_aggr_input(x, config.get("input_dir"), value, section.get("start_date", None),
                                   section.get("end_date", None))
                re_str += value + " "
            elif x == "merged_raw_data":
                re_str += config["sample"]["merged_raw_data"] + " "
            else:
                re_str += section[x] + " "
    elif isinstance(jar_args, type("")):
        if jar_args in input_section:
            value = input_section[jar_args]
            prepare_aggr_input(jar_args, config.get("input_dir"), value, section.get("start_date", None),
                               section.get("end_date", None))
            re_str += value + " "
        elif jar_args == "merged_raw_data":
            re_str += config["sample"]["merged_raw_data"] + " "
        else:
            re_str += section[jar_args] + " "
    return re_str


def get_middle_dir(config):
    for key in config["input_file"]:
        value = config["input_file"][key]
        return value[: value.rfind("/") + 1]


def feature_config_loader_executor(config_file):
    config = ConfigObj(config_file)
    # parse input_file key
    for key in config.keys():
        if not key.endswith("_feature"):
            continue
        cmd = "java -cp {} {} {}".format(
            config[key]["jar_file"],
            config[key]["jar_entry"].replace(":", "."),
            parse_jar_args(config, config[key],
                           config[key]["jar_args"]))
        if "{$start_date}" in cmd:
            cmd = cmd.replace("{$start_date}", config[key]["start_date"])
        if "{$end_date}" in cmd:
            cmd = cmd.replace("{$end_date}", config[key]["end_date"])
        print cmd
        os.system(cmd)
    # check
    debug_flag = False
    if debug_flag:
        home_arg = os.environ['HOME']
        if config_file.startswith(home_arg):
            # diff
            for key in config.keys():
                if not key.endswith("_feature") or key == "community_phone_feature":
                    continue
                feature_file = config[key]["feature_file"]
                # /Users/zxf/project_data/sky_opportunity_classify/feature_file/raw_feature/raw_feature_20170919
                target_file = feature_file.replace(home_arg, "/home/online")
                cmd = "diff %s %s" % (feature_file, target_file)
                print cmd
                os.system(cmd)
    # delete middle files
    middle_dir = get_middle_dir(config)
    cmd = "rm %s*" % middle_dir
    print cmd
    os.system(cmd)


if __name__ == '__main__':
    feature_config_loader_executor("/Users/zxf/sky_opportunity_classify/config/feature_config_20170920.ini")
