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


# 关闭
def fibonacci_handler(result):
    get_name = result["name"]
    hashTree = result["hashTree"]
    for i, get_data in enumerate(hashTree):
        if get_data["type"] == "scenario" and get_data["enable"] == True:
            if str(get_data['name']).count("哥伦比亚修改当前时间") > 0 and i > 3:
                result["hashTree"][i]["enable"] = False
                print("已关闭last 当前时间")


def handler_process(id):
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    # todo
    fibonacci_handler(result)

    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]
    # get_daa=json.dumps(get_post_data)
    get_info_udpate = MetersphereUtils.update_scenario_detail(get_post_data)
    print(get_info_udpate)


if __name__ == '__main__':
    # 输入用例id
    module_id = [
  "541f6421-56e1-40c2-9e59-24b60e9720d3",
  "b0e877f8-2ba1-499c-a922-8b4a71b3c941",
  "f3cfd270-efbe-4bb3-b2c3-93e1d9ccf86b",
  "52de5366-ac7b-403d-87c9-05b55c9c8269",
  "2bc2a96c-b1fa-41a9-9b98-10f4efdeb59f",
  "e3a1cf0e-6fa5-4a7c-99f8-a3a20a511955",
  "5fa612fc-8912-44d1-9129-7c2aa40fb245",
  "6fa25ba7-b90e-46be-8b3b-6db6f23ffde9"
]
    get_ids = get_batch_id_list(module_id)
    for get_id in get_ids:
        handler_process(get_id)
