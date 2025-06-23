import json
import re

from jsonpath import jsonpath

from MetersphereInterface import MetersphereUtils

is_updated = 0

true = True


def only_find(get_data, insert_str_data):
    global is_updated
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:

        if str(get_data["path"]).count("/v1.0/backoffice-ng/credit/marketing/mockStrategyEngine") > 0:
            if get_data["enable"] == True:
                get_data["enable"] = False
                is_updated = 1
                print("处理mock....")

    if str(get_data["type"]) == "IfController" and get_data["enable"] == True:
        # if get_data["enable"] == True and str(get_data['variable']).find("mock_") !=-1:
        if get_data["enable"] == True and str(get_data['variable']).count("mock_") > 0:
            get_data["enable"] = False
            is_updated = 1
            print("处理if.....")

    if get_data["type"] == "scenario" and get_data["enable"] == True:
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            only_find(subScenario, insert_str_data)


def fibonacci_handler(result, insert_str_data):
    hashTree = result["hashTree"]
    only_find(result, insert_str_data)
    result["hashTree"] = hashTree


def handler_process_data(id, insert_str_data):
    global is_updated
    is_updated = 0

    global pre_check_contract
    pre_check_contract = True
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    # todo
    # get_name=get_dict_one["name"]
    # get_name=str(get_name).replace("copy_", "")
    # pattern = r"_[0-9a-z][0-9a-z][0-9a-z][0-9a-z]"

    #
    # get_name = re.sub(pattern, "", get_name)
    fibonacci_handler(result, insert_str_data)
    # todo

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
    # 获取数据
    get_list_data = MetersphereUtils.module_list()
    dict_data_list = []
    # get_result=get_list["data"]
    # get_level1 = jsonpath(get_list_data,
    #                       "$.data.[?(@.name=='营销')].children[?(@.name=='返现集成测试new关闭mock')].children.[id,name,parentId])")
    get_level1 = jsonpath(get_list_data,
                          "$.data.[?(@.name=='营销')].children[?(@.name=='redemption集成测试new关闭mock')].children.[id,name,parentId])")
    print(get_level1)
    num = len(get_level1)
    for i, get_one in enumerate(get_level1):
        if i < num - 1 and i % 2 == 0:
            dict_data_list.append({"id": get_level1[i], "name": get_level1[i + 1]})

    print(dict_data_list)

    # dir_dict_data_list = [{'id': '8eb61faf-edd5-4c0f-b030-c186eb75fa1d', 'name': '账期限额'},
    #                       # {'id': '8a54eb67-50ef-44d0-b55b-1b6749ef1b04', 'name': '账期限次'},
    #                       # {'id': 'f17b64a7-6cd8-4691-bab6-6a5c4e0fe934', 'name': '时间区间内限额'},
    #                       # {'id': '51a96aac-0a24-43a2-b577-03df2b2ce2ec', 'name': '时间区间内限次'},
    #                       # {'id': '8034ef15-3b4c-4caf-b898-39f15da98db7', 'name': '新模型账期限额'},
    #                       # {'id': '11544c0a-8ca0-4596-ac0c-fb7640cb7269', 'name': '新模型账期限次'},
    #                       # {'id': '345f2547-b3d0-4aca-89f9-ad2dd8507bd6', 'name': '新模型账期限次限额'},
    #                       # {'id': '00d5a460-4819-46d3-8117-b72a30cebb3e', 'name': '新模型账期固定金额限次'},
    #                       # {'id': '551c1899-d706-494b-8309-d2f2fe924241', 'name': '以签约时间为计算返现有效期'},
    #                       # {'id': '76628c25-1b0f-4ac8-92b5-959f2ec2cebe', 'name': '以CL为返现额度'},
    #                       # {'id': '822b21e6-b419-4460-bfa3-ea283d1686d6', 'name': '活动时间限额'},
    #                       # {'id': '4e087db6-dd91-4616-9966-b2818bf2a8e8', 'name': '活动时间限次'},
    #                       # {'id': 'dfd401ef-22eb-409f-ab28-63054765412d', 'name': '活动时间限额限次'},
    #                       # {'id': '586b3c06-314c-481a-a83a-7410f0a2bd93', 'name': '活动时间固定金额限次'},
    #                       # {'id': 'fea0af7e-41f4-4066-93e2-83506b10f27b', 'name': '自然月限额限次'},
    #                       # {'id': '2364ba18-09a8-4332-9068-efc287af5fae', 'name': '根据签约范围添加活动返现资格'}
    #                       ]
    # redemption = [{'id': 'b7849af5-a3a9-43cb-a210-c5c075ac5142', 'name': '账期限额'},
    #               {'id': 'cdd9fd57-92d4-473a-8f66-eb5fd098f72a', 'name': '账期限次'},
    #               {'id': '374226c0-f30c-4f79-b6a7-c456182b35db', 'name': '账期限额限次'},
    #               {'id': '1805be47-dcdb-4623-99f4-af5da2a420fb', 'name': '账期固定金额限次'},
    #               {'id': '89ae5808-51d3-460d-b605-9b3a65dd1a49', 'name': '区间限次'},
    #               {'id': '99d4aa22-b295-448f-8a39-fd9f68b2614c', 'name': '区间限额'},
    #               {'id': '2b08fa8f-0dda-4568-82a3-df98a9b3442d', 'name': '活动限额'},
    #               {'id': 'e3276277-10e8-4721-ba4b-d40429d8857f', 'name': '活动限次'},
    #               {'id': '76a24768-133e-42ef-859f-1fdd7af16ec9', 'name': '活动限额限次'},
    #               {'id': 'c3c49c10-9e70-4590-ac39-df09ae721b7b', 'name': '活动固定金额限次'},
    #               {'id': 'e8d4bb9c-e80c-4b8a-b3fe-f74a88c278e9', 'name': '用户维度返现有效期'},
    #               {'id': '9b74aecf-5c63-4763-9b26-fde14859f90d', 'name': '用户维度限额'},
    #               {'id': 'fcfb5a49-6a4d-4f9b-9dd9-7b3750a96d2e', 'name': '自然月限额限次'}
    #               ]
    #
    # for get_one in dir_dict_data_list:
    #
    #     get_module_id = get_one["id"]
    #     get_ids = MetersphereUtils.get_batch_ids(1, 50, [get_module_id])
    #     for get_id in get_ids:
    #         handler_process_data(get_id, "")
