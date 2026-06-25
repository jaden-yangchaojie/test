import json

# usageCount 必填

task_desc='自动化测试勿动-推荐人&被推荐人'
start_time = "2024-09-20 00:00:00"
end_time = "2024-10-25 23:59:59"

activity_no = "MK20260413000001"
#不改动##########
task_id=activity_no + "_TRAIL_FUND_TASK"
task_name ="自动化测试-勿动"
start_time_activity = start_time
end_time_activity =end_time


##############活动配置#################
mk_activity = (
            "INSERT INTO configB1.`mk_activity` (`tenant_id`,`entity_id`,`activity_no`,`activity_type`,`activity_desc`,`activity_name`,`activity_status`,`notification_config`,`activity_rules`,`benefit_batch_no`,`crowd_no`,`creator_id`,`creator_name`,`activity_start_time`,`activity_end_time`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`user_rules`,`product_code`,`biz_type`,`biz_source`,`mutual_exclusion_rules`,`biz_scene`,`audience_id`,`registration_start_time`,`registration_end_time`) VALUES " +
            "('SVMXFINCORE0','MXDC20220000','" + activity_no + "','TRIAL_FUND','体验金迭代优化-自动化测试勿动并发','体验金迭代优化-自动化测试勿动','ACTIVE',null,'{}','','" + "" + "','system','system','" + start_time_activity + "','" + end_time_activity + "','2025-08-19 22:01:50','2025-08-20 04:01:50','2025-08-19 22:01:50','2025-08-20 04:01:50',null,'SVD001','DEBIT','DEPOSIT',null,'BALANCE',null,null,null);")
print(mk_activity + "\n")



##############活动任务#################
mk_activity_task = (
            "INSERT INTO corebankingB1.`mk_activity_task` (`tenant_id`,`entity_id`,`task_id`,`task_name`,`task_desc`,`task_type`,`budget_list`,`complete_config`,`activity_no`,`activity_type`,`benefit_package`,`crowd_rule`,`start_time`,`end_time`,`task_limit`,`task_params`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`) VALUES " +
            "('SVMXFINCORE0','MXDC20220000','" + task_id + "','" + task_name + "','trail fund Autotest-自动化测试勿动','CLICK','','{}','" + activity_no + "','TRIAL_FUND','" + "" + "',null,'" + start_time + "','" + end_time + "','','"+'{"amount":100000,"ccy":"MXN","days":3}'+"','2025-08-18 20:40:57','2025-08-19 02:40:57','2025-08-18 20:40:57','2025-08-19 02:40:57');")
print(mk_activity_task + "\n")

mk_buget=("INSERT INTO configB1.mk_budget (tenant_id, entity_id, budget_id, budget_name, budget_type,total_amt, allocated_amt, used_amt, ccy, overlimit_rate, fund_source,budget_status, budget_owner, start_time, end_time,create_time_local, create_time_utc, update_time_local, update_time_utc) VALUES "
          "('SVMXFINCORE0', 'MXDC20220000', 'TRIAL_BUDGET_1215','体验金总预算任务专项自动化测试勿动', 'main',100000, 3013, 763, 'MXN', 1, 'default','ACTIVE', 'jaden', '2025-06-11 00:00:00', '2025-11-20 23:59:59','2025-08-06 04:05:56', '2025-08-06 10:05:56', '2026-01-20 03:09:44', '2026-01-20 09:09:44');")
print(mk_buget + "\n")



