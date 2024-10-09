import json

import MetersphereUtils
from ColInstallment import ColScenarioHandler



def get_batch_id():
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50,[
  "51b3b82f-2dd2-4ed3-9f90-1eb7e975c0cd",
  "54dc2e01-234c-4456-a9b5-68dba146593f",
  "e9d7c1b2-0c83-4a09-b78e-17c81bc79e0e"
])
    return get_batch_ids

def handler_update_name(id):
    scenario_id = ColScenarioHandler.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = ColScenarioHandler.get_scenario_detail_all_info(scenario_id)

    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    result["name"] = "dfl逾期DQ操作1"
    data["data"]["scenarioDefinition"] = result
    data["data"]["name"] = "dfl逾期DQ操作1"
    get_post_data = data["data"]
    # get_daa=json.dumps(get_post_data)
    ColScenarioHandler.update_scenario_detail(get_post_data)
def fibonacci_handler(result):

    print()
    hashTree = result["hashTree"]

    for  i,get_data in enumerate(hashTree):
        if get_data["type"] == "scenario"  and get_data["enable"] == True:
            # if get_data['num']==100452 or get_data['num']==102260 or get_data['num']==100206:
            if get_data['num'] ==12307:
                 result["hashTree"][i]['referenced']="REF"


def handler_process(id):
    scenario_id= ColScenarioHandler.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = ColScenarioHandler.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result=json.loads(get_sce_data)
    #todo
    fibonacci_handler(result)

    data["data"]["scenarioDefinition"]=result
    get_post_data=data["data"]
    # get_daa=json.dumps(get_post_data)
    get_info_udpate=ColScenarioHandler.update_scenario_detail(get_post_data)
    print()

if __name__ == '__main__':
    #输入用例id
    get_ids=get_batch_id()
    for get_id in get_ids:
        handler_process(get_id)
    # handler_process("102304")
    # handler_process("100651")