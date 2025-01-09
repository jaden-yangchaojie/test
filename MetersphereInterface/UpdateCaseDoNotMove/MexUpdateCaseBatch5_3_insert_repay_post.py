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
    module_id =[
  "87343a4d-3a0c-43f5-9e35-0b4d45d0df33",
  "66bb5ed9-9802-4ae3-b491-8733f9ebf8f8",
  "74742167-1150-43a3-b19e-e46b154d533b",
  "8b66890e-0e6a-4bee-b22d-826b9b5b5b7a",
  "c9bd4106-768f-4932-8dbe-4c8b47cbb37e",
  "03a2c9e0-cb7a-4c70-ad0b-3025d86ecb30"
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
