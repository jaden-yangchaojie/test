import json
import re

from jsonpath import jsonpath

from MetersphereInterface import MetersphereUtils

#只改签约、和产品
# STC103 ->  (subproductCode)AFFINITY03
# STC104 ->  (subproductCode)AFFINITY04
# 跑之前必须打开 前置检查-服务可用性验证
is_updated=0
pre_check_contract=True
update_param_productCode="STC104"
update_param_subproductCode="AFFINITY04"
def only_find(get_data, insert_hash_tree_data):
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:

        if str(get_data["path"]).count("/v1.0/credit/contracts") > 0:
            print(str(get_data["path"]))
            global pre_check_contract
            if pre_check_contract==True:
                pre_check_contract =False
                return
            elif pre_check_contract==False:
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

    if get_data["type"] == "scenario" and get_data["enable"] == True :
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

    global pre_check_contract
    pre_check_contract = True
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    # todo
    if str(result).count("前置检查-服务可用性验证")>0:
        pre_check_contract = True
    else:
        pre_check_contract = False
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
    # module_ids =[
    #     "b4689eaa-875c-455e-89e5-ea57fb2b6e50"
    # ]
    module_ids =[
  "faf8ed4e-1119-4b3c-8337-08cbfa8baec8",
  "f94b4a55-9b89-446f-9dcd-2904caab008d",
  "2882ca0a-8155-4c62-9af0-3039597814d5",
  "ac9735a9-bc65-434c-ab6b-cc93f57e8384",
  "302df3aa-57ae-42e9-8aa1-abded1d15fe9",
  "cefab182-f7ea-4355-8fd7-19bc7c8c09f2",
  "6b206768-980d-4de3-a6b7-e827da787a5e",
  "a2125b9c-f6a2-4c84-86a8-30198bc195ed",
  "fa671e46-5b9f-4c64-9349-5c5b42151a96",
  "f0b07734-2bb6-453b-bafa-e06d861bf9d8"
]

    for i in range(1,6):
        get_ids = MetersphereUtils.get_batch_ids(i, 50, module_ids)

        for get_id in get_ids:
            handler_process_data(get_id, "")