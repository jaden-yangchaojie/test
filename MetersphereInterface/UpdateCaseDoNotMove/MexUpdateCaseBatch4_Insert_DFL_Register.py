import json
import re

from MetersphereInterface import MetersphereUtils


def get_batch_id(module_id):
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50, [
        module_id
    ])
    return get_batch_ids


def get_batch_id(module_id_list):
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50, module_id_list)
    return get_batch_ids


def handler_process_data(id, insert_hash_tree_data):
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    hashTree = list(result["hashTree"])
    for i, get_data in enumerate(hashTree):
        if get_data["type"] == "scenario" and get_data["enable"] == True:
            if get_data['num'] == 104875:
                break
            if get_data['num'] == 100452:
                hashTree.insert(i, insert_hash_tree_data)
                break
    for i, get_data in enumerate(hashTree):
        hashTree[i]["index"] = i + 1
    result["hashTree"] = hashTree
    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]
    get_info_udpate = MetersphereUtils.update_scenario_detail(get_post_data)
    print(get_info_udpate)


if __name__ == '__main__':
    # 输入用例id
    # module_id="5a750d10-7327-4c71-ad9c-57d143809187"
    # MCI/ #MSI
    module_id_list = [
        "8eb53f76-f032-4e92-8396-16357612f2d6",
        "252c7ded-c1bd-41ab-98b9-a8c7e7f2f663"
    ]

    get_ids = get_batch_id(module_id_list)
    insert_detail_id = "5b00d3bd-21de-4992-8d58-a88e9f6ebeef"
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(
        insert_detail_id) if insert_detail_id.isdigit() else insert_detail_id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    result['referenced'] = 'REF'
    insert_hash_tree_data = result

    for get_id in get_ids:
        handler_process_data(get_id, insert_hash_tree_data)
