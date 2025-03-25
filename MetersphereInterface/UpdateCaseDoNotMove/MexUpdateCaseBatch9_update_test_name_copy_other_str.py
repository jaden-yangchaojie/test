import json
import re

from jsonpath import jsonpath

from MetersphereInterface import MetersphereUtils


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
  "27e166b2-6fee-4e5c-9916-b63e3acc8526"
]

    get_ids = MetersphereUtils.get_batch_ids(1, 50, module_ids)
    for get_id in get_ids:
        handler_process_data(get_id, "")