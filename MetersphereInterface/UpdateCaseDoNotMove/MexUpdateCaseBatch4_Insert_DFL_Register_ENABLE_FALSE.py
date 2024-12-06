import json
import re

from MetersphereInterface import MetersphereUtils


def get_batch_id(module_id):
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50,[
  module_id
])
    return get_batch_ids
def get_batch_id(module_id_list):
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50,module_id_list)
    return get_batch_ids
def handler_process_data(id, insert_hash_tree_data):
    scenario_id= MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result=json.loads(get_sce_data)
    hashTree=list(result["hashTree"])
    for i, get_data in enumerate(hashTree):
        if get_data["type"] == "scenario" and get_data["enable"] == True:
            # if get_data['num'] == 104875 or:
            if get_data['num'] == 100452:
                hashTree[i]["enable"]=False
    result["hashTree"]=hashTree
    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]
    get_info_udpate=MetersphereUtils.update_scenario_detail(get_post_data)
    print(get_info_udpate)
if __name__ == '__main__':
    #输入用例id
    # module_id="5a750d10-7327-4c71-ad9c-57d143809187"

    module_id_list=[
        "71b0fff8-fcfb-4b53-baa7-2bcb3d22aeb1",
        "321b5420-04da-4f9b-865c-01e5aa2159af",
        "78875e78-6531-4715-9f8e-73dbd94a704b"
]
    # MSI
    # module_id_list = [
    #     "44cb03af-f6e0-4f6a-813f-60f061b0f09d",
    #     "26ce0b3d-4a3a-4958-8301-b5ab5a76cb05",
    #     "7887c215-0feb-4486-911b-3927a72e4a47",
    #     "91a5538d-c326-46bc-aa68-f842ad99dada",
    #     "6933991f-e132-4580-8efe-5ef8de86f3ea"
    # ]
    # module_id_list = [
    #     "d6dbe6e4-ebd8-4f94-8200-116d13a8beea"
    # ]
    get_ids=get_batch_id(module_id_list)
    insert_detail_id="5b00d3bd-21de-4992-8d58-a88e9f6ebeef"
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(insert_detail_id) if insert_detail_id.isdigit() else insert_detail_id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    result['referenced']='REF'
    insert_hash_tree_data=result

    for get_id in get_ids:
        handler_process_data(get_id,insert_hash_tree_data)
