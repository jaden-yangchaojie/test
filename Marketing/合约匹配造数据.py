import json
#####模板####
# {"merchant_name": "autotest", "match_type": "EXACT_MATCH"},
# {"merchant_name": "autotest1", "match_type": "EXACT_MATCH", "task_id": "1234"},
# {"merchant_name": "autotest2", "match_type": "EXACT_MATCH", "task_id": "1234"},
# {"merchant_name": "autotest12", "match_type": "EXACT_MATCH", "task_id": "1234", "benefit_batch_no": "43123"}
# {"merchant_name": "%autotest%", "match_type": "FUZZY_MATCH", "contract_id": "20260629052810080010"},
# {"merchant_name":"autotest","match_type":"EXACT_MATCH","contract_id":"20260629052810080004"},
# {"merchant_name": "autotest1", "match_type": "EXACT_MATCH","contract_id":"20260629052810080005"},
# {"merchant_name": "autotest2", "match_type": "EXACT_MATCH","contract_id":"20260629052810080006","task_id":"MK20260629200004_BENEFIT_TASK"},
# {"merchant_name": "autotest12", "match_type": "EXACT_MATCH", "contract_id": "20260629052810080007","benefit_batch_no":"26062900100100333300000000000004"},
# {"merchant_name": "autotest_black", "match_type": "EXACT_BLACKLIST", "contract_id": "20260629052810080009"},
# {"merchant_name":"%autotest%","match_type":"FUZZY_MATCH","contract_id":"20260629052810080010"},
# {"merchant_name": "%autotest%", "match_type": "FUZZY_MATCH","contract_id":"20260629052810080011","task_id":"MK20260629200007_BENEFIT_TASK"},
# {"merchant_name": "%autotest%", "match_type": "FUZZY_MATCH", "contract_id": "20260629052810080012","benefit_batch_no":"26062900100100333300000000000008"},
# {"merchant_name": "%autotest%", "match_type": "FUZZY_MATCH", "contract_id": "20260629052810080013"},
# {"merchant_name": "%autotest1%", "match_type": "FUZZY_MATCH", "contract_id": "20260629052810080014"},
# {"merchant_name": "%1autotest%", "match_type": "FUZZY_MATCH", "contract_id": "20260629052810080015"},
# {"merchant_name": "%kkkk%", "match_type": "FUZZY_MATCH", "contract_id": "20260629052810080016"},
# {"merchant_name": "%autotest_black%", "match_type": "FUZZY_BLACKLIST", "contract_id": "20260629052810080017"},
activity_no = "MK20260616000001"
merchant_name_dict_to_match_type_dict_list=[
    {"merchant_name": "%simi%", "match_type": "FUZZY_MATCH", "contract_id": "20260629052810080055"},
    # {"merchant_name": "%autotest1%", "match_type": "FUZZY_BLACKLIST", "contract_id": "20260629052810080054"}


]


# contract_id_init="202606290528100800"

# benefit_batch_no = "26062200100100333300000000000001"


for i,get_one in enumerate(merchant_name_dict_to_match_type_dict_list):
    # contract_id=contract_id_init + f"{i:02d}"

    merchant_name=get_one["merchant_name"]
    match_type=get_one["match_type"]
    task_id = 'null'
    benefit_batch_no = 'null'
    if "task_id" in get_one.keys():
        task_id="'"+get_one["task_id"]+"'"
    if "benefit_batch_no" in get_one.keys():
        benefit_batch_no="'"+get_one["benefit_batch_no"]+"'"
    if "contract_id" in get_one.keys():
        contract_id = "'" + get_one["contract_id"] + "'"

    mc_mk_merchant_contract = (
                "INSERT INTO corebankingA1.`mc_mk_merchant_contract` (`tenant_id`,`entity_id`,`create_time_local`,`create_time_utc`,`update_time_local`,`update_time_utc`,`contract_id`,`contract_status`,`mcc_code`,`merchant_name`,`merchant_id`,`activity_no`,`active_start_time_local`,`active_end_time_local`,`extension_info`,`match_type`,`task_id`,`benefit_batch_no`) VALUES " +
                "('STMXFINCORE0','MXCC20220000','2026-06-24 03:00:42','2026-06-24 09:00:42','2026-06-24 03:00:42','2026-06-24 09:00:42',"+contract_id+ ",'active','','"+merchant_name+"','','"+activity_no+"','2022-06-24 00:00:00','2036-06-24 23:59:59',null,'"+match_type+"',"+task_id+","+benefit_batch_no+");")

    print(mc_mk_merchant_contract + "\n")




