import os
from global_config import PARENT_DATA_DIR, FILE_SUFFIX


class RawFileNode:
    def __init__(self, path, name):
        self.__path__ = path
        self.__name__ = name

    def get_dir_path(self):
        return os.path.join(PARENT_DATA_DIR, self.__path__)

    def get_path(self, date_str):
        if not self.__name__:
            raise NameError("The specified file not exists")
        return os.path.join(PARENT_DATA_DIR, self.__path__, self.__name__ + FILE_SUFFIX % date_str)


class RawFilePathConfig:
    def __init__(self):
        pass

    __conf_map = {
    }

    __setters = []

    @staticmethod
    def config(name):
        return RawFilePathConfig.__conf_map[name]

    @staticmethod
    def set(name, value):
        if name in RawFilePathConfig.__setters:
            RawFilePathConfig.__conf_map[name] = value
        else:
            raise NameError("Name not accepted in set() method")

    """
        config raw file here
        abbreviation :
            YDAY -> yesterday
            OPP  -> opportunity
            UP   -> update
            HIST -> history
            POTN -> potential
            RESV -> reservation

    """

    RAW_APPLIED_ORDER = RawFileNode("raw_data/applied_order", "applied_order")
    RAW_ALIGNMENT = RawFileNode("raw_data/alignment", "alignment")
    RAW_ALIGNMENT_FOLLOW = RawFileNode("raw_data/alignment_follow", "alignment_follow")
    RAW_XIAONENG_DATA = RawFileNode("raw_data/xiao_neng_data", "xiao_neng_data")
    RAW_MEIQIA_DATA = RawFileNode("raw_data/mei_qia_data", "mei_qia_data")
    RAW_GREAT_BEAR_DATA = RawFileNode("raw_data/great_bear_data", "great_bear_data")
    RAW_HIDDEN_OPP = RawFileNode("raw_data/hidden_opp", "hidden_opp")
    RAW_ACC_BASIC_INFO = RawFileNode("raw_data/acc_basic_info", "acc_basic_info")
    RAW_CMMN_PHONE = RawFileNode("raw_data/community_phone", "community_phone")
    RAW_CALL_RECORD = RawFileNode("raw_data/call_record", "call_record")
    RAW_ACC_CONFIG_DATA = RawFileNode("raw_data/acc_config_data", "acc_config_data")
    RAW_FOLLOW_LOG_DATA = RawFileNode("raw_data/follow_log_data", "follow_log_data")
    RAW_MESSAGE_INFO = RawFileNode("raw_data/message_info", "message_info")
    RAW_HISTORY_OPP_LIMIT = RawFileNode("raw_data/history_opp_limit", "history_opp_limit")

    RAW_MIDDLE = RawFileNode("middle_file", "")
    RAW_MERGE_DATA = RawFileNode("merged_raw_data", "merged_raw_data")

    RAW_FEATURE = RawFileNode("feature_file/raw_feature", "raw_feature")
    MERGED_FEATURE = RawFileNode("feature_file/merged_feature", "merged_feature")
    ACC_BASIC_INFO_FEATURE = RawFileNode("feature_file/acc_basic_info_feature", "acc_basic_info_feature")
    REGIST_FEATURE = RawFileNode("feature_file/community_phone_feature", "community_phone_feature")
    XIAO_NENG_FEATURE = RawFileNode("feature_file/xiao_neng_feature", "xiao_neng_feature")
    MEI_QIA_FEATURE = RawFileNode("feature_file/mei_qia_feature", "mei_qia_feature")
    GREAT_BEAR_FEATURE = RawFileNode("feature_file/great_bear_feature", "great_bear_feature")
    TWICE_CONSULT_FEATURE = RawFileNode("feature_file/twice_consult_feature", "twice_consult_feature")
    PASTNDAY_SITEID_APPLIED_RATIO_FEATURE = RawFileNode("feature_file/pastNday_siteId_applied_ratio_feature", "pastNday_siteId_applied_ratio_feature")
    PASTNDAY_ADVERTISER_APPLIED_RATIO_FEATURE = RawFileNode("feature_file/pastNday_advertiser_applied_ratio_feature", "pastNday_advertiser_applied_ratio_feature")
    PASTNDAY_ACC_APPLIED_RATIO_FEATURE = RawFileNode("feature_file/pastNday_acc_applied_ratio_feature", "pastNday_acc_applied_ratio_feature")
    MESSAGE_INFO_FEATURE = RawFileNode("feature_file/message_info_feature", "message_info_feature")

    ACC_REAL_CALL_FEATURE = RawFileNode("feature_file/acc_real_call_feature", "acc_real_call_feature")
    ACC_REAL_DISTRIBUTION_FEATURE = RawFileNode("feature_file/acc_real_distribution_feature", "acc_real_distribution_feature")
    ACC_REAL_FOLLOWING_FEATURE = RawFileNode("feature_file/acc_real_following_feature", "acc_real_following_feature")

R_CONFIG = RawFilePathConfig()


if __name__ == '__main__':
    r_config = RawFilePathConfig()
    print r_config.RAW_MIDDLE.get_dir_path()
