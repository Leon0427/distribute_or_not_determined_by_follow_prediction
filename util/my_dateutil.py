# -*- coding:UTF-8 -*-
import datetime


class DateUtil(object):
    def __init__(self):
        super(DateUtil, self).__init__()

    """
    usage: DateUtil.get_relative_delta_time_str("20150525", day=-1)
    output: "20150524"
    """

    @staticmethod
    def get_relative_delta_time_str(date=None, day=None, week=None, date_format="%Y%m%d"):
        if not date:
            date = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")
        define_datetime_datetime = datetime.datetime.strptime(date, date_format)
        if day is not None:
            define_datetime_datetime += datetime.timedelta(days=day)
        if week is not None:
            define_datetime_datetime += datetime.timedelta(weeks=week)
        return define_datetime_datetime.strftime(date_format)

    @staticmethod
    def get_every_day(begin_date, end_date):
        import datetime
        date_list = []
        begin_date = datetime.datetime.strptime(begin_date, "%Y%m%d")
        end_date = datetime.datetime.strptime(end_date, "%Y%m%d")
        if begin_date == end_date:
            date_list.append(begin_date.strftime("%Y%m%d"))
            return date_list
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y%m%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
        return date_list

    @staticmethod
    def get_weekday(date):
        date = datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
        return date.isoweekday()



if __name__ == '__main__':
    print DateUtil.get_relative_delta_time_str("20170622", day=1)
