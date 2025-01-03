import json
import re

from MetersphereInterface import MetersphereUtils

def get_batch_id(module_id):
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50,[
  module_id
])
    return get_batch_ids
def get_batch_id_list(module_ids):
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50,module_ids)
    return get_batch_ids
# def handler_update_name(id):
#     scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
#     data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
#
#     get_sce_data = data.get("data").get("scenarioDefinition")
#     result = json.loads(get_sce_data)
#     result["name"] = "dfl逾期DQ操作1"
#     data["data"]["scenarioDefinition"] = result
#     data["data"]["name"] = "dfl逾期DQ操作1"
#     get_post_data = data["data"]
#     # get_daa=json.dumps(get_post_data)
#     MetersphereUtils.update_scenario_detail(get_post_data)
def fibonacci_handler(result):
    hashTree = result["hashTree"]
    if str(hashTree).count("/xxl-job-admin/jobinfo/trigger")>0 and str(hashTree).count("expect_time")>0:
        for i,get_data in enumerate(hashTree):
            if get_data["type"] == "scenario"  and get_data["enable"] == True:
                if str(get_data['name']).count("xxljob分期入账")>0 and str(get_data['hashTree']).count("/xxl-job-admin/jobinfo/trigger")>0:
                    result["hashTree"][i]["enable"] = False
                    print("处理单个处理入账")
                elif str(get_data['name']).count("0926") > 0 and str(get_data['hashTree']).count("/xxl-job-admin/jobinfo/trigger")>0:
                    result["hashTree"][i]["hashTree"][2]["enable"] = False
                    print("处理时间下的处理入账关闭0926")
                elif str(get_data['name']).count("1026")>0 and str(get_data['hashTree']).count("/xxl-job-admin/jobinfo/trigger")>0:
                    result["hashTree"][i]["hashTree"][2]["enable"] = False
                    print("处理时间下的处理入账关闭1026")
                elif str(get_data['name']).count("1127")>0 and str(get_data['hashTree']).count("/xxl-job-admin/jobinfo/trigger")>0:
                    result["hashTree"][i]["hashTree"][2]["enable"] = False
                    print("处理时间下的处理入账关闭1127")
                elif str(get_data['name']).count("1226")>0 and str(get_data['hashTree']).count("/xxl-job-admin/jobinfo/trigger")>0:
                    result["hashTree"][i]["hashTree"][2]["enable"] = False
                    print("处理时间下的处理入账关闭1226")







def handler_process(id):
    scenario_id= MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result=json.loads(get_sce_data)
    #todo
    fibonacci_handler(result)

    data["data"]["scenarioDefinition"]=result
    get_post_data=data["data"]
    # get_daa=json.dumps(get_post_data)
    get_info_udpate=MetersphereUtils.update_scenario_detail(get_post_data)
    print(get_info_udpate)
def handler_process_data(id):
    scenario_id= MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result=json.loads(get_sce_data)
    data["data"]["scenarioDefinition"]=result
    get_name = data["data"]["name"]
    get_name = get_name.replace("copy_", "")
    pattern=r"_[0-9a-z][0-9a-z][0-9a-z][0-9a-z]"
    get_name=re.sub(pattern,"",get_name)

    data["data"]["name"] = get_name
    get_post_data=data["data"]
    # get_daa=json.dumps(get_post_data)
    get_info_udpate=MetersphereUtils.update_scenario_detail(get_post_data)
    print()
if __name__ == '__main__':
    #输入用例id
    module_id=[
  "62c14f01-4410-44ce-a222-096e2c86d444",
  "e535a5cd-a663-4549-8d2c-db601c5b6189",
  "5a750d10-7327-4c71-ad9c-57d143809187",
  "cbe0e9dc-f69f-4ed8-ab80-d58f35f4c927",
  "03a5f314-f6bc-4c3f-afe8-deaff4b917f8",
  "f8008aa2-4ebf-4959-b44d-d7dc00a9d8cc"
]
    get_ids=get_batch_id_list(module_id)
    for get_id in get_ids:
        handler_process(get_id)
    # handler_process("102304")
    # handler_process("100651")