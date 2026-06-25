import json
for one in range(0,24):
    if len(str(one))==1:
        print("\"0"+str(one)+"\",")
    else:
        print( "\""+str(one)+"\",")
# usageCount 必填
get_range_param_list=["00",
"01",
"02",
"03",
"04",
"05",
"06",
"07",
"08",
"09",
"10",
"11",
"12",
"13",
"14",
"15",
"16",
"17",
"18",
"19",
"20",
"21",
"22",
"23"]

for get_range in get_range_param_list:
    benefit_batch_no = "260201001001003333000000000000"+get_range
    benefit_name = '自动化测试勿动-任务中心-专项测试'
    start_time = "2024-12-01 00:00:00"
    end_time = "2025-01-15 23:59:59"

    crowd_no = "260201123456789101112000000000"+get_range
    crowd_rules = json.dumps({"productCode": "STC002", "openDate": "2024-12-02T"+get_range+":00:00", "openEndDate": "2024-12-02T"+get_range+":59:59"})

    activity_no = "MK202602010000"+get_range
    #不改动##########
    task_name = activity_no + "TEST_TASK"
    start_time_activity = start_time
    end_time_activity =end_time

    ##############活动配置#################
    mk_activity = (
                "INSERT INTO configA1.`mk_activity` (`tenant_id`,`entity_id`,`activity_no`,`activity_type`,`activity_desc`,`activity_name`,`activity_status`,`notification_config`,`activity_rules`,`benefit_batch_no`,`crowd_no`,`creator_id`,`creator_name`,`activity_start_time`,`activity_end_time`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`user_rules`,`product_code`,`biz_type`,`biz_source`,`mutual_exclusion_rules`,`biz_scene`,`audience_id`,`registration_start_time`,`registration_end_time`) VALUES " +
                "('STMXFINCORE0','MXCC20220000','" + activity_no + "','CASHBACK','BENEFIT autotest-任务中心--自动化测试勿动','task 任务中心-自动化测试','ACTIVE',null,'"+'{}'+"','','','system','system','" + start_time_activity + "','" + end_time_activity + "','2025-08-19 22:01:50','2025-08-20 04:01:50','2025-08-19 22:01:50','2025-08-20 04:01:50',null,'STC002','CREDIT',null,null,null,'',null,null);")

    print(mk_activity + "\n")

    mk_crowd = (
                "INSERT INTO configA1.`mk_crowd` (`tenant_id`,`entity_id`,`crowd_no`,`quantity`,`crowd_desc`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`type`,`crowd_rules`) VALUES " +
                "('STMXFINCORE0','MXCC20220000','" + crowd_no + "','0','" + benefit_name + "','2025-11-12 06:53:11','2025-11-12 12:53:11','2025-11-12 06:53:11','2025-11-12 12:53:11','DYNAMIC','" + crowd_rules + "');")
    print(mk_crowd + "\n")

    ##############活动任务#################
    mk_activity_task = (
                "INSERT INTO configA1.`mk_activity_task` (`tenant_id`,`entity_id`,`task_id`,`task_name`,`task_desc`,`task_type`,`budget_list`,`complete_config`,`activity_no`,`activity_type`,`benefit_package`,`crowd_rule`,`start_time`,`end_time`,`task_limit`,`task_params`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`) VALUES " +
                "('STMXFINCORE0','MXCC20220000','" + task_name + "','" + benefit_name + "','任务中心-专项测试 Autotest','DEFAULT','','{}','" + activity_no + "','CASHBACK','" + benefit_batch_no + "',null,'" + start_time + "','" + end_time + "','','','2025-08-18 20:40:57','2025-08-19 02:40:57','2025-08-18 20:40:57','2025-08-19 02:40:57');")
    print(mk_activity_task + "\n")







