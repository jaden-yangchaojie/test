import datetime
import json

import jsonpath

from MetersphereInterface import MetersphereUtils

insert_data_list = []

insert_data_num = 0


def get_batch_report_id(get_id):
    list_case_report_ids, list_case_case_ids = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_and_unrun_and_success_cases_report_ids5(
        get_id)
    return list_case_report_ids, list_case_case_ids


def report_only_find(get_data):
    global insert_data_list
    if get_data["type"] == "scenario":
        children = get_data['children']
        for subScenario in children:
            report_only_find(subScenario)


    if get_data["type"] == 'HTTPSamplerProxy':
        # 场景名称
        if get_data["label"] == '查询账单过程数据':
            step_id = get_data['stepId']
            get_step_id_result = MetersphereUtils.report_step_id(step_id)

            # name=get_step_id_result["label"]
            url = get_step_id_result["url"]
            responseResult = get_step_id_result["responseResult"]
            assertions = responseResult["assertions"]
            body = responseResult["body"]
            get_need_update_body = json.loads(body)
            data = get_need_update_body["data"]
            tmp = []
            #需要配置自己配置
            tmp.append(
                {"$.data.minPayment.calculateResult": data['minPayment']["calculateResult"]})

            insert_data_list.append(tmp)


# 更新自动化case
def only_find(get_data, new_insert_data_mul_list):


    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:

        if str(get_data["path"]).count("/backoffice/dfl/credit/statement/processDetail") > 0:
            for i, get_one in enumerate(get_data['hashTree']):
                if get_one['type'] == 'Assertions':

                    global insert_data_num
                    get_data['hashTree'][i]['jsonPath'] = new_insert_data_mul_list[insert_data_num]
                    insert_data_num = insert_data_num + 1

    if (get_data["type"] == "scenario" and get_data["enable"] == True):
        # and 'referenced' in get_data and (get_data['referenced'] == "Copy" or get_data['referenced'] == 'Created')):
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            only_find(subScenario, new_insert_data_mul_list)


def update_case_handler(result, new_insert_data_mul_list):
    hashTree = result["hashTree"]
    only_find(result, new_insert_data_mul_list)
    result["hashTree"] = hashTree


def data_process(case_report_id, case_case_id):
    get_content = MetersphereUtils.get_test_plan_report_id_get_content(case_report_id)

    global insert_data_list
    global insert_data_num
    insert_data_list = []
    insert_data_num = 0
    content_str = get_content['content']
    content = json.loads(content_str)
    steps = content["steps"][0]
    # case的报告id
    report_only_find(steps)
    print("++++++++")
    print(insert_data_list)
    new_insert_data_mul_list = []

    for i, get_one_list in enumerate(insert_data_list):
        tmp = []
        # 插入http断言
        for get_one in (get_one_list):
            for k, v in dict(get_one).items():
                tmp.append({'valid': True, 'expect': str(v), 'expression': str(k), 'enable': True,
                'description': (str(k) + "expect: " + str(v)), 'type': 'JSON', 'option': 'REGEX'})

        print(tmp)
        new_insert_data_mul_list.append(tmp)
    # 更新用例数据
    data = MetersphereUtils.get_scenario_detail_all_info(case_case_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)

    update_case_handler(result, new_insert_data_mul_list)

    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]

    get_info_udpate = MetersphereUtils.update_scenario_detail(get_post_data)
    print(get_info_udpate)



if __name__ == '__main__':
    # 输入用例id
    # all_report_id = "bd48be62-8aca-4d5c-8a47-bc1027e746a7"
    all_report_id = "b2b088c2-9722-480d-9155-6832ffb88caf"
    # repalce_id = "37065b9a-9022-4c22-bf09-45d1516aadcd"

    list_case_report_ids, list_case_case_ids = get_batch_report_id(all_report_id)
    case_report_id_map_into_case_case_id = []
    if len(list_case_report_ids) == len(list_case_case_ids):
        for i, get_one_id in enumerate(list_case_report_ids):
            case_report_id_map_into_case_case_id.append({get_one_id: list_case_case_ids[i]})

        data_process("d5ba2aea-d8e9-4b78-bd4d-f262804e1b8d", "fb2242a3-fccc-4c5d-9869-78e781f47fe0")
        # case_report_id_map_into_case_case_id=[]
        # for get_one in case_report_id_map_into_case_case_id:
        #     for case_report_id,case_case_id in dict(get_one).items():
        #         data_process(case_report_id, case_case_id)
