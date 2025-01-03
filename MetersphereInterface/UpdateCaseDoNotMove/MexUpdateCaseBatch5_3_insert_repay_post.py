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

    for i, get_data in enumerate(hashTree):
        if get_data["type"] == "scenario" and get_data["enable"] == True:
            if str(get_data['hashTree']).count("2022-09-26 ") > 0:

                hashTree.insert(i + 1, insert_hash_tree_data)
                print("处理add 0926入账")
            elif str(get_data['hashTree']).count("2022-10-26 ") > 0:
                tmp_insert = str(insert_hash_tree_data).replace("$.data.repayPlanList[0].postDate",
                                                                "$.data.repayPlanList[1].postDate")
                tmp_insert = tmp_insert.replace("$.data.repayPlanList[0].planStatus",
                                                "$.data.repayPlanList[1].planStatus")
                insert_hash_tree_data_dict = eval(tmp_insert)
                hashTree.insert(i + 1, insert_hash_tree_data_dict)
                print("处理add 1026入账")
            elif str(get_data['hashTree']).count("2022-11-27 ") > 0:
                tmp_insert = str(insert_hash_tree_data).replace("$.data.repayPlanList[0].postDate",
                                                                "$.data.repayPlanList[2].postDate")
                tmp_insert = tmp_insert.replace("$.data.repayPlanList[0].planStatus",
                                                "$.data.repayPlanList[2].planStatus")
                insert_hash_tree_data_dict = eval(tmp_insert)
                hashTree.insert(i + 1, insert_hash_tree_data_dict)
                print("处理add 1127入账")
            elif str(get_data['hashTree']).count("2022-12-26 ") > 0:
                tmp_insert = str(insert_hash_tree_data).replace("$.data.repayPlanList[0].postDate",
                                                                "$.data.repayPlanList[3].postDate")
                tmp_insert = tmp_insert.replace("$.data.repayPlanList[0].planStatus",
                                                "$.data.repayPlanList[3].planStatus")
                insert_hash_tree_data_dict = eval(tmp_insert)
                hashTree.insert(i + 1, insert_hash_tree_data_dict)
                print("处理add 1226入账")

    for i, get_data in enumerate(hashTree):
        hashTree[i]["index"] = i + 1

    result["hashTree"] = hashTree
    #     if str(get_data['hashTree']).count('GID')>0 :
    #         tmp=hashTree[i]
    #         tem_2=str(tmp).replace("GID","THALES")
    #         result["hashTree"][i]=eval(tem_2)
    #         # result["hashTree"][i] = "GID"
    #         # result["hashTree"][i]['id']="5b00d3bd-21de-4992-8d58-a88e9f6ebeef"
    #         # result["hashTree"][i]['referenced']="REF"
    #         break
    # # if get_data['num']==102260:
    # #     result["hashTree"][i]['referenced']="REF"


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
    module_id = [
        "62c14f01-4410-44ce-a222-096e2c86d444",
        "e535a5cd-a663-4549-8d2c-db601c5b6189",
        "5a750d10-7327-4c71-ad9c-57d143809187",
        "cbe0e9dc-f69f-4ed8-ab80-d58f35f4c927",
        "03a5f314-f6bc-4c3f-afe8-deaff4b917f8",
        "f8008aa2-4ebf-4959-b44d-d7dc00a9d8cc"
    ]
    get_ids = get_batch_id_list(module_id)
    # for get_id in get_ids:
    #     handler_process(get_id)
    insert_detail_id = "07665ce1-30f8-4e02-a170-922ea5b74156"
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(
        insert_detail_id) if insert_detail_id.isdigit() else insert_detail_id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    result['referenced'] = 'Copy'
    insert_hash_tree_data = result

    for get_id in get_ids:
        handler_process_data(get_id, insert_hash_tree_data)
