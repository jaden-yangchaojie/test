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
    if str(hashTree).count("125000")==0:
        print("不存在......")
        return None
    for i, get_data in enumerate(hashTree):
        if get_data["type"] == "scenario" and get_data["enable"] == True:
            # if get_data['num'] == 104875 or:
            if str(get_data).count("125000")>0:
                # get_tmp=str(get_data).replace("1250.00","1250.01")
                # print(str(get_data))
                get_tmp = str(get_data).replace("125000", "125001")
                get_tmp_1=eval(get_tmp)
                hashTree[i]=get_tmp_1
    result["hashTree"]=hashTree
    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]
    get_info_udpate=MetersphereUtils.update_scenario_detail(get_post_data)
    print(get_info_udpate)
if __name__ == '__main__':
    #输入用例id
    # module_id="5a750d10-7327-4c71-ad9c-57d143809187"

    module_id_list =[
  "1fe4ac7a-a120-4d7f-8c72-21089782e342",
  "60f4d97b-2f52-4862-a390-84d1f9830cf7",
  "aa07e11a-add2-4164-8db8-b0e75d57cdc5",
  "b8cc7e36-d1ee-45ee-ae2a-1a9a35a54198",
  "dcdfc1aa-0cfc-45a4-820f-cfacb5b21b99"
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
