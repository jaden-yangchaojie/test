import json

from ColInstallment import ColScenarioHandler


def get_batch_id():
    get_batch_ids = ColScenarioHandler.get_batch_ids(1, 50)
    return get_batch_ids


def find_process(id):
    scenario_id = ColScenarioHandler.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = ColScenarioHandler.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    get_list = []
    cur_time_line = ""

    find_handler1(result, get_list)


cur_time_line = ""


def find_handler(get_data, dds):
    global cur_time_line
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
        get_path = get_data["path"]
        if get_path == "/api/admin/system/faketime":
            get_raw = json.loads(get_data["body"]["raw"])
            cur_time_line = str(get_raw["time"])
        elif get_path.count("/transactions/adjustments/credit"):
            if str(get_data["body"]["raw"]).count("PAYMENT"):
                if cur_time_line.count('-05') > 0:
                    print(str(get_data["name"]) + "这里有")
    #
    # if get_data["type"]=="JDBCSampler" and get_data["enable"] == True:
    #     get_sql = get_data["query"]
    #     # if str(get_sql).count(" set ")>0:
    #     #     get_dict = {"path":"update_sql","update_sql":  get_sql}
    #     #     dds.append(get_dict)

    if get_data["type"] == "scenario" and get_data["enable"] == True:
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            find_handler(subScenario, dds)


def find_handler1(get_data, dds):
    global cur_time_line
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
        get_path = get_data["path"]
        if get_path == "/api/admin/system/faketime":
            get_raw = json.loads(get_data["body"]["raw"])
            cur_time_line = str(get_raw["time"])
        elif get_path.count("payment"):
            print(str(get_data["name"]) + "这里有")
    if get_data["type"] == "scenario" and get_data["enable"] == True:
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            find_handler(subScenario, dds)


if __name__ == '__main__':
    # 输入用例id
    get_list_id = get_batch_id()
    for get_one_id in get_list_id:
        find_process(get_one_id)
