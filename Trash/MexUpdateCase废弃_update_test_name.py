import json

from MetersphereInterface import MetersphereUtils

def handler_update_name(id):

    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data =  MetersphereUtils.get_scenario_detail_all_info(scenario_id)

    get_sce_data = data.get("data").get("scenarioDefinition")
    # result = json.loads(get_sce_data)
    # result["name"] = "dfl逾期DQ操作1"
    # data["data"]["scenarioDefinition"] = result
    tmp_str=data["data"]["name"]
    str(tmp_str).replace("copy_","")
    data["data"]["name"] = "dfl逾期DQ操作1"
    get_post_data = data["data"]
    # get_daa=json.dumps(get_post_data)
    MetersphereUtils.update_scenario_detail(get_post_data)

def handler_process(id):
    scenario_id= MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result=json.loads(get_sce_data)
    #todo

    data["data"]["scenarioDefinition"]=result
    get_post_data=data["data"]
    # get_daa=json.dumps(get_post_data)
    get_info_udpate=MetersphereUtils.update_scenario_detail(get_post_data)
    print()

if __name__ == '__main__':
    #输入用例id
    handler_process("102629")
    # handler_process("102304")
    # handler_process("100651")