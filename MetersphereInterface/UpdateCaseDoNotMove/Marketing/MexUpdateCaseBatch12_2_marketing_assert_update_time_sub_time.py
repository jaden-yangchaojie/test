import json
import re

from jsonpath import jsonpath

from MetersphereInterface import MetersphereUtils

is_updated = 0


def only_find(get_data, insert_str_data):
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:

        if str(get_data["path"]).count("/v1.0/credit/transactions/cashback") > 0 or str(get_data["path"]).count("/v1.0/credit/marketing/redemption/cashbacks") > 0 :
            jsonPath = get_data['hashTree'][0]['jsonPath']
            for i,get_one in enumerate(jsonPath):
                if get_one['enable']==True:
                    if str(get_one['expression']).count("$.data.activityList[0].effectiveTime")>0 or \
                        str(get_one['expression']).count("$.data.activityList[0].postTime")>0 or \
                        str(get_one['expression']).count("$.data.activityList[0].relatedTransactions[0].effectiveTime") > 0 or \
                            str(get_one['expression']).count("$.data.activityList[0].relatedTransactions[0].postTime") > 0:
                        if len(str(get_one["expect"]))>=10:
                            get_one["expect"]=str(get_one["expect"])[0:10]
                            get_one['description'] = str(get_one['expression'])+" "+str(get_one['option'])+": "+str(get_one["expect"])
                            jsonPath[i]=get_one
                            global is_updated
                            is_updated = 1
                            print("had to process......")
                        else:
                            print("assert no dayu 10")



    if get_data["type"] == "scenario" and get_data["enable"] == True:
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            only_find(subScenario, insert_str_data)


def fibonacci_handler(result, insert_str_data):
    hashTree = result["hashTree"]
    only_find(result, insert_str_data)
    result["hashTree"] = hashTree


def handler_process_data(id, insert_str_data):
    global is_updated
    is_updated = 0

    global pre_check_contract
    pre_check_contract = True
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    # todo

    fibonacci_handler(result, insert_str_data)
    # todo

    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]
    # get_daa=json.dumps(get_post_data)
    if is_updated == 1:
        print("had updated")
        get_info_udpate = MetersphereUtils.update_scenario_detail(get_post_data)
        print(get_info_udpate)
    else:
        print("no need to update")


if __name__ == '__main__':

    dir_dict_data_list = [
        {"id": "bf111fb8-f316-4a68-83fd-02e684479c7a", "name": "账期限额", "time": "2024-01-28 02:29:59"},
        # {"id":"58bf522b-2632-426b-bb54-8325807a9f96","name":"账期限次","time":""},
        # {"id":"34873885-38a9-4cc2-af68-fda6a164452d","name":"时间区间内限额","time":"2024-01-28 03:29:59"},
        # {"id":"5b3618f1-87d5-443b-8112-d0cb656724ce","name":"时间区间内限次","time":"2024-01-28 01:29:59"},
        # {"id":"23dc3fed-e2a9-4f3f-8cbc-64dde5c9d488","name":"新模型账期限额","time":"2024-01-28 04:29:59"},
        # {"id":"7c4c140c-24fd-4160-9cb6-d544c891535d","name":"新模型账期限次","time":"2024-01-28 05:29:59"},
        # {"id":"e1949d36-fcd7-4329-bccd-7ee08c680174","name":"新模型账期限次限额","time":"2024-01-28 06:29:59"},
        # {"id":"ac885d9e-1077-4f2b-8618-389edb5a69c7","name":"新模型账期固定金额限次","time":"2024-01-28 07:29:59"},
        #
        # {"id":"7ac954ee-91b6-4727-b97c-7b6a9fdeb7f2","name":"以签约时间为计算返现有效期","time":""},
        # {"id":"b2fa4d8f-060f-4b75-b1ed-f231291f4c9c","name":"以CL为返现额度","time":""},
        # {"id":"2d18b60f-d9f4-4350-9f71-8f47af280d43","name":"活动时间限额","time":"2024-01-28 08:29:59"},
        # {"id":"75674695-3926-4843-b950-511aa6c998b0","name":"活动时间限次","time":"2024-01-28 09:29:59"},
        # {"id":"d1846ff5-de8e-46c8-8966-a02b6ed544f3","name":"活动时间限额限次","time":"2024-01-28 08:29:59"},
        # {"id":"5a051b3c-fa96-4a6d-a6f9-5ae6c502c8a9","name":"活动时间固定金额限次","time":"2024-01-28 10:29:59"},
        # {"id":"f6a947be-1886-4405-8a14-7bd07ba3bee5","name":"自然月限额限次","time":"2024-01-28 11:29:59"},
        # {"id":"249853ab-6860-4726-9670-447142620f38","name":"根据签约范围添加活动返现资格","time":"2024-01-28 12:29:59"}
    ]

    for get_one in dir_dict_data_list:

        get_module_id = get_one["id"]
        get_ids = MetersphereUtils.get_batch_ids(1, 50, [get_module_id])
        for get_id in get_ids:
            handler_process_data(get_id, "")
# for get_one in dir_dict_data_list:
#     # print(get_one)
#     if len(str(get_one["time"]))<10:
#         continue
#     for k,v in get_one.items():
#         print(k)
#         print(v)
#         if str(k).count("time")>0:
#             continue
#         get_ids = MetersphereUtils.get_batch_ids(1, 50, [k])
#         insert_str_data=get_one["time"]
#         if len(str(insert_str_data))>0:
#             for get_id in get_ids:
#                 handler_process_data(get_id,insert_str_data)
