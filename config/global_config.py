# -*- coding:UTF-8 -*-
"""
Filename:
Function:
Author:
Create:
"""


import os
import getpass
user = getpass.getuser()
PARENT_DIR = "/home/%s/project_data/" % user
PROJECT_NAME = "personalized_alignment_classify"
PARENT_DATA_DIR = os.path.join(PARENT_DIR, PROJECT_NAME)
PROJECT_DIR = os.path.join("/home/%s" % user, PROJECT_NAME)
MYSQL_CONFIG_FILE = os.path.join(PARENT_DATA_DIR, "config_files/mysql_config.ini")
NEW_SKYNET_MYSQL_CONFIG_FILE = os.path.join(PARENT_DATA_DIR, "config_files/new_skynet_mysql_config.ini")
SMS_CONFIG_FILE = os.path.join(PARENT_DATA_DIR, "config_files/send_message.cfg")
FILE_SUFFIX = "_%s"
ACC_BASIC_INFO_URL = "http://ehr.sunlands.com/ehr-web/staffAchive/getSalerBaseInfo.do"
COMMUNITY_MYSQL_CONFIG_FILE = os.path.join(PARENT_DATA_DIR, "config_files/community_mysql_config.ini")