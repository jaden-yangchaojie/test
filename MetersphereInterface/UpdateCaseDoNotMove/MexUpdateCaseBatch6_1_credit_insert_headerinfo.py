import json
import re

from MetersphereInterface import MetersphereUtils


def get_batch_id(module_id):
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50, [
        module_id
    ])
    return get_batch_ids


def get_batch_id_list(module_ids):
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50, module_ids)
    return get_batch_ids


def fibonacci_handler(result, insert_hash_tree_data):

    hashTree = result["hashTree"]

    for i, get_data in enumerate(hashTree):

        if get_data["type"] == "scenario" and get_data["enable"] == True:
            if len(get_data["hashTree"])>0:
                bool_insert=False
                get_data_1_hashTree=get_data["hashTree"]
                for k, get_data_1 in enumerate(get_data_1_hashTree):
                    if get_data_1["type"] == 'HTTPSamplerProxy' and str(get_data_1["path"]).count("v1.0")>0 and get_data_1["enable"] == True:
                        headers=list(get_data_1["headers"])
                        headers.append(insert_hash_tree_data)
                        bool_insert=True
                        hashTree[i]["hashTree"][k]["headers"]=headers
                        print("已处理一层："+str(get_data_1["path"]))
                    #三层
                    elif get_data_1["type"] == "scenario" and get_data_1["enable"] == True:
                        for kk, get_data_2 in enumerate(get_data["hashTree"]["hashTree"]):
                            if get_data_2["type"] == 'HTTPSamplerProxy' and str(get_data_2["path"]).count(
                                    "v1.0") > 0 and get_data_2["enable"] == True:
                                headers = list(get_data_2["headers"])
                                headers.append(insert_hash_tree_data)
                                bool_insert = True
                                hashTree[i]["hashTree"][k]["hashTree"][kk]["headers"] = headers
                                print("已处理2层：" + str(get_data_1["path"]))


        else:
            if get_data["type"] == 'HTTPSamplerProxy' and str(get_data["path"]).count("v1.0") > 0 and get_data["enable"] == True:
                headers = list(get_data["headers"])
                headers.append(insert_hash_tree_data)
                bool_insert = True
                hashTree[i]["headers"] = headers
                print("直接插入"+str(get_data["path"]))






    result["hashTree"] = hashTree



def handler_process_data(id, insert_hash_tree_data):
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    # todo
    fibonacci_handler(result, insert_hash_tree_data)

    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]
    # get_daa=json.dumps(get_post_data)
    get_info_udpate = MetersphereUtils.update_scenario_detail(get_post_data)
    print(get_info_udpate)


if __name__ == '__main__':
    # 输入用例id
    module_id =[
  "9aa6c422-d881-4fd5-952c-2c4ad5896ee2"
    ]
    get_ids = get_batch_id_list(module_id)
    for get_id in get_ids:
        handler_process_data(get_id, {'enable': True, 'file': False, 'name': 'X-Customer-Id', 'required': True, 'urlEncode': False, 'valid': True, 'value': '${X-Customer-Id}'})
