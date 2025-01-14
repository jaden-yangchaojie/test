import json
import re

from MetersphereInterface import MetersphereUtils


def get_batch_id(module_id):
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50, [
        module_id
    ])
    return get_batch_ids


def get_batch_id_list(module_ids):
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50, module_ids)
    return get_batch_ids


def fibonacci_handler(result, insert_hash_tree_data):
    # 在账单日前一天插入入账

    hashTree = result["hashTree"]
    if str(hashTree).count("/xxl-job-admin/jobinfo/trigger") > 0 and str(hashTree).count("expect_time") > 0:
        for i, get_data in enumerate(hashTree):
            if get_data["type"] == "scenario" and get_data["enable"] == True:
                #兼容
                # if (str(get_data).count("2022-") > 0 or str(get_data).count("2023-") > 0) and str(get_data['hashTree']).count("/xxl-job-admin/jobinfo/trigger") > 0\
                #         and str(get_data).count("分期本金入账") > 0 and str(get_data).count("调整")==0 :
                #     # bool_insert=False
                #     # if len(get_data['hashTree']) >= 2:
                #     #     for k, get_sub_data in enumerate(get_data['hashTree']):
                #     #         if str(get_sub_data['name']).count("xxljob账单日分期本金入账") > 0:
                #     #             bool_insert=True
                #     #             print("处理1下有时间和调整")
                #     #     if bool_insert==True:
                #     hashTree.insert(i + 1, insert_hash_tree_data)
                #     print("处理1下有时间和调整")
                # elif str(get_data['name']).count("分期本金入账") > 0  and str(get_data['name']).count("2022-")== 0 :
                #     hashTree.insert(i + 1, insert_hash_tree_data)
                #     print("直接插入数据")
                if (str(get_data["name"]).count("2022-") > 0 or str(get_data).count("2023-") > 0) and str(get_data['hashTree']).count("/xxl-job-admin/jobinfo/trigger") > 0\
                        and str(get_data).count("账单日分期本金入账") > 0 :
                    # bool_insert=False
                    # if len(get_data['hashTree']) >= 2:
                    #     for k, get_sub_data in enumerate(get_data['hashTree']):
                    #         if str(get_sub_data['name']).count("xxljob账单日分期本金入账") > 0:
                    #             bool_insert=True
                    #             print("处理1下有时间和调整")
                    #     if bool_insert==True:
                    hashTree.insert(i + 1, insert_hash_tree_data)
                    print("处理1下有时间和调整")
                elif str(get_data['name']).count("账单日分期本金入账") > 0:
                    hashTree.insert(i + 1, insert_hash_tree_data)
                    print("直接插入数据")

            #不合适
            # if str(get_data['hashTree']).count("2022-09-25 ") > 0 :
            #
            #     hashTree.insert(i + 1, insert_hash_tree_data)
            #     print("处理add 0925入账")
            # if str(get_data['hashTree']).count("2022-10-25 ") > 0:
            #
            #     hashTree.insert(i + 1, insert_hash_tree_data)
            #     print("处理add 1025入账")
            # elif str(get_data['hashTree']).count("2022-11-25 ") > 0:
            #     hashTree.insert(i + 1, insert_hash_tree_data)
            #     print("处理add 1125入账")
            # elif str(get_data['hashTree']).count("2022-12-25 ") > 0:
            #     hashTree.insert(i + 1, insert_hash_tree_data)
            #     print("处理add 1225入账")

    for i, get_data in enumerate(hashTree):
        hashTree[i]["index"] = i + 1

    result["hashTree"] = hashTree



def handler_process_data(id, insert_hash_tree_data):
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    # todo
    fibonacci_handler(result, insert_hash_tree_data)

    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]
    # get_daa=json.dumps(get_post_data)
    get_info_udpate = MetersphereUtils.update_scenario_detail(get_post_data)
    print(get_info_udpate)


if __name__ == '__main__':
    # 输入用例id
    module_id =[
  "b0e877f8-2ba1-499c-a922-8b4a71b3c941"
]
    get_ids = get_batch_id_list(module_id)
    # for get_id in get_ids:
    #     handler_process(get_id)
    insert_detail_id = "71b29297-65a7-4989-a440-1af8a2431c45"
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(
        insert_detail_id) if insert_detail_id.isdigit() else insert_detail_id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    result['referenced'] = 'Copy'
    insert_hash_tree_data = result

    for get_id in get_ids:
        handler_process_data(get_id, insert_hash_tree_data)
