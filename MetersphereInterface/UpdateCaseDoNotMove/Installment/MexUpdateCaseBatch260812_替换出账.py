import json
import re

from jsonpath import jsonpath

from MetersphereInterface import MetersphereUtils

is_updated = 0

def only_find(get_data, insert_hash_tree_data):
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:

        if str(get_data["path"])=="/backoffice/dfl/credit/statement/create":
            print(str(get_data["path"]))
            get_body = get_data["body"]
            # hash_tree=get_data["hashTree"]
            # get_data=insert_hash_tree_data
            index=get_data["index"]
            if isinstance(insert_hash_tree_data, dict):
                insert_hash_tree_data.keys()-dict(get_data).keys()
                tmp_d_list=list(get_data.keys() - insert_hash_tree_data.keys())
                print(tmp_d_list)
                for get_one in list(tmp_d_list):
                    del get_data[get_one]

            for key in list(insert_hash_tree_data.keys()):
                get_data[key] = insert_hash_tree_data[key]
            get_data["index"]=index
            global is_updated
            is_updated = 1
            print("chuli chuzhang had to process")


    if get_data["type"] == "LoopController" and get_data["enable"] == True and str(get_data["whileController"]).count("${statementDate}")>0:
        is_updated = 1
        print("chuli LoopController had to process")
        get_data["enable"] = False

    if get_data["type"] == "scenario" and get_data["enable"] == True:
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            only_find(subScenario, insert_hash_tree_data)


def fibonacci_handler(result, insert_hash_tree_data):
    hashTree = result["hashTree"]
    only_find(result, insert_hash_tree_data)
    result["hashTree"] = hashTree


def handler_process_data(id, insert_hash_tree_data):
    global is_updated
    is_updated = 0

    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    # todo

    fibonacci_handler(result, insert_hash_tree_data)

    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]
    # get_daa=json.dumps(get_post_data)

    if is_updated == 1:
        print("need to update")
        get_info_udpate = MetersphereUtils.update_scenario_detail(get_post_data)
        print(get_info_udpate)
    else:
        print("no need to update")


if __name__ == '__main__':
    # 输入用例id

# [
#   "0ae6b422-e949-4234-9834-4edb6e8933f1"
# ]
#     [
#         "cbc96a31-21b0-4dce-a38d-a12bbf73b3a4"
#     ][
    #   "3525be45-280a-4937-97a0-62d562c1ae10"
    # ][
    #   "c77a8494-2d51-4b3f-b2a7-5f84ae3dc8c4"
    # ][
    #   "6c1181e2-fc18-4f32-9f6e-55fc03564e27"
    # ][
    #   "dfb80a28-0645-4e14-94e0-758ba9e6da79"
    # ][
    #   "1837c75c-0d19-4e2c-aa69-1bd3e2c00736",
    #   "3ee4e78a-4c82-4597-a45a-5a441a66458a",
    #   "1163100c-b1a6-441e-aef3-26a6a617cf28",
    #   "bad907bb-2742-4ab7-a31a-b47821c3640e"
    # ][
    #   "34e574c2-3094-4e5c-a0db-3411101d1b9c"
    # ][
    #   "4dcb57f3-cd8d-4038-9742-c1c8b6605e63"
    # ][
    #   "f9b54a47-fe1a-4198-b283-4f81f2e55f6d"
    # ][
    #   "798441f2-8099-487e-97a9-8c0fec0b98ea"
    # ]

    # 输入用例id
    module_id =[
  "61fce67c-e7eb-456f-bad5-5928e58493bf",
  "b97464ea-b5b0-41a5-b4f3-3bb5478c9592",
  "f305c94e-1ae3-4a76-854e-a6df6c110ad5",
  "1a1b1a1d-0261-4a33-9ebb-85c5bc557618",
  "25cd044d-3006-4b4d-834f-8cd71b9b1af6",
  "8b9ff580-bc56-4c35-86a3-f24fdd6f321c"
]
    get_ids =MetersphereUtils.get_batch_ids(1, 50,module_id)
    # for get_id in get_ids:
    #     handler_process(get_id)
    insert_detail_id = "340f5a63-f25d-4920-940a-6963ac1b32d1"
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(
        insert_detail_id) if insert_detail_id.isdigit() else insert_detail_id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    result['referenced'] = 'REF'
    insert_hash_tree_data = result
    # copy_5_14五期账单case14，边界天数89，duebucket3，多笔还款pending-》duebucket4，多笔还款posting，DQ回退成功（先退回DQ1、2，再回退DQ3）_1ce0
    # copy_第三期用例9.1，溢缴款=》出账，交易&换卡=》出账，DQ_2d33
    #copy_4_1四期账单case1,还款S1最小还款-》还款S2的最小还款变无DQ-》再次DQ_51ba
    # get_ids=["79b003c0-4992-4902-83ae-a22f9e44dee4","d803e6f3-c27d-4fa2-a404-e4b1c71cae5f","ab9caae0-1fa7-4f11-b09d-31ec44086151"]
    for get_id in get_ids:
        handler_process_data(get_id, insert_hash_tree_data)