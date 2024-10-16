import json

import MetersphereUtils
from ColInstallment import ColScenarioHandler



def get_batch_id():
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50,[
  "e00c1576-be16-4eb5-b8e1-3785d330ec76"
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
            if str(get_data['name']).count('出账')>0 and get_data['num']==100562 :
                # result["hashTree"][i]['hashTree']="REF"
                tmp_chuzhang_hashtree=result["hashTree"][i]['hashTree']
                str_tmp_chuzhang_hashtree=str(tmp_chuzhang_hashtree)
                str_update=str_tmp_chuzhang_hashtree.replace("MXN","COP")
                tmp_update_hashtree=eval(str_update)
                result["hashTree"][i]['hashTree']=tmp_update_hashtree



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