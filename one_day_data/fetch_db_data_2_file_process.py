# -*- coding: utf-8 -*-
import codecs
import re
from .base_dao import BaseDAO
from ..log.get_logger import G_LOG as LOG
from ..config import global_config

MYSQL_CONFIG_FILE = global_config.MYSQL_CONFIG_FILE

CONTROL_CHARS = ''.join(map(unichr, range(2, 7) + range(11, 12+1) + range(17, 31+1)))
CONTROL_CHAR_RE = re.compile('[%s]' % re.escape(CONTROL_CHARS))


def remove_control_chars(s):
    return CONTROL_CHAR_RE.sub('', s)


def db_fetch_db_process(sql, config_file=MYSQL_CONFIG_FILE):
    dao = BaseDAO(config_file)
    dao.connect()
    LOG.info("Start to fetch data from database, sql:\n" + sql)
    # logging.info("Start to fetch data from database, sql:\n" + sql)
    # get_logger().debug("Start to fetch data from database, sql:\n" + sql)
    dao.cursor.execute(sql)
    data = dao.cursor.fetchall()
    dao.close()
    return data


def dump_2_file(data, output):
    with codecs.open(output, "w", "utf-8") as fout:
        for i in data:
           # fout.write("\t".join([remove_control_chars(unicode(j)).replace("\r\t", "\001").replace("\n\t", "\001").replace("\r", "\001").replace("\n", "\001").replace("\t", "\001") for j in i]) + "\n")
           # fout.write("\t".join([unicode(j).replace("\r\t", "\001").replace("\n\t", "\001").replace("\r", "\001").replace("\n", "\001").replace("\t", "\001").replace(unichr(28), "").replace(unichr(29), "") for j in i]) + "\n")
           # row_msg = "\t".join([unicode(j).replace("\r\t", "\001").replace("\n\t", "\001").replace("\r", "\001").replace("\n", "\001").replace("\t", "\001").replace(unichr(28), "").replace(unichr(29), "").replace(unichr(12), "") for j in i])
            row_msg = "\t".join([unicode(j).replace("\r\t", "\001").replace("\n\t", "\001").replace("\r", "\001").replace("\n", "\001").replace("\t", "\001") for j in i])
            row_msg = remove_control_chars(row_msg)
            fout.write(row_msg + "\n")


def dump_2_file_sky_opp(data, output):
    with codecs.open(output, "w", "utf-8") as fout:
        for i in data:
            if len(i) != 18:
                continue
            arr = [unicode(j).strip().replace("\t", "") for j in i if len(i) == 18]
            fout.write("\t".join(arr) + "\n")
