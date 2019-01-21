# -*- coding:UTF-8 -*-
"""
Filename:
Function:
Author:
Create:
"""

import MySQLdb
from ..config import global_config

MYSQL_CONFIG_FILE = global_config.MYSQL_CONFIG_FILE
NEW_SKYNET_MYSQL_CONFIG_FILE = global_config.NEW_SKYNET_MYSQL_CONFIG_FILE


class BaseDAO(object):
    def __init__(self, config_file=MYSQL_CONFIG_FILE):
        self.config_file = config_file

    def connect(self):
        from ..config.config_loader import load_config
        dict_config = load_config(self.config_file)
        self.host = dict_config["database"]["host"]
        self.user = dict_config["database"]["user"]
        self.passwd = dict_config["database"]["passwd"]
        self.db = dict_config["database"]["db"]
        if "crmback" in dict_config["database"]:
            self.crmback = dict_config["database"]["crmback"]  # 天网crmback库

        conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, charset="utf8")
        self.conn = conn
        cursor = conn.cursor()
        self.cursor = cursor

    def close(self):
        self.cursor.close()
        self.conn.close()
