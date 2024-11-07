import json

from MexInstallment import MetersphereUtils


#批量修改任务id和其他参数用例




def find_process(id):
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_single_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)

    get_list = []
    only_find(result, get_list)


def only_find(get_data, dds):
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
        get_path = get_data["path"]

        if str(get_path).count("/xxl-job-admin/jobinfo/trigger"):
            # get_list = get_data["body"]["kvs"]
            # if get_list[0]["value"]'' :
            if "DQ_STATUS_UPDATE" in str(get_data) :
                print(get_data["body"]["kvs"][1])
                # if ("{{" in str(get_data) or  "{ {"in str(get_data) or  "{  {"in str(get_data)):
                #     print("yes++++")

            # print("++++++++")

    if get_data["type"] == "scenario" and get_data["enable"] == True :
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            only_find(subScenario, dds)

if __name__ == '__main__':
    # 输入用例id
    module_ids_list=[
  "cab35b7a-0b79-4b59-86bf-ef2cb98a89a5",
  "215d2b0f-94fe-44a0-9ae5-5a38359dbda2",
  "1014bc27-e5b0-4fe3-abb8-5d93bc507fdc",
  "05f88e9a-4581-4095-8149-cc8557ee8262",
  "095a64ef-3ca7-41ed-857d-27e3b9ea6af6",
  "db96f904-7441-41b1-bb3e-33af3eeb3e17",
  "e00c1576-be16-4eb5-b8e1-3785d330ec76",
  "c83c8e7f-7026-414e-b74a-457c28ba19e2"
]
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50, module_ids_list)
    for get_one_id in get_batch_ids:
        find_process(get_one_id)
    # find_process("6cbf57db-ee2e-4965-8b71-d661d56e9932")
