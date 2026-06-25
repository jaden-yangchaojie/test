import json

# usageCount 必填
activity_no = "MK20260622000001"

# benefit_batch_no = "26062200100100333300000000000001"

merchant_name_dict_to_match_type_dict_list=[
    {"merchant_name":"autotest1","match_type":"EXACT_MATCH"},
    {"merchant_name":"autotest2","match_type":"EXACT_MATCH"}]
task_id='null'
benefit_batch_no='null'
match_type='EXACT_MATCH'
for i,get_one in enumerate(merchant_name_dict_to_match_type_dict_list):
    contract_id="202606250528100800" + f"{i:02d}"
    merchant_name=get_one["merchant_name"]
    match_type=get_one["match_type"]
    mc_mk_merchant_contract = (
                "INSERT INTO corebankingA1.`mc_mk_merchant_contract` (`tenant_id`,`entity_id`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`contract_id`,`contract_status`,`mcc_code`,`merchant_name`,`merchant_id`,`activity_no`,`active_start_time_local`,`active_end_time_local`,`extension_info`,`match_type`,`task_id`,`benefit_batch_no`) VALUES " +
                "('STMXFINCORE0','MXCC20220000','2026-06-24 03:00:42','2026-06-24 09:00:42','2026-06-24 03:00:42','2026-06-24 09:00:42','"+contract_id+ "','active','','"+merchant_name+"','','"+activity_no+"','2022-06-24 00:00:00','2036-06-24 23:59:59',null,'"+match_type+"',"+task_id+","+benefit_batch_no+");")

    print(mc_mk_merchant_contract + "\n")




