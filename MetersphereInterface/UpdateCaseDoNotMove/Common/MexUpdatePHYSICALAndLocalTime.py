import json
import re
import time

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

    global is_updated
    is_updated = 0
    result = json.loads(get_sce_data)
    # get_data["referenced"]=='REF'
    hashTree = list(result["hashTree"])

    for i, get_data in enumerate(hashTree):
        if str(get_data).count('/v1.0/credit/contracts') > 0 and get_data["enable"]==True and get_data["referenced"]!='REF':
            if str(get_data).count("\"@email\""):
                get_tmp = str(get_data).replace("\"@email\"", "\"${__time(,)}@testcredit.com\"")
                handle_data = eval(get_tmp)
                hashTree[i] = handle_data
                is_updated = 1
                break
    result["hashTree"] = hashTree
    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]
    if is_updated == 1:
        time.sleep(3)
        get_info_udpate = MetersphereUtils.update_scenario_detail(get_post_data)
        print(get_info_udpate)
    else:
        print("no handle......")


if __name__ == '__main__':

    insert_hash_tree_data = []
    get_ids = get_batch_id([
  "e77c6e64-e125-4127-b672-054f66454053",
  "bf6940d1-8c38-4fbc-b189-907779c6febd",
  "f88ae288-30d9-415f-8746-00a7bdaec780",
  "969f7801-31bf-4db2-bbbb-d3861cc3a4d5",
  "8b791460-2aa2-4532-9b98-9fb47f292694"
])
    for get_id in get_ids:
        handler_process_data(get_id, insert_hash_tree_data)
