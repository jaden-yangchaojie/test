import json

from MetersphereInterface import MetersphereUtils


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
        # get_path = get_data["path"]

        if str(get_data).count("debit/"):
            # # get_list = get_data["body"]["kvs"]
            # # if get_list[0]["value"]'' :
            # if "DQ_STATUS_UPDATE" in str(get_data) :
            #     print(get_data["body"]["kvs"][1])
            #     # if ("{{" in str(get_data) or  "{ {"in str(get_data) or  "{  {"in str(get_data)):
            #     #     print("yes++++")

            print("++++++++")

    if get_data["type"] == "scenario" and get_data["enable"] == True :
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            only_find(subScenario, dds)

if __name__ == '__main__':
    # 输入用例id
    module_ids_list=[
  "c252ced6-b1d1-49ec-9f0b-21a3028cd48c",
  "cab35b7a-0b79-4b59-86bf-ef2cb98a89a5",
  "215d2b0f-94fe-44a0-9ae5-5a38359dbda2",
  "1014bc27-e5b0-4fe3-abb8-5d93bc507fdc",
  "05f88e9a-4581-4095-8149-cc8557ee8262",
  "095a64ef-3ca7-41ed-857d-27e3b9ea6af6",
  "db96f904-7441-41b1-bb3e-33af3eeb3e17",
  "e00c1576-be16-4eb5-b8e1-3785d330ec76",
  "c83c8e7f-7026-414e-b74a-457c28ba19e2",
  "541f6421-56e1-40c2-9e59-24b60e9720d3",
  "b0e877f8-2ba1-499c-a922-8b4a71b3c941",
  "f3cfd270-efbe-4bb3-b2c3-93e1d9ccf86b",
  "52de5366-ac7b-403d-87c9-05b55c9c8269",
  "2bc2a96c-b1fa-41a9-9b98-10f4efdeb59f",
  "e3a1cf0e-6fa5-4a7c-99f8-a3a20a511955",
  "5fa612fc-8912-44d1-9129-7c2aa40fb245",
  "73e26b1d-869c-4d66-9785-a40e30486934",
  "e84d2051-2628-4ece-be9b-439a8182b04d",
  "29f7119b-0148-4216-8dde-228811348f4b",
  "e39bf86c-4144-4ac4-ac5c-4d81a173924f"
]
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50, module_ids_list)
    for get_one_id in get_batch_ids:
        find_process(get_one_id)
    # find_process("6cbf57db-ee2e-4965-8b71-d661d56e9932")
