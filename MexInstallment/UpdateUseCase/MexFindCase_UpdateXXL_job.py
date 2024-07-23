import json

from ColInstallment import ColScenarioHandler
from MexInstallment import MetersphereUtils
#批量修改任务id和其他参数用例

def get_batch_id():
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50)
    return get_batch_ids

isTrue= False
def find_process(id):
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)

    get_list = []
    # only_find(result, get_list)
    find_handler2_interface(result, get_list)

    data["data"]["scenarioDefinition"] = result

    get_post_data = data["data"]
    global isTrue
    if isTrue==True:
        get_update_info = MetersphereUtils.update(get_post_data)
        isTrue=False

    # print(get_update_info)
    # for get_one in get_list:
    #     print(get_one)

def only_find(get_data, dds):
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
        get_path = get_data["path"]

        if get_path == "/xxl-job-admin/jobinfo/trigger":
            get_list = get_data["body"]["kvs"]
            print(get_list[0]["value"])

    if get_data["type"] == "scenario" and get_data["enable"] == True and (get_data["referenced"]=="COPY" or get_data["referenced"]=="Created"):
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            only_find(subScenario, dds)
def find_handler2_interface(get_data, dds):
    global cur_time_line
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
        get_path = get_data["path"]
        # if get_path == "/transactions/authorizations" or get_path == "/transactions/adjustments/credit":
        #     print()
        #     get_script = get_data["hashTree"][0]["script"]
        #     old_words = "hByKl5U+zzpMibm7MiEnjEsnBHC4ntATnEhjzKRw2fw="
        #     new_words = "${api-secret}"
        #     if str(get_script).count(old_words) > 0:
        #         get_replace = str(get_script).replace(old_words, new_words)
        #         get_data["hashTree"][0]["script"] = get_replace
        if get_path == "/xxl-job-admin/jobinfo/trigger":
            get_list = get_data["body"]["kvs"]

            if get_list[0]["value"] == '${xxl_task_id_posted}':
                print()
            kkk=[{"1011":"${xxl_task_id_posted}"}   ##1725
                # # ,{"1013":"${xxl_task_id_posted_process}"}  ##1727
                # # ,{"1015":"${xxl_task_id_check_overdue_opening_split}"} ##1729
                # #  ,{"1033":"${xxl_task_id_check_overdue_overdue_split}"} ##1745
                # # , {"1017": "${xxl_task_id_check_overdue_process}"} ##1731
                # #  , {"1920": "${xxl_task_id_dispute_process}"}  ##1916
                # # , {"1919": "${xxl_task_id_dispute_split}"}     ##1915
                # # , {"1023": "${xxl_task_id_dq_cancel_split}"}  ##1737
                # # , {"1025": "${xxl_task_id_dq_cancel_process}"}  ##1739
                # # , {"1021": "${xxl_task_id_refund_cancel_process}"} ##1735
                # # , {"1019": "${xxl_task_id_refund_cancel_split}"} ##1733
                # # , {"963": "${xxl_task_id_dq_status_update_split}"} ##1711
                # # , {"961": "${xxl_task_id_dq_status_update_process}"} ##1709
                # # , {"913": "${xxl_task_id_dq_notice_statement_split}"} ##1577
                # # , {"911": "${xxl_task_id_dq_notice_statement_process}"}  ##1575
                # # , {"909": "${xxl_task_id_payment_process}"} ##1573
                # #  ,{"671":"${xxl_task_id_payment_job_task_process}"} ##1495
                # #错误修正
                # , {"1725": "${xxl_task_id_posted}"}

                ]
            for kk in kkk:
                for k,v in kk.items():
                    if get_list[0]["value"] == v:
                        print()
                        # get_list[0]["value"]=v
                        # get_script = get_data["hashTree"][0]["script"]
                        # get_replace = str(get_script).replace(k, v)
                        # get_data["hashTree"][0]["script"] = get_replace
                        # get_script = get_data["hashTree"][1]["script"]
                        if str(get_list[1]["value"]).count("7") > 0:
                            # get_replace = str(get_list[1]["value"]).replace("MXCC20220000", "${entityId}")
                            # get_replace = str(get_replace).replace("STMXFINCORE0", "${tenantId}")
                            get_replace = str(get_list[1]["value"]).replace("7", "0")
                            get_replace = str(get_replace).replace("19", "0")
                            print("+++++++")
                            global isTrue
                            isTrue=True
                            # get_data["hashTree"][1]["script"] = get_replace
                            get_list[1]["value"]=get_replace
            # elif get_list[0]["value"] == "1013":
            #     get_script = get_data["hashTree"][0]["script"]
            #     get_replace = str(get_script).replace("1013", "${xxl_task_id_posted_process}")
            #     get_data["hashTree"][0]["script"] = get_replace
            #     get_script = get_data["hashTree"][1]["script"]
            #     if str(get_script).count("MXCC20220000") > 0:
            #         get_replace = str(get_script).replace("MXCC20220000", "${entityId}")
            #         get_replace = str(get_replace).replace("STMXFINCORE0", "${tenantId}")
            #         get_data["hashTree"][1]["script"] = get_replace
            # elif get_list[0]["value"] == "1015":
            #     get_script = get_data["hashTree"][0]["script"]
            #     get_replace = str(get_script).replace("1015", "${xxl_task_id_check_overdue_split}")
            #     get_data["hashTree"][0]["script"] = get_replace
            #     get_script = get_data["hashTree"][1]["script"]
            #     if str(get_script).count("MXCC20220000") > 0:
            #         get_replace = str(get_script).replace("MXCC20220000", "${entityId}")
            #         get_replace = str(get_replace).replace("STMXFINCORE0", "${tenantId}")
            #         get_data["hashTree"][1]["script"] = get_replace


    if get_data["type"] == "scenario" and get_data["enable"] == True:
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            find_handler2_interface(subScenario, dds)

