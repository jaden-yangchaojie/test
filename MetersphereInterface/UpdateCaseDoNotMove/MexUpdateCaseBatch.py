import json
import re

from MetersphereInterface import MetersphereUtils

def get_batch_id(module_id):
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50,[
  module_id
])
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
    if "copy_" in get_name:
        get_name=get_name.replace("copy_", "")
        result["name"]=get_name

    # hashTree = result["hashTree"]
    print()
    # for  i,get_data in enumerate(hashTree):
    #     if get_data["type"] == "scenario"  and get_data["enable"] == True:
    #         # if get_data['num']==100452 or get_data['num']==102260 or get_data['num']==100206:
    #         if str(get_data['name']).count('出账')>0 and get_data['num']==100562 :
    #             # result["hashTree"][i]['hashTree']="REF"
    #             tmp_chuzhang_hashtree=result["hashTree"][i]['hashTree']
    #             str_tmp_chuzhang_hashtree=str(tmp_chuzhang_hashtree)
    #             str_update=str_tmp_chuzhang_hashtree.replace("MXN","COP")
    #             tmp_update_hashtree=eval(str_update)
    #             result["hashTree"][i]['hashTree']=tmp_update_hashtree



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
    print()
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
    module_id="5a750d10-7327-4c71-ad9c-57d143809187"
    get_ids=get_batch_id(module_id)
    for get_id in get_ids:
        handler_process_data(get_id)
    # handler_process("102304")
    # handler_process("100651")