import json
true=True
# usageCount 必填
# get_range_param_list=["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20"]
get_range_param_list={"27":"28","29":"30","31":"32","33":"34"}
#

for get_referrer,get_referred in  get_range_param_list.items():
    get_referrer=str(get_referrer)
    benefit_batch_no = "260413001001003333000000000000"+str(get_referrer)
    benefit_name = '自动化测试勿动-referral-推荐人&被推荐人'
    start_time = "2024-09-20 00:00:00"
    end_time = "2024-10-25 23:59:59"
    usage_rules = json.dumps({"autoConfig":{"autoUsage":true,"dqCheck":true},"txnFilterParam": {
        "cardTypes": [],"effectiveEndTime": "","effectiveStartTime": "","mccCodes": [],
        "postEndTime": "","postStartTime": "","productType": "credit","subTypes": [],"terminalTypes": []},
        "effectiveTimeLimit": {"type": "interval","effectiveStartTime": start_time,"effectiveEndTime": end_time}, "usageCount": 100,"usageAmountLimit": 10000})

    crowd_no = "260413123456789101112000000000"+get_referrer
    crowd_rules = json.dumps(
        {"productCode": "STC002", "openDate": "2025-04-21T"+get_referrer+":00:00", "openEndDate": "2025-04-21T"+get_referrer+":59:59"})
    activity_no_referrer = "MK202604130000"+get_referrer
    #不改动##########
    task_name = activity_no_referrer + "_BENEFIT_TASK"
    start_time_activity = start_time
    end_time_activity =end_time
    #百分比#########
    # preferential_rules = json.dumps({"singleAmountLimit": 10000, "calculateMethod": "percent", "calculateParam": "0.07", "rewardChannel": "CASHBACK"})
    # preferential_rules = json.dumps({"singleAmountLimit": 10000,  "calculateMethod": "percent", "calculateParam": "0.05", "rewardChannel": "CASHBACK"})
    # mk_common_param2_mcc_code = json.dumps([{"activityNo": activity_no, "cashbackAmountCalParams": "0.05",
    #                                          "cashbackType": "percent", "categoryName": "all", "mccCode": "all",
    #                                          "terminalType": ""}])
    # # activity_rules = json.dumps({"cashbackAmountCalMethod": "percent", "cashbackAmountCalParams": "0.05", "cashbackLimit": {},
    # #                   "cashbackMatchRuleType": "rules_engine"})
    #返回固定金额
    preferential_rules = json.dumps({ "calculateMethod": "fixAmount", "calculateParam": "100", "rewardChannel": "ADJUSTMENT"})
    # mk_common_param2_mcc_code = json.dumps([{"activityNo": activity_no_referrer, "cashbackAmountCalParams": "100",
    #                                          "cashbackType": "fixAmount", "categoryName": "all", "mccCode": "all",
    #                                          "terminalType": ""}])
    #权益化已不用这个字段
    activity_rules =''
    # activity_rules = json.dumps({"cashbackAmountCalMethod": "fixAmount", "cashbackAmountCalParams": "100", "cashbackLimit": {},
    #                   "cashbackMatchRuleType": "rules_engine"})



    ##############活动权益#################
    mk_bf_instance = (
                "INSERT INTO configA1.`mk_bf_instance` (`tenant_id`,`entity_id`,`template_no`,`benefit_batch_no`,`benefit_name`,`benefit_type`,`status`,`product_code`,`biz_type`,`creator_id`,`creator_name`,`benefit_desc`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`biz_scenario`) VALUES " +
                "('STMXFINCORE0','MXCC20220000','000000','" + benefit_batch_no + "','" + benefit_name + "','REWARD','ACTIVE','STC002','CREDIT','tester','tester','自动化测试勿动-referral-推荐人&被推荐人','2025-08-01 03:43:47','2025-08-01 09:43:47','2025-08-01 03:43:47','2025-08-01 09:43:47',null);")


    print(mk_bf_instance + "\n")

    mk_bf_instance_rules = ((
                                '''INSERT INTO configA1.`mk_bf_instance_rules` (`tenant_id`,`entity_id`,`benefit_batch_no`,`receive_start_time`,`receive_end_time`,`preferential_rules`,`usage_rules`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`) VALUES ''') +
                            (
                                        "('STMXFINCORE0','MXCC20220000','" + benefit_batch_no + "','" + start_time + "','" + end_time + "','" +
                                        preferential_rules + "','" + usage_rules + "','2025-08-01 03:43:47','2025-08-01 09:43:47','2025-08-01 03:43:47','2025-08-01 09:43:47');"))

    print(mk_bf_instance_rules + "\n")

    mk_bf_instance_stock = (
                "INSERT INTO configA1.`mk_bf_instance_stock` (`tenant_id`,`entity_id`,`benefit_batch_no`,`total_quantity`,`received_quantity`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`remaining_quantity`) VALUES "
                + "('STMXFINCORE0','MXCC20220000','" + benefit_batch_no + "','30000','0','2025-08-01 03:43:47','2025-08-01 09:43:47','2025-08-01 03:43:47','2025-08-01 09:43:47','30000');")

    print(mk_bf_instance_stock + "\n")

    ##############活动配置#################
    mk_activity = (
                "INSERT INTO configA1.`mk_activity` (`tenant_id`,`entity_id`,`activity_no`,`activity_type`,`activity_desc`,`activity_name`,`activity_status`,`notification_config`,`activity_rules`,`benefit_batch_no`,`crowd_no`,`creator_id`,`creator_name`,`activity_start_time`,`activity_end_time`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`user_rules`,`product_code`,`biz_type`,`biz_source`,`mutual_exclusion_rules`,`biz_scene`,`audience_id`,`registration_start_time`,`registration_end_time`) VALUES " +
                "('STMXFINCORE0','MXCC20220000','" + activity_no_referrer + "','REFERRAL','"+benefit_name+"','"+benefit_name+"','ACTIVE',null,'"+activity_rules+"','','','system','system','" + start_time_activity + "','" + end_time_activity + "','2025-08-19 22:01:50','2025-08-20 04:01:50','2025-08-19 22:01:50','2025-08-20 04:01:50',null,'STC002','CREDIT',null,null,null,'" + activity_no_referrer + "_audience',null,null);")

    print(mk_activity + "\n")

    # mk_crowd = (
    #             "INSERT INTO configA1.`mk_crowd` (`tenant_id`,`entity_id`,`crowd_no`,`quantity`,`crowd_desc`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`type`,`crowd_rules`) VALUES " +
    #             "('STMXFINCORE0','MXCC20220000','" + crowd_no + "','0','" + benefit_name + "','2025-11-12 06:53:11','2025-11-12 12:53:11','2025-11-12 06:53:11','2025-11-12 12:53:11','DYNAMIC','" + crowd_rules + "');")
    # print(mk_crowd + "\n")

    # mk_common_param = (
    #             "INSERT INTO configA1.`mk_common_param` (`tenant_id`,`entity_id`,`activity_no`,`param_name`,`param_key`,`param_value`,`param_desc`,`effect_time_start_local`,`effect_time_end_local`,`priority`,`version`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`is_deleted`,`param_config_type`) VALUES" +
    #             "('STMXFINCORE0','MXCC20220000','" + activity_no + "','TRANS_FILTER_RULE','TRANS_FILTER_RULE','" + '''{"cardTypes":[],"mccCodes":[],"productType":"credit","spelExpression":"","subTypes":[],"terminalTypes":[]}',null,null,null,'1','1','2025-11-13 22:57:18','2025-11-14 04:57:18','2025-11-13 23:02:10','2025-11-14 05:02:10','0','TRANS_FILTER_RULE');''')
    #
    # print(mk_common_param + "\n")

    # mk_common_param2 = (
    #             "INSERT INTO configA1.`mk_common_param` (`tenant_id`,`entity_id`,`activity_no`,`param_name`,`param_key`,`param_value`,`param_desc`,`effect_time_start_local`,`effect_time_end_local`,`priority`,`version`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`is_deleted`,`param_config_type`) VALUES" +
    #             "('STMXFINCORE0','MXCC20220000','" + activity_no + "','cashback_category_mapping','cashback_category_mapping','" + mk_common_param2_mcc_code + "',null,null,null,'1','1','2025-11-13 22:57:18','2025-11-14 04:57:18','2025-11-13 23:02:10','2025-11-14 05:02:10','0','MCC_ACTIVITY_RULE');")
    # print(mk_common_param2 + "\n")

    ##############活动任务#################
    mk_activity_task = (
                "INSERT INTO configA1.`mk_activity_task` (`tenant_id`,`entity_id`,`task_id`,`task_name`,`task_desc`,`task_type`,`budget_list`,`complete_config`,`activity_no`,`activity_type`,`benefit_package`,`crowd_rule`,`start_time`,`end_time`,`task_limit`,`task_params`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`) VALUES " +
                "('STMXFINCORE0','MXCC20220000','" + task_name + "','" + benefit_name + "','benefit Autotest','REFERRAL','','{}','" + activity_no_referrer + "','REFERRAL','" + benefit_batch_no + "',null,'" + start_time + "','" + end_time + "','','','2025-08-18 20:40:57','2025-08-19 02:40:57','2025-08-18 20:40:57','2025-08-19 02:40:57');")
    print(mk_activity_task + "\n")




