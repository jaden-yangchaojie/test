import json
import re

from jsonpath import jsonpath

from MetersphereInterface import MetersphereUtils
#前置检查优化

def handler_process_data(id, insert_hash_tree_data):
    global is_updated
    is_updated = 0

    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    # todo
    if str(result['hashTree'][0]['name']).count("前置检查-服务可用性验证") > 0:
        if result['hashTree'][0]['referenced'] == "Copy" and result['hashTree'][0]['enable'] == True:
            result['hashTree'][0]['referenced'] = "REF"
            is_updated = 1

    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]
    # get_daa=json.dumps(get_post_data)

    if is_updated == 1:
        print("had updated")
        get_info_udpate = MetersphereUtils.update_scenario_detail(get_post_data)
        print(get_info_udpate)
    else:
        print("no need to update")


if __name__ == '__main__':
    # 输入用例id
    # module_ids =[
    #     "b4689eaa-875c-455e-89e5-ea57fb2b6e50"
    # ]
    module_ids = [
  "b63aa2c4-8fcd-4ff2-83a8-d0d763e0ebe4",
  "af4cbe23-807d-41f8-a3cd-7fc9838d447a",
  "38766155-89ec-4824-bbf7-215c400d490e",
  "5f9c511c-9751-4516-809c-fe8a2fe5601f"
]

    get_ids = MetersphereUtils.get_batch_ids(1, 50, module_ids)

    for get_id in get_ids:
        handler_process_data(get_id, "")
