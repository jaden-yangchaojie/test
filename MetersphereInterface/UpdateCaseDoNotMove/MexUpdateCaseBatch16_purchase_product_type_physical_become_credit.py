import json
import re

from jsonpath import jsonpath

from MetersphereInterface import MetersphereUtils

is_updated=0
def only_find(get_data, insert_hash_tree_data):
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:

        if str(get_data["path"]).count("/v1.0/credit/authorizations/posting") > 0 or str(get_data["path"]).count("/v1.0/credit/authorizations")>0 or str(get_data["path"]).count("/backoffice/dfl-ng/credit/authorizations/posting")>0 or  str(get_data["path"]).count("/transactions/authorizations")>0:
            print(str(get_data["path"]))
            get_body = get_data["body"]
            if str(get_body).count("PHYSICAL")>0:
                get_tmp=str(get_body).replace("PHYSICAL","CREDIT")
                get_data["body"] = eval(get_tmp)
                global  is_updated
                is_updated=1
                print("chuli had to process")
    if get_data["type"] == "scenario" and get_data["enable"] == True and 'referenced' in get_data and (
            get_data['referenced'] == "Copy" or get_data['referenced'] == 'Created'):
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            only_find(subScenario, insert_hash_tree_data)


def fibonacci_handler(result, insert_hash_tree_data):
    hashTree = result["hashTree"]
    only_find(result, insert_hash_tree_data)
    result["hashTree"] = hashTree


def handler_process_data(id, insert_hash_tree_data):
    global is_updated
    is_updated=0
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    # todo
    fibonacci_handler(result, insert_hash_tree_data)

    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]
    # get_daa=json.dumps(get_post_data)
    if is_updated==1:
        print("need to update")
        get_info_udpate = MetersphereUtils.update_scenario_detail(get_post_data)
        print(get_info_udpate)
    else:
        print("no need to update")



if __name__ == '__main__':
    # 输入用例id

    module_ids =[
  "991a79a0-2504-4bfe-886d-258f6f99569e"
]


    get_ids = MetersphereUtils.get_batch_ids(1, 50, module_ids)
#     get_ids = ["08e1e980-e177-409a-9791-7b5ec988fa79"]

    for get_id in get_ids:
        handler_process_data(get_id, "")