#     被推荐人
    get_referred=str(get_referred)
    benefit_batch_no = "260413001001003333000000000000"+str(get_referred)
    benefit_name = '自动化测试勿动-referral-推荐人&被推荐人'
    start_time = "2024-09-20 00:00:00"
    end_time = "2024-10-25 23:59:59"
    usage_rules = json.dumps({"txnFilterParam": {
        "cardTypes": [],"effectiveEndTime": "","effectiveStartTime": "","mccCodes": [],
        "postEndTime": "","postStartTime": "","productType": "credit","subTypes": [],"terminalTypes": []},
        "effectiveTimeLimit": {"type": "interval","effectiveStartTime": start_time,"effectiveEndTime": end_time}, "usageCount": 100,"usageAmountLimit": 10000})

    crowd_no = "260413123456789101112000000000"+get_referred
    crowd_rules = json.dumps(
        {"productCode": "STC002", "openDate": "2025-04-21T"+get_referred+":00:00", "openEndDate": "2025-04-21T"+get_referred+":59:59"})
    activity_no_referred = "MK202604130000"+get_referred
    #不改动##########
    task_name = activity_no_referred + "_BENEFIT_TASK"
    start_time_activity = start_time
    end_time_activity =end_time

    #返回固定金额
    preferential_rules = json.dumps({ "calculateMethod": "fixAmount", "calculateParam": "100", "rewardChannel": "ADJUSTMENT"})

    #权益化已不用这个字段
    activity_rules =''
    # activity_rules = json.dumps({"cashbackAmountCalMethod": "fixAmount", "cashbackAmountCalParams": "100", "cashbackLimit": {},
    #                   "cashbackMatchRuleType": "rules_engine"})



    ##############活动权益#################
    mk_bf_instance = (
                "INSERT INTO configA1.`mk_bf_instance` (`tenant_id`,`entity_id`,`template_no`,`benefit_batch_no`,`benefit_name`,`benefit_type`,`status`,`product_code`,`biz_type`,`creator_id`,`creator_name`,`benefit_desc`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`biz_scenario`) VALUES " +
                "('STMXFINCORE0','MXCC20220000','000000','" + benefit_batch_no + "','" + benefit_name + "','CASHBACK','ACTIVE','STC002','CREDIT','tester','tester','自动化测试勿动-referral-推荐人&被推荐人','2025-08-01 03:43:47','2025-08-01 09:43:47','2025-08-01 03:43:47','2025-08-01 09:43:47',null);")


    print(mk_bf_instance + "\n")

    mk_bf_instance_rules = ((
                                '''INSERT INTO configA1.`mk_bf_instance_rules` (`tenant_id`,`entity_id`,`benefit_batch_no`,`receive_start_time`,`receive_end_time`,`preferential_rules`,`usage_rules`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`) VALUES ''') +
                            (
                                        "('STMXFINCORE0','MXCC20220000','" + benefit_batch_no + "','" + start_time + "','" + end_time + "','" +
                                        preferential_rules + "','" + usage_rules + "','2025-08-01 03:43:47','2025-08-01 09:43:47','2025-08-01 03:43:47','2025-08-01 09:43:47');"))

    print(mk_bf_instance_rules + "\n")

    mk_bf_instance_stock = (
                "INSERT INTO configA1.`mk_bf_instance_stock` (`tenant_id`,`entity_id`,`benefit_batch_no`,`total_quantity`,`received_quantity`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`remaining_quantity`) VALUES "
                + "('STMXFINCORE0','MXCC20220000','" + benefit_batch_no + "','30000','0','2025-08-01 03:43:47','2025-08-01 09:43:47','2025-08-01 03:43:47','2025-08-01 09:43:47','30000');")

    print(mk_bf_instance_stock + "\n")

    ##############活动配置#################
    mk_activity = (
                "INSERT INTO configA1.`mk_activity` (`tenant_id`,`entity_id`,`activity_no`,`activity_type`,`activity_desc`,`activity_name`,`activity_status`,`notification_config`,`activity_rules`,`benefit_batch_no`,`crowd_no`,`creator_id`,`creator_name`,`activity_start_time`,`activity_end_time`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`user_rules`,`product_code`,`biz_type`,`biz_source`,`mutual_exclusion_rules`,`biz_scene`,`audience_id`,`registration_start_time`,`registration_end_time`) VALUES " +
                "('STMXFINCORE0','MXCC20220000','" + activity_no_referred + "','CASHBACK','"+benefit_name+"','"+benefit_name+"','ACTIVE',null,'"+activity_rules+"','','','system','system','" + start_time_activity + "','" + end_time_activity + "','2025-08-19 22:01:50','2025-08-20 04:01:50','2025-08-19 22:01:50','2025-08-20 04:01:50',null,'STC002','CREDIT',null,null,null,'" + activity_no_referred + "_audience',null,null);")

    print(mk_activity + "\n")



    ##############活动任务#################
    mk_activity_task = (
                "INSERT INTO configA1.`mk_activity_task` (`tenant_id`,`entity_id`,`task_id`,`task_name`,`task_desc`,`task_type`,`budget_list`,`complete_config`,`activity_no`,`activity_type`,`benefit_package`,`crowd_rule`,`start_time`,`end_time`,`task_limit`,`task_params`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`) VALUES " +
                "('STMXFINCORE0','MXCC20220000','" + task_name + "','" + benefit_name + "','benefit Autotest','DEFAULT','','{}','" + activity_no_referred + "','CASHBACK','" + benefit_batch_no + "',null,'" + start_time + "','" + end_time + "','','','2025-08-18 20:40:57','2025-08-19 02:40:57','2025-08-18 20:40:57','2025-08-19 02:40:57');")
    print(mk_activity_task + "\n")








