import json

# usageCount 必填
benefit_batch_no = "26040900100100333300000000000001"
benefit_name = '自动化测试勿动-返现权益化-打标-添加资格'
start_time = "2024-11-18 00:00:00"
end_time = "2024-11-18 23:59:59"
usage_rules = json.dumps({"txnFilterParam": {
    "cardTypes": [],"effectiveEndTime": "","effectiveStartTime": "","mccCodes": [],
    "postEndTime": "","postStartTime": "","productType": "credit","subTypes": [],"terminalTypes": []},
    "effectiveTimeLimit": {"type": "interval","effectiveStartTime": start_time,"effectiveEndTime": end_time}, "usageCount": 10000})
# usage_rules = json.dumps({"effectiveTimeLimit":{"type":"sinceReceive","rangeDays":1},
#                           "txnFilterParam":{"mccCodes":[],"terminalTypes":["APP"],"subTypes":["TOP_UP","BILL"],"cardTypes":[],"productCodes":["STC002"],
#                                             "minAmt":"10000","maxAmt":"","ccy":"MXN","productType":"credit","postStartTime":start_time,"postEndTime":end_time,"effectiveStartTime":start_time,"effectiveEndTime":end_time},"usageAmountLimit":"1000","usageCount":100})
activity_no = "MK20260409000001"

#  "usageAmountLimit": 45000
crowd_no = "26040912345678910111200000000001"
crowd_rules = json.dumps(
    {"productCode": "STC002", "openDate": "2024-11-18T15:00:00", "openEndDate": "2024-11-18T15:59:59"})

#不改动##########
task_name = activity_no + "_BENEFIT_TASK"
start_time_activity = start_time
end_time_activity = str(end_time).replace("-08-", "-10-")
#百分比#########
# preferential_rules = json.dumps({"singleAmountLimit": 10000, "calculateMethod": "percent", "calculateParam": "0.07", "rewardChannel": "CASHBACK"})
preferential_rules = json.dumps({ "calculateMethod": "percent", "calculateParam": "0.05", "rewardChannel": "CASHBACK"})
mk_common_param2_mcc_code = json.dumps([{"activityNo": activity_no, "cashbackAmountCalParams": "0.05",
                                         "cashbackType": "percent", "categoryName": "all", "mccCode": "all",
                                         "terminalType": ""}])
activity_rules = json.dumps({"cashbackAmountCalMethod": "percent", "cashbackAmountCalParams": "0.05", "cashbackLimit": {},
                  "cashbackMatchRuleType": "rules_engine"})
#
# task_complete_config=json.dumps({"productType": "debit", "types": [ "PAY_IN", "TRANSFER", "CASH_IN", "INCENTIVE" ],
#                                  "direction": "IN", "postStartTime": "taskEffectiveTime", "postEndTime": "taskExpireTime", "minAmt": "1"})
# task_complete_config=json.dumps({"productType":"credit", "minAmt":"1","maxAmt":"500000","types":["PURCHASE"],"effectiveStartTime":"2024-11-17 00:00:00","effectiveEndTime":"2024-11-17 23:59:59","postStatuses":["POSTING","POSTED"]})

task_complete_config=json.dumps({})

#返回固定金额
# preferential_rules = json.dumps({ "calculateMethod": "fixAmount", "calculateParam": "100", "rewardChannel": "CASHBACK"})
# mk_common_param2_mcc_code = json.dumps([{"activityNo": activity_no, "cashbackAmountCalParams": "100",
#                                          "cashbackType": "fixAmount", "categoryName": "all", "mccCode": "all",
#                                          "terminalType": ""}])
# activity_rules = json.dumps({"cashbackAmountCalMethod": "fixAmount", "cashbackAmountCalParams": "100", "cashbackLimit": {},
#                   "cashbackMatchRuleType": "rules_engine"})



##############活动权益#################
mk_bf_instance = (
            "INSERT INTO configA1.`mk_bf_instance` (`tenant_id`,`entity_id`,`template_no`,`benefit_batch_no`,`benefit_name`,`benefit_type`,`status`,`product_code`,`biz_type`,`creator_id`,`creator_name`,`benefit_desc`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`biz_scenario`) VALUES " +
            "('STMXFINCORE0','MXCC20220000','000000','" + benefit_batch_no + "','" + benefit_name + "','CASHBACK','ACTIVE','STC002','CREDIT','tester','tester','自动化测试勿动-偏回归','2025-08-01 03:43:47','2025-08-01 09:43:47','2025-08-01 03:43:47','2025-08-01 09:43:47',null);")


print(mk_bf_instance + "\n")

mk_bf_instance_rules = ((
                            '''INSERT INTO configA1.`mk_bf_instance_rules` (`tenant_id`,`entity_id`,`benefit_batch_no`,`receive_start_time`,`receive_end_time`,`preferential_rules`,`usage_rules`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`) VALUES ''') +
                        (
                                    "('STMXFINCORE0','MXCC20220000','" + benefit_batch_no + "','" + start_time + "','" + end_time + "','" +
                                    preferential_rules + "','" + usage_rules + "','2024-11-01 03:43:47','2024-11-30 09:43:47','2025-08-01 03:43:47','2025-08-01 09:43:47');"))

print(mk_bf_instance_rules + "\n")

