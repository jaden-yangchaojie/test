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
  "b2a54dc5-21f0-4aed-970b-037f1ef56cbe",
  "28859d83-4947-4c45-94cb-01f5c41a6006",
  "859a5a9f-29b9-4753-a891-953e62cfc2e8",
  "c3865a04-64fc-4521-8082-6055466f97c3",
  "ca631490-4ac2-472e-8519-a627bea50074"
]

    get_ids = MetersphereUtils.get_batch_ids(1, 50, module_ids)

    for get_id in get_ids:
        handler_process_data(get_id, "")
