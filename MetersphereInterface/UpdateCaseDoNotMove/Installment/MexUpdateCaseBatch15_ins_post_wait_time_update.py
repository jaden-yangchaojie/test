import json
import re

from jsonpath import jsonpath

from MetersphereInterface import MetersphereUtils

is_updated = 0

def only_find(get_data, insert_hash_tree_data):
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:

        if str(get_data["path"]).count("/xxl-job-admin/jobinfo/trigger") > 0 :
            print(str(get_data["path"]))
            get_body = get_data["body"]
            hash_tree=get_data["hashTree"]
            if str(get_body).count("${xxl_task_id_posted}") > 0:
                if str(hash_tree).count("//String userName =")==0:
                    get_tmp = str(hash_tree).replace("String userName =", "//String userName =")
                    get_tmp = str(get_tmp).replace("vars.put(${__metersphere_env_id}", "//vars.put(${__metersphere_env_id}")
                    get_tmp = str(get_tmp).replace("vars.put(\"userName\"", "//vars.put(\"userName\"")

                    get_data["hashTree"] = eval(get_tmp)
                    global is_updated
                    is_updated = 1
                    print("chuli had to process")
            if str(get_body).count("${xxl_task_id_posted_process}") > 0:
                if str(hash_tree).count("insPostWaitTime") == 0:
                    get_tmp = str(hash_tree).replace("stmtGenerateTime", "insPostWaitTime")
                    get_data["hashTree"] = eval(get_tmp)

                    is_updated = 1
                    print("chuli had to process1")

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

    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    # todo

    fibonacci_handler(result, insert_hash_tree_data)

    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]
    # get_daa=json.dumps(get_post_data)

    if is_updated == 1:
        print("need to update")
        get_info_udpate = MetersphereUtils.update_scenario_detail(get_post_data)
        print(get_info_udpate)
    else:
        print("no need to update")


if __name__ == '__main__':
    # 输入用例id

    module_ids = [
  "87343a4d-3a0c-43f5-9e35-0b4d45d0df33",
  "66bb5ed9-9802-4ae3-b491-8733f9ebf8f8",
  "74742167-1150-43a3-b19e-e46b154d533b",
  "8b66890e-0e6a-4bee-b22d-826b9b5b5b7a",
  "03a2c9e0-cb7a-4c70-ad0b-3025d86ecb30",
  "c9bd4106-768f-4932-8dbe-4c8b47cbb37e"
]

    get_ids = MetersphereUtils.get_batch_ids(1, 50, module_ids)

    for get_id in get_ids:
        handler_process_data(get_id, "")
