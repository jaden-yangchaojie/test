import json

from ColInstallment import ColScenarioHandler
from MexInstallment import MetersphereUtils
#批量修改任务id和其他参数用例

def get_batch_id():
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50)
    return get_batch_ids


def find_process(id):
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)

    get_list = []
    only_find(result, get_list)


def only_find(get_data, dds):
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
        get_path = get_data["path"]

        if str(get_path).count("dq"):
            # get_list = get_data["body"]["kvs"]
            # if get_list[0]["value"]'' :
            #
            print("++++++++")

    if get_data["type"] == "scenario" and get_data["enable"] == True :
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            only_find(subScenario, dds)

if __name__ == '__main__':
    # 输入用例id
    get_list_id = get_batch_id()
    for get_one_id in get_list_id:
        find_process(get_one_id)
    # find_process("6cbf57db-ee2e-4965-8b71-d661d56e9932")
