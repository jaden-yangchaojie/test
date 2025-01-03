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
    module_ids_list= \
        [
            "6a652fe4-18b1-4dad-9490-aadb5c9dfc2b",
            "31981617-83e2-4c47-846e-426696259567",
            "2e1be7ed-3cb4-44b8-b4b0-7423669a2897",
            "cca06efa-ab32-4b31-9bfb-37d245cfe8cf",
            "ebb09a4a-3f80-4f9c-9510-4b15ab96b971",
            "fd14e1ad-a3b8-4e27-b0ef-051b922ab232",
            "537e301a-0b49-4124-9e03-266fa60c5983",
            "497e7bd4-8dbf-4b05-b38b-a1afa8d940c1",
            "a1fa0e02-2478-4e15-a4d1-056cd9237a09"
        ]
    #  'environmentJson': '{}',ref  ,copy没有
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50, module_ids_list)
    for get_one_id in get_batch_ids:
        find_process(get_one_id)
    # find_process("6cbf57db-ee2e-4965-8b71-d661d56e9932")
