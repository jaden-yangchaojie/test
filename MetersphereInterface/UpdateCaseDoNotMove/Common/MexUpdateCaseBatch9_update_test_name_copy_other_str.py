import json
import re

from jsonpath import jsonpath

from MetersphereInterface import MetersphereUtils

#把copy_XXXXX_76z6 的用例名称替换掉
def handler_process_data(id, insert_hash_tree_data):

    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)


    tmp_str=data["data"]["name"]
    tmp_str=str(tmp_str).replace("copy_","")
    pattern=re.compile(r"_[a-z|0-9][a-z|0-9][a-z|0-9][a-z|0-9]")
    tmp_str=pattern.sub("",tmp_str)
    data["data"]["name"] = str(tmp_str)

    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]


    get_info_udpate = MetersphereUtils.update_scenario_detail(get_post_data)
    print(get_info_udpate)


if __name__ == '__main__':
    # 输入用例id

    module_ids =[
  "87343a4d-3a0c-43f5-9e35-0b4d45d0df33",
  "66bb5ed9-9802-4ae3-b491-8733f9ebf8f8",
  "74742167-1150-43a3-b19e-e46b154d533b",
  "8b66890e-0e6a-4bee-b22d-826b9b5b5b7a",
  "c9bd4106-768f-4932-8dbe-4c8b47cbb37e",
  "03a2c9e0-cb7a-4c70-ad0b-3025d86ecb30"
]

    get_ids = MetersphereUtils.get_batch_ids(1, 50, module_ids)
    for get_id in get_ids:
        handler_process_data(get_id, "")