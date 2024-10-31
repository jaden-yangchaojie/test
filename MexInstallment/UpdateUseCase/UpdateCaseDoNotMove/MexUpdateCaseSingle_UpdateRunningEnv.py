import json
import re

import MetersphereUtils
from ColInstallment import ColScenarioHandler





def handler_process_data(id, project_id, set_running_env_id):
    scenario_id= ColScenarioHandler.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = ColScenarioHandler.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result=json.loads(get_sce_data)
    result['environmentMap'] = {project_id: set_running_env_id}

    data["data"]["scenarioDefinition"]=result
    environmentJson_k="{\""+project_id+"\": \""+set_running_env_id +"\"}"
    # environmentJson_k = json.dumps({"11406dc7-8340-401f-813f-3511a97d3fbb\": \"d2723bd0-7959-4c8f-b4ca-864469a6dc20\"})

    data["data"]['environmentJson'] = environmentJson_k
    data["data"]['environmentType'] ="JSON"
    get_post_data=data["data"]
    # get_daa=json.dumps(get_post_data)
    get_info_udpate=ColScenarioHandler.update_scenario_detail(get_post_data)
    print(get_info_udpate)
if __name__ == '__main__':
    #输入用例id
    id="54eb3c5d-dd11-4342-bc20-e2af5cd9a3a6"
    # "qa-test-dfl-new-eks"
    set_running_env_id="d2723bd0-7959-4c8f-b4ca-864469a6dc20"
    project_id = "11406dc7-8340-401f-813f-3511a97d3fbb"

    handler_process_data(id, project_id, set_running_env_id)

