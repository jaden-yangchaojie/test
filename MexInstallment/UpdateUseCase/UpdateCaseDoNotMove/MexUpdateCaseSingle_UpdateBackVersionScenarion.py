import json
import re

import MetersphereUtils
from ColInstallment import ColScenarioHandler



def handler_process_data1(get_data):
    id="54eb3c5d-dd11-4342-bc20-e2af5cd9a3a6"
    scenario_id = ColScenarioHandler.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = ColScenarioHandler.get_scenario_detail_all_info(scenario_id)
    # get_sce_data = data.get("data").get("scenarioDefinition")
    get_columns = get_data
    scenarioDefinition=get_columns['newValue']
    result=json.loads(scenarioDefinition)
    # result['environmentMap'] = {"11406dc7-8340-401f-813f-3511a97d3fbb": "d2723bd0-7959-4c8f-b4ca-864469a6dc20"}
    data["data"]["scenarioDefinition"]=result
    # environmentJson_k=json.dumps({"11406dc7-8340-401f-813f-3511a97d3fbb": "d2723bd0-7959-4c8f-b4ca-864469a6dc20"})
    #
    # data["data"]['environmentJson'] = environmentJson_k
    # data["data"]['environmentType'] ="JSON"
    get_post_data=data["data"]
    # get_daa=json.dumps(get_post_data)
    get_info_udpate=ColScenarioHandler.update_scenario_detail(get_post_data)
    print(get_info_udpate)

if __name__ == '__main__':
    #输入用例id
    #自动化场景回退到某个版本
    get_list=MetersphereUtils.operating_log_get_source()
    get_list=get_list["data"]["listObject"]
    for i,get_one in enumerate(get_list):
        if i==7:
            # print(get_one)
            get_data=get_one['details']['columns']

            get_data=get_data[0]
            handler_process_data1(get_data)

