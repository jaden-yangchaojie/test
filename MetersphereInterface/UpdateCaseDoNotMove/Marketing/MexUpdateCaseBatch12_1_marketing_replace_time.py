import json
import re

from jsonpath import jsonpath

from MetersphereInterface import MetersphereUtils

# 只改签约、和产品
# STC103 ->  (subproductCode)AFFINITY03
# STC104 ->  (subproductCode)AFFINITY04
# 跑之前必须打开 前置检查-服务可用性验证
is_updated = 0



def only_find(get_data, insert_hash_tree_data):
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
        global is_updated
        if str(get_data["path"]).count("/api/admin/system/faketime") > 0 and is_updated != 1:
            print(str(get_data["path"]))
            tmp = get_data['body']
            tmp["raw"] = '{"time": "' + str(insert_str_data) + '"}'
            get_data['body']=tmp

            is_updated = 1
            print("had to process......")

    if get_data["type"] == "scenario" and get_data["enable"] == True:
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            only_find(subScenario, insert_hash_tree_data)


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
    # num_test_ser=len(result['hashTree'])
    # for i, get_one in enumerate(result['hashTree']):
    #     if  i+1<num_test_ser and str(result['hashTree'][i + 1]['name']).count("用户注册") > 0:
    #         ready_update_time_hashtree=result['hashTree'][i]['hashTree'][0]
    #         if str(ready_update_time_hashtree['path']).count("/api/admin/system/faketime") > 0 and result['hashTree'][i]['name'].count("系统时间")>0:
    #             result['hashTree'][i]["name"]="系统时间-"+str(insert_str_data)
    #             tmp =ready_update_time_hashtree['body']
    #             tmp["raw"]='{"time": "'+str(insert_str_data)+'"}'
    #             ready_update_time_hashtree['body']=tmp
    #             result['hashTree'][i]['hashTree'][0]=ready_update_time_hashtree
    #             is_updated = 1
    #             print("had to process......")
    fibonacci_handler(result,insert_str_data)
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
# {"ad23325c-292e-4c98-b0eb-adb5b65beab5":"账期限额","time":""},
# {"32f262dc-16fe-41f7-abfd-abb52755077a":"账期限次","time":"2024-01-28 05:39:59"},
# {"49372faa-695a-4add-aa5e-b7a92d4fa86b":"账期限额限次","time":"2024-01-28 06:39:59"},
# {"3653b516-2c90-4922-a409-3072a47c5665":"账期固定金额限次","time":"2024-01-28 07:39:59"},
# {"00c67fd5-26ba-40a8-857b-0446a3325cf9":"区间限次","time":"2024-01-28 01:39:59"},
# {"1a507c10-ee53-40d5-a345-d3fc485e14c4":"区间限额","time":"2024-01-28 03:39:59"},
# {"dbab2217-17cf-4568-bca4-97478f835319":"活动限额","time":"2024-01-28 08:39:59"},
# {"751eba06-a992-469b-a76f-879581fe12bc":"活动限次","time":"2024-01-28 09:39:59"},
# {"32b769a2-330a-44e5-8e4c-c9627ca014b6":"活动限额限次","time":"2024-01-28 08:39:59"},
# {"02a5e826-191d-46ec-b129-6580ccfbdd82":"活动固定金额限次","time":"2024-01-28 10:39:59"},
#
# {"9467c339-b1eb-4c86-9034-45df6c26d14c":"用户维度返现有效期","time":""},
# {"cfded6de-8bb6-4e98-8939-71060a550581":"用户维度限额","time":""},
# {"15c2fae4-1a3a-4b39-b816-7c2c1e775282":"自然月限额限次","time":"2024-01-28 11:39:59"},

        {"ad23325c-292e-4c98-b0eb-adb5b65beab5": "账期限额", "time": "2024-01-28 13:39:59"},
    ]
    for get_one in dir_dict_data_list:
        # print(get_one)
        for k,v in get_one.items():
            print(k)
            print(v)
            if str(k).count("time")>0:
                exit()
            get_ids = MetersphereUtils.get_batch_ids(1, 50, [k])
            insert_str_data=get_one["time"]
            for get_id in get_ids:
                handler_process_data(get_id,insert_str_data)



#
# module_ids = [
#         # "3f646930-dc33-4329-b497-e2fd6182c3bd",总目录
#
#         "bf111fb8-f316-4a68-83fd-02e684479c7a",
#
#         "58bf522b-2632-426b-bb54-8325807a9f96",
#
#         "34873885-38a9-4cc2-af68-fda6a164452d",
#
#         "5b3618f1-87d5-443b-8112-d0cb656724ce",
#
#         "23dc3fed-e2a9-4f3f-8cbc-64dde5c9d488",
#
#         "7c4c140c-24fd-4160-9cb6-d544c891535d",
#
#         "e1949d36-fcd7-4329-bccd-7ee08c680174",
#
#         "ac885d9e-1077-4f2b-8618-389edb5a69c7",
#
#         "04aaf7bd-892e-4693-a300-3a5defcc10b7", 二级目录
#         "7ac954ee-91b6-4727-b97c-7b6a9fdeb7f2",
#         "b2fa4d8f-060f-4b75-b1ed-f231291f4c9c",
#
#         "2d18b60f-d9f4-4350-9f71-8f47af280d43",
#
#         "75674695-3926-4843-b950-511aa6c998b0",
#
#         "d1846ff5-de8e-46c8-8966-a02b6ed544f3",
#
#         "5a051b3c-fa96-4a6d-a6f9-5ae6c502c8a9",
#
#         "f6a947be-1886-4405-8a14-7bd07ba3bee5",
#
#         "249853ab-6860-4726-9670-447142620f38"
#     ]


    # 输入用例id
    # module_ids =[
    #     "b4689eaa-875c-455e-89e5-ea57fb2b6e50"
    # ]
    # dir_dict_data_list = [{"bf111fb8-f316-4a68-83fd-02e684479c7a": "2024-01-02 12:00:00"},
    #
    #                       {"58bf522b-2632-426b-bb54-8325807a9f96": ""},
    #
    #                       {"34873885-38a9-4cc2-af68-fda6a164452d": ""},
    #
    #                       {"5b3618f1-87d5-443b-8112-d0cb656724ce": ""},
    #
    #                       {"23dc3fed-e2a9-4f3f-8cbc-64dde5c9d488": ""},
    #
    #                       {"7c4c140c-24fd-4160-9cb6-d544c891535d": ""},
    #
    #                       {"e1949d36-fcd7-4329-bccd-7ee08c680174": ""},
    #
    #                       {"ac885d9e-1077-4f2b-8618-389edb5a69c7": ""},
    #
    #                       {"7ac954ee-91b6-4727-b97c-7b6a9fdeb7f2": ""},
    #                       {"b2fa4d8f-060f-4b75-b1ed-f231291f4c9c": ""},
    #
    #                       {"2d18b60f-d9f4-4350-9f71-8f47af280d43": ""},
    #                       {"75674695-3926-4843-b950-511aa6c998b0": ""},
    #                       {"d1846ff5-de8e-46c8-8966-a02b6ed544f3": ""},
    #                       {"5a051b3c-fa96-4a6d-a6f9-5ae6c502c8a9": ""},
    #                       {"f6a947be-1886-4405-8a14-7bd07ba3bee5": ""},
    #                       {"249853ab-6860-4726-9670-447142620f38": ""}
    #                       ]