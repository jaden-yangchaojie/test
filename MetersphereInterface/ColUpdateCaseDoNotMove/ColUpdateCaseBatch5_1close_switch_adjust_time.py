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

def fibonacci_handler(result):
    get_name = result["name"]
    hashTree = result["hashTree"]
    if str(hashTree).count("/xxl-job-admin/jobinfo/trigger") > 0 and str(hashTree).count("expect_time") > 0:
        for i, get_data in enumerate(hashTree):

                if get_data["type"] == "scenario" and get_data["enable"] == True :
                    if str(get_data).count("/xxl-job-admin/jobinfo/trigger") > 0:
                        # 优先处理这个
                        if str(get_data['name']).count("触发调整时间") > 0 and str(get_data['hashTree']).count(
                                "修改系统时间") > 0:
                            if len(get_data['hashTree']) >= 2:
                                for k, get_sub_data in enumerate(get_data['hashTree']):
                                    if str(get_sub_data['name']).count("触发调整时间") > 0:
                                        result["hashTree"][i]["hashTree"][k]["enable"] = False
                                        print("处理1下有时间和调整")
                        #再处理
                        elif str(get_data['name']).count("账单日前触发调整时间") > 0:
                            result["hashTree"][i]["enable"] = False
                            print("处理2直接触发调整时间")


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
    module_id =[
  "5fa612fc-8912-44d1-9129-7c2aa40fb245"
]
    get_ids = get_batch_id_list(module_id)
    for get_id in get_ids:
        handler_process(get_id)

