import json
import re

from MetersphereInterface import MetersphereUtils

def get_batch_id(module_id_list):
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50,module_id_list)
    return get_batch_ids
def handler_process_data(id, project_id, set_running_env_id):
    scenario_id= MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
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
    get_info_udpate=MetersphereUtils.update_scenario_detail(get_post_data)
    print(get_info_udpate)
if __name__ == '__main__':
    #输入用例id
    module_id_list = [
        "5cd506d1-0083-4e7d-85df-7ba228b5baa0",
        "2eac8cf4-b4f5-45a8-93f0-ebab868a854d",
        "5869dab0-83fa-4b3a-a7a0-ed9d941b829b",
        "807d2f75-0d99-45e8-83e5-f9fb868d3cb1",
        "c9ae059d-4589-46bd-b02f-3f625cd52817",
        "71b0fff8-fcfb-4b53-baa7-2bcb3d22aeb1",
        "321b5420-04da-4f9b-865c-01e5aa2159af",
        "78875e78-6531-4715-9f8e-73dbd94a704b"
    ]
    # MSI
    # module_id_list = [
    #     "44cb03af-f6e0-4f6a-813f-60f061b0f09d",
    #     "26ce0b3d-4a3a-4958-8301-b5ab5a76cb05",
    #     "7887c215-0feb-4486-911b-3927a72e4a47",
    #     "91a5538d-c326-46bc-aa68-f842ad99dada",
    #     "6933991f-e132-4580-8efe-5ef8de86f3ea"
    # ]
    # module_id_list = [
    #     "d6dbe6e4-ebd8-4f94-8200-116d13a8beea"
    # ]
    get_ids = get_batch_id(module_id_list)
    #固定
    set_running_env_id = "17ee4027-94c3-4740-9f57-27f10629c462"
    project_id = "11406dc7-8340-401f-813f-3511a97d3fbb"
    for id in get_ids:
        handler_process_data(id, project_id, set_running_env_id)

