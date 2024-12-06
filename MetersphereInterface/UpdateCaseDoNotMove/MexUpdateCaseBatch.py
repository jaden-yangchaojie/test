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
    get_name=result["name"]
    # if "copy_" in get_name:
    #     get_name=get_name.replace("copy_", "")
    #     result["name"]=get_name

    hashTree = result["hashTree"]
    for  i,get_data in enumerate(hashTree):
        if get_data["type"] == "scenario"  and get_data["enable"] == True:
            if get_data['num']==100452:
            # if str(get_data['name']).count('出账')>0 and get_data['num']==100562 :
                result["hashTree"][i]['num'] = "104875"
                result["hashTree"][i]['id']="5b00d3bd-21de-4992-8d58-a88e9f6ebeef"
                result["hashTree"][i]['referenced']="REF"

            # if get_data['num']==102260:
            #     result["hashTree"][i]['referenced']="REF"





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
  "318ad5f2-7d95-4b1c-a06c-ff4d9445a866",
  "1a26e9eb-0d81-43da-bcfa-230c31ab9576",
  "368982c9-2e96-4465-a3c0-7bbcdf800385",
  "6f5300aa-9b2b-40f5-9a43-23320f3d2015",
  "c3fc0c30-03d5-4634-a68a-4b2142908974"
]
    get_ids=get_batch_id_list(module_id)
    for get_id in get_ids:
        handler_process(get_id)
    # handler_process("102304")
    # handler_process("100651")