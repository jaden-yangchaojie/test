import json

from MetersphereInterface import MetersphereUtils
from StatementImgrate import StoriScenario



def get_batch_id_list(module_ids):
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50, module_ids)
    return get_batch_ids
def handler_process(id):
    scenario_id= MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result=json.loads(get_sce_data)
    # batch = StoriBatch(dir="Scenario", fileNames=["core1","core2","core3","coren"])
    # StoriScenario.DefalutScenario(result).handleScenario(scenario=result)
    StoriScenario.StatementScenario(result).handleScenario(scenario=result)
    # print(result)
    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]
    get_info_udpate = MetersphereUtils.update_scenario_detail(get_post_data)
    print(get_info_udpate)


if __name__ == '__main__':

#     module_id = [
#   "99031a6d-27a1-4065-9c40-5a0a06395177"
# ]
#     get_ids = get_batch_id_list(module_id)
    get_ids=["2d593f1c-75fe-4bf2-9ea6-7eba288ee0ea"]
    for get_id in get_ids:
        handler_process(get_id)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # sys.exit()
