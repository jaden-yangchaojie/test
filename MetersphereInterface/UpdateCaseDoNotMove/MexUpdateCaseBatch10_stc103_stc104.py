import json
import re

from jsonpath import jsonpath

from MetersphereInterface import MetersphereUtils

#只改签约、和产品
# STC103 ->  (subproductCode)AFFINITY03
# STC104 ->  (subproductCode)AFFINITY04
is_updated=0
update_param_productCode="STC003"
update_param_subproductCode="AFFINITY03"
def only_find(get_data, insert_hash_tree_data):
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:

        if str(get_data["path"]).count("/v1.0/credit/contracts") > 0 :
            print(str(get_data["path"]))
            get_body = get_data["body"]
            if str(get_body).count("STC001")>0 or  str(get_body).count("STC002")>0 or  str(get_body).count("${productCode}")>0:
                get_tmp=(str(get_body).replace("STC001",update_param_productCode)
                         .replace("STC002", update_param_productCode)
                         .replace("${productCode}", update_param_productCode))
                get_tmp = (str(get_tmp).replace("construye", update_param_subproductCode)
                           .replace("clasica", update_param_subproductCode)
                           .replace("projectx", update_param_subproductCode)
                           .replace("lider", update_param_subproductCode)
                           .replace("${subproductCode}", update_param_subproductCode))

                get_data["body"] = eval(get_tmp)
                global  is_updated
                is_updated=1
                print("need to process")

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
        print("had updated")
        get_info_udpate = MetersphereUtils.update_scenario_detail(get_post_data)
        print(get_info_udpate)
    else:
        print("no need to update")



if __name__ == '__main__':
    # 输入用例id

    module_ids =[
  "fde3ae40-ad4a-4192-ac29-14b81cdbfaa3",
  "b4689eaa-875c-455e-89e5-ea57fb2b6e50",
  "7ea5c6a9-408b-4817-b0cc-a58f5c55401c",
  "cf3a9157-bbe8-49ea-9aa0-d3dfe8ed383f",
  "6f54cd81-83fd-4421-a1d3-bffcfb848413",
  "7e4f52b7-e8da-4fa7-9201-321fca5b896f",
  "4014445e-d0f0-4ee3-8adc-349ef7569896",
  "531b5dee-d4f3-484a-a7e4-c531c15dfa64",
  "b772e3bb-b8c5-4402-b96f-fa007bdf3461",
  "4397b332-b7f6-4f73-806e-a858f90f54c9"
]

    for i in range(1,5):
        get_ids = MetersphereUtils.get_batch_ids(1, 50, module_ids)

        for get_id in get_ids:
            handler_process_data(get_id, "")