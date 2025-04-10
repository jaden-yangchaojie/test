import json
import re

from jsonpath import jsonpath

from MetersphereInterface import MetersphereUtils


def only_find(get_data, insert_hash_tree_data):
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
        print("no")
    if get_data["type"] == 'JDBCSampler' and get_data["enable"] == True:
        print("no")
    if get_data["type"] == 'ConstantTimer' and get_data["enable"] == True:
        get_data['delay']="3000"


    if get_data["type"] == "scenario" and get_data["enable"] == True:
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            only_find(subScenario, insert_hash_tree_data)


def fibonacci_handler(result, insert_hash_tree_data):
    hashTree = result["hashTree"]
    only_find(result, insert_hash_tree_data)
    result["hashTree"] = hashTree


def handler_process_data(id, insert_hash_tree_data):
    global is_updated
    is_updated = 0

    global pre_check_contract
    pre_check_contract = True
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
    # module_ids =[
    #     "b4689eaa-875c-455e-89e5-ea57fb2b6e50"
    # ]
    module_ids = [
        "c435271b-f655-48a8-be2c-d63cf40fef77"
    ]

    get_ids = MetersphereUtils.get_batch_ids(1, 50, module_ids)

    for get_id in get_ids:
        handler_process_data(get_id, "")
