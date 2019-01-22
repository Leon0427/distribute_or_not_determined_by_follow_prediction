#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/21 11:17
# @Author  : liangxiao
# @Site    : 
# @File    : sql_mapper.py
# @Software: PyCharm

GET_ALIGNMENT = """
SELECT
     DISTINCT drag_opportunity_distribution_log.`id`,
     drag_opportunity_distribution_log.`opp_id`,
     drag_opportunity_distribution_log.`account`,
     drag_opportunity_distribution_log.`sub_distribution_type`,
     drag_opportunity_distribution_log.`operator_time`,
     drag_opportunity_distribution_log.`quantum_id`,
     if(drag_opportunity_follow_log.`consultant_account` is not null, 1, 0) as followed
 FROM
     drag_opportunity
 LEFT JOIN
     drag_quantum_config
 ON
     drag_opportunity.`quantum_id` = drag_quantum_config.`quantum_id`
 LEFT JOIN
     drag_opportunity_distribution_log
 ON
     drag_opportunity_distribution_log.`opp_id` = drag_opportunity.`id`
 LEFT OUTER JOIN
     drag_opportunity_follow_log
 ON
     drag_opportunity_follow_log.`opportunity_id` = drag_opportunity.`id`
 and 
     drag_opportunity_follow_log.`consultant_account` = drag_opportunity_distribution_log.`account`
 WHERE
     drag_opportunity_distribution_log.`distribution_type` = 'AUTO_DISTRIBUTION'
 AND
 (
     drag_opportunity_distribution_log.`sub_distribution_type`= 'SUB_AUTO_ONLINE_DISTRIBUTION'
 OR
     drag_opportunity_distribution_log.`sub_distribution_type`= 'SUB_AUTO_PREDICT_DISTRIBUTION'
 OR
     drag_opportunity_distribution_log.`sub_distribution_type`= 'SUB_AUTO_PREDICT_RECYCLE_DISTRIBUTION'
 OR 
     drag_opportunity_distribution_log.`sub_distribution_type`= 'SUB_AUTO_PREDICT_ONLINE_DISTRIBUTION'
 OR 
     drag_opportunity_distribution_log.`sub_distribution_type`= 'SUB_AUTO_PREDICT_MESSAGE_DISTRIBUTION'
 OR
     drag_opportunity_distribution_log.`sub_distribution_type`= 'SUB_AUTO_MESSAGE_DISTRIBUTION'
 OR
     drag_opportunity_distribution_log.`sub_distribution_type`= 'SUB_AUTO_RECYCLE_DISTRIBUTION'
 OR
     drag_opportunity_distribution_log.`sub_distribution_type`= 'SUB_AUTO_INDIVIDUATION_DISTRIBUTION'
 )
 AND
     drag_quantum_config.`config_value` IN ('MOBILE', 'WECHAT', 'MOBILE_WECHAT')
 AND
     drag_opportunity_distribution_log.`operator_time` >= "20190102"
 AND
     drag_opportunity_distribution_log.`operator_time` < "20190103"
"""

GET_ALIGNMENT_FOLLOW_STATUS = """
SELECT
opportunity_id, consultant_account, state_time
FROM
drag_opportunity_follow_log
WHERE
opportunity_id in ({0})
"""