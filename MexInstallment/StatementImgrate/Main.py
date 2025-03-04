import json
import sys

from MetersphereInterface import MetersphereUtils
from StatementImgrate import StoriBatch
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


if __name__ == '__main__':

#     module_id = [
#   "99031a6d-27a1-4065-9c40-5a0a06395177"
# ]
#     get_ids = get_batch_id_list(module_id)
    get_ids=["938d6ba2-83f5-49d2-8920-d257ca709f67"]
    for get_id in get_ids:
        handler_process(get_id)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # sys.exit()
