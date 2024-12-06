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
            if get_data['num'] == 104875:
                break
            if get_data['num'] == 100452 :
                hashTree.insert(i,insert_hash_tree_data)
                break
    result["hashTree"]=hashTree
    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]
    get_info_udpate=MetersphereUtils.update_scenario_detail(get_post_data)
    print(get_info_udpate)
if __name__ == '__main__':
    #输入用例id
    # module_id="5a750d10-7327-4c71-ad9c-57d143809187"
    # MCI/ #MSI
    module_id_list=[
  "1fe4ac7a-a120-4d7f-8c72-21089782e342",
  "60f4d97b-2f52-4862-a390-84d1f9830cf7",
  "aa07e11a-add2-4164-8db8-b0e75d57cdc5",
  "b8cc7e36-d1ee-45ee-ae2a-1a9a35a54198",
  "dcdfc1aa-0cfc-45a4-820f-cfacb5b21b99",
            "5cd506d1-0083-4e7d-85df-7ba228b5baa0",
            "2eac8cf4-b4f5-45a8-93f0-ebab868a854d",
            "5869dab0-83fa-4b3a-a7a0-ed9d941b829b",
            "807d2f75-0d99-45e8-83e5-f9fb868d3cb1",
            "c9ae059d-4589-46bd-b02f-3f625cd52817",
        "71b0fff8-fcfb-4b53-baa7-2bcb3d22aeb1",
        "321b5420-04da-4f9b-865c-01e5aa2159af",
        "78875e78-6531-4715-9f8e-73dbd94a704b"

]


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
