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
  "87343a4d-3a0c-43f5-9e35-0b4d45d0df33",
  "66bb5ed9-9802-4ae3-b491-8733f9ebf8f8",
  "74742167-1150-43a3-b19e-e46b154d533b",
  "8b66890e-0e6a-4bee-b22d-826b9b5b5b7a",
  "c9bd4106-768f-4932-8dbe-4c8b47cbb37e",
  "03a2c9e0-cb7a-4c70-ad0b-3025d86ecb30"
]
    get_ids=get_batch_id_list(module_id)
    for get_id in get_ids:
        handler_process(get_id)
    # handler_process("102304")
    # handler_process("100651")