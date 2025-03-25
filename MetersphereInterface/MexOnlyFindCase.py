import json

from jsonpath import jsonpath

from MetersphereInterface import MetersphereUtils


#批量修改任务id和其他参数用例




def find_process(id):
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_single_detail_all_info(scenario_id)
    get_data_main=data.get("data")
    # print(get_data_main['description'])
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)

    get_list = []
    only_find(result, get_list)

tmp_set=set([])
def only_find(get_data, dds):
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
        # get_path = get_data["path"]
        # if str(get_data).count("/api/admin/system/faketime")>0 :
        #     if str(get_data).count("__timeShift")>0:
        #         print(get_data["body"])
            # get_list=jsonpath(get_data, "$..jsonPath")
        if str(get_data).count("v1.0/credit/cards")>0:
            # body=get_data["body"]['raw']
            # print(json.loads(body)["product"]["productCode"])
            # if str(body).count("BALANCE_INQUIRY")>0:
                print("++++++++++++")

        # print(len(get_list))

        # if str(get_data).count("REFUND"):
            # # get_list = get_data["body"]["kvs"]
            # # if get_list[0]["value"]'' :
            # if "DQ_STATUS_UPDATE" in str(get_data) :
            #     print(get_data["body"]["kvs"][1])
            #     # if ("{{" in str(get_data) or  "{ {"in str(get_data) or  "{  {"in str(get_data)):
            #     #     print("yes++++")

            # print("++++++++")

    if get_data["type"] == "JDBCSampler" and get_data["enable"] == True:
        get_list = jsonpath(get_data, "$..regex")
        # if len(get_list) > 0:
        #     for get_one in get_list:
        #         if len(get_one) > 0:
        #             print("db断言："+str(len(get_one)) )

    if get_data["type"] == "scenario" and get_data["enable"] == True :
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            only_find(subScenario, dds)

if __name__ == '__main__':
    # 输入用例id
    module_ids_list= [
        "9aa6c422-d881-4fd5-952c-2c4ad5896ee2"
        # "e169ce21-2d1a-44d9-a501-16b6db059a67"
        ]
#         [
#   "9aa6c422-d881-4fd5-952c-2c4ad5896ee2"
# ]
     # 'environmentJson': '{}',ref  ,copy没有
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 100, module_ids_list)
    # get_batch_ids=["6d59c1cb-6ab2-4668-b3aa-a306712e82a9"]
    for get_one_id in get_batch_ids:
        find_process(get_one_id)
    # find_process("6cbf57db-ee2e-4965-8b71-d661d56e9932")
    # print(tmp_set)