if __name__ == '__main__':
    # 输入用例id
    get_list_id = get_batch_id()
    #
    for get_one_id in get_list_id:
        find_process(get_one_id)
    # find_process("6cbf57db-ee2e-4965-8b71-d661d56e9932")

# def find_handler(get_data, dds):
#     global cur_time_line
#     if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
#         get_path = get_data["path"]
#         if get_path == "/api/admin/system/faketime":
#             get_raw = json.loads(get_data["body"]["raw"])
#             cur_time_line = str(get_raw["time"])
#         elif get_path.count("/transactions/adjustments/credit"):
#             if str(get_data["body"]["raw"]).count("PAYMENT"):
#                 if cur_time_line.count('-05') > 0:
#                     print(str(get_data["name"]) + "这里有")
#     #
#     # if get_data["type"]=="JDBCSampler" and get_data["enable"] == True:
#     #     get_sql = get_data["query"]
#     #     # if str(get_sql).count(" set ")>0:
#     #     #     get_dict = {"path":"update_sql","update_sql":  get_sql}
#     #     #     dds.append(get_dict)
#
#     if get_data["type"] == "scenario" and get_data["enable"] == True:
#         hashTree = get_data["hashTree"]
#         for subScenario in hashTree:
#             find_handler(subScenario, dds)

#
# def find_handler1(get_data, dds):
#     global cur_time_line
#     if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
#         get_path = get_data["path"]
#         if get_path == "/api/admin/system/faketime":
#             get_raw = json.loads(get_data["body"]["raw"])
#             cur_time_line = str(get_raw["time"])
#         elif get_path.count("payment"):
#             print(str(get_data["name"]) + "这里有")
#     if get_data["type"] == "scenario" and get_data["enable"] == True:
#         hashTree = get_data["hashTree"]
#         for subScenario in hashTree:
#             find_handler(subScenario, dds)
#
#
# replace_keyword = {"entityId": "COCC20230000", "tenantId": "STCOFINCORE0", "taskSource": "CREDIT_CARD_STATEMENT",
#                    "taskType": "DELINQUENCY", "batchIds": [], "batchDetailIds": [], "referenceKeys": [],
#                    "taskStatus": ["INACTIVE"]}