mk_bf_instance_stock = (
            "INSERT INTO configA1.`mk_bf_instance_stock` (`tenant_id`,`entity_id`,`benefit_batch_no`,`total_quantity`,`received_quantity`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`remaining_quantity`) VALUES "
            + "('STMXFINCORE0','MXCC20220000','" + benefit_batch_no + "','30000','0','2025-08-01 03:43:47','2025-08-01 09:43:47','2025-08-01 03:43:47','2025-08-01 09:43:47','30000');")

print(mk_bf_instance_stock + "\n")

##############活动配置#################
mk_activity = (
            "INSERT INTO configA1.`mk_activity` (`tenant_id`,`entity_id`,`activity_no`,`activity_type`,`activity_desc`,`activity_name`,`activity_status`,`notification_config`,`activity_rules`,`benefit_batch_no`,`crowd_no`,`creator_id`,`creator_name`,`activity_start_time`,`activity_end_time`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`user_rules`,`product_code`,`biz_type`,`biz_source`,`mutual_exclusion_rules`,`biz_scene`,`audience_id`,`registration_start_time`,`registration_end_time`) VALUES " +
            "('STMXFINCORE0','MXCC20220000','" + activity_no + "','CASHBACK','"+benefit_name+"','benefit 返现权益化-自动化测试','ACTIVE',null,'"+activity_rules+"','','" + crowd_no + "','system','system','" + start_time_activity + "','" + end_time_activity + "','2025-08-19 22:01:50','2025-08-20 04:01:50','2025-08-19 22:01:50','2025-08-20 04:01:50',null,'STC002','CREDIT',null,null,null,'" + activity_no + "_audience',null,null);")

print(mk_activity + "\n")

mk_crowd = (
            "INSERT INTO configA1.`mk_crowd` (`tenant_id`,`entity_id`,`crowd_no`,`quantity`,`crowd_desc`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`type`,`crowd_rules`) VALUES " +
            "('STMXFINCORE0','MXCC20220000','" + crowd_no + "','0','" + benefit_name + "','2025-11-12 06:53:11','2025-11-12 12:53:11','2025-11-12 06:53:11','2025-11-12 12:53:11','DYNAMIC','" + crowd_rules + "');")
print(mk_crowd + "\n")

# mk_common_param = (
#             "INSERT INTO configA1.`mk_common_param` (`tenant_id`,`entity_id`,`activity_no`,`param_name`,`param_key`,`param_value`,`param_desc`,`effect_time_start_local`,`effect_time_end_local`,`priority`,`version`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`is_deleted`,`param_config_type`) VALUES" +
#             "('STMXFINCORE0','MXCC20220000','" + activity_no + "','TRANS_FILTER_RULE','TRANS_FILTER_RULE','" + '''{"cardTypes":[],"mccCodes":[],"productType":"credit","spelExpression":"","subTypes":[],"terminalTypes":[]}',null,null,null,'1','1','2025-11-13 22:57:18','2025-11-14 04:57:18','2025-11-13 23:02:10','2025-11-14 05:02:10','0','TRANS_FILTER_RULE');''')
#
# print(mk_common_param + "\n")

mk_common_param2 = (
            "INSERT INTO configA1.`mk_common_param` (`tenant_id`,`entity_id`,`activity_no`,`param_name`,`param_key`,`param_value`,`param_desc`,`effect_time_start_local`,`effect_time_end_local`,`priority`,`version`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`is_deleted`,`param_config_type`) VALUES" +
            "('STMXFINCORE0','MXCC20220000','" + activity_no + "','cashback_category_mapping','cashback_category_mapping','" + mk_common_param2_mcc_code + "',null,null,null,'1','1','2025-11-13 22:57:18','2025-11-14 04:57:18','2025-11-13 23:02:10','2025-11-14 05:02:10','0','MCC_ACTIVITY_RULE');")
print(mk_common_param2 + "\n")

##############活动任务#################
mk_activity_task = (
            "INSERT INTO configA1.`mk_activity_task` (`tenant_id`,`entity_id`,`task_id`,`task_name`,`task_desc`,`task_type`,`budget_list`,`complete_config`,`activity_no`,`activity_type`,`benefit_package`,`crowd_rule`,`start_time`,`end_time`,`task_limit`,`task_params`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`) VALUES " +
            "('STMXFINCORE0','MXCC20220000','" + task_name + "','" + benefit_name + "','benefit Autotest','TRANSACTION','','"+task_complete_config +"','" + activity_no + "','CASHBACK','" + benefit_batch_no + "',null,'" + start_time + "','" + end_time + "','','"+'{"autoConfig":{"autoRunning":true,"autoComplete":true,"autoReward":true}}'+"','2025-08-18 20:40:57','2025-08-19 02:40:57','2025-08-18 20:40:57','2025-08-19 02:40:57');")
print(mk_activity_task + "\n")


#
#
# mk_exclusion_group=("INSERT INTO `mk_exclusion_group` (`tenant_id`,`entity_id`,`group_id`,`member_type`,`member_id`,`priority`,`group_desc`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`) VALUES "+
#                     "('STMXFINCORE0','MXCC20220000','1111','BENEFIT','TE9','4','"+benefit_name+"','2025-09-10 21:45:07','2025-09-10 21:45:07','2025-09-10 21:45:07','2025-09-10 21:45:07');")
#
# print(mk_exclusion_group + "\n")