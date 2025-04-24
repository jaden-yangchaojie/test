import datetime
import json

from MetersphereInterface import MetersphereUtils

insert_data_new_st = []
insert_data_st_process_detail = []
num1 = 0
num2 = 0


def get_batch_report_id(get_id):
    list_case_report_ids, list_case_case_ids = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_and_unrun_and_success_cases_report_ids5(
        get_id)
    return list_case_report_ids, list_case_case_ids


def report_only_find(get_data):
    if get_data["type"] == "scenario":
        children = get_data['children']
        for subScenario in children:
            report_only_find(subScenario)

    if get_data["type"] == 'HTTPSamplerProxy':
        # 场景名称
        # if get_data["label"]=='app purchase auth' and get_data["totalStatus"]=="ERROR":
        if get_data["label"] == '查询最新已出账单':
            step_id = get_data['stepId']
            get_step_id_result = MetersphereUtils.report_step_id(step_id)

            # name=get_step_id_result["label"]
            url = get_step_id_result["url"]
            responseResult = get_step_id_result["responseResult"]
            body = responseResult["body"]
            get_need_update_body = json.loads(body)
            data = get_need_update_body["data"]
            global insert_data_new_st
            insert_data_new_st.append({"$.status": get_need_update_body["status"], "$.data.dueDate": data['dueDate'],
                                       "$.data.statementDate": data['statementDate'],
                                       "$.data.graceDate": data["graceDate"],
                                       "$.data.billingCycle": data["billingCycle"],
                                       "$.data.minPayment.amountInMnrUnits": data["minPayment"]["amountInMnrUnits"]})

            print(insert_data_new_st)

        if get_data["label"] == '查询账单过程数据':
            step_id = get_data['stepId']
            get_step_id_result = MetersphereUtils.report_step_id(step_id)

            # name=get_step_id_result["label"]
            url = get_step_id_result["url"]
            responseResult = get_step_id_result["responseResult"]
            body = responseResult["body"]
            get_need_update_body = json.loads(body)
            data = get_need_update_body["data"]
            global insert_data_st_process_detail
            insert_data_st_process_detail.append(
                {"$.data.minPayment.calculateResult": data['minPayment']["calculateResult"]}
                )
            print(insert_data_st_process_detail)


def only_find(get_data, new_insert_data_new_st, new_insert_data_st_process_detail):
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:

        if str(get_data["path"]).count("/backoffice/dfl/credit/statement/settled") > 0:
            global num1
            get_data['hashTree'][2]['jsonPath'] = new_insert_data_new_st[num1]
            num1 = num1 + 1
        if str(get_data["path"]).count("/backoffice/dfl/credit/statement/processDetail") > 0:
            global num2
            get_data['hashTree'][0]['jsonPath'] = new_insert_data_st_process_detail[num2]
            num2 = num2 + 1

    if get_data["type"] == "scenario" and get_data["enable"] == True and 'referenced' in get_data and (
            get_data['referenced'] == "Copy" or get_data['referenced'] == 'Created'):
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            only_find(subScenario, new_insert_data_new_st, new_insert_data_st_process_detail)


def fibonacci_handler(result, new_insert_data_new_st, new_insert_data_st_process_detail):
    hashTree = result["hashTree"]
    only_find(result, new_insert_data_new_st, new_insert_data_st_process_detail)
    result["hashTree"] = hashTree


def data_process(id, replace_id):
    get_content = MetersphereUtils.get_test_plan_report_id_get_content(id)
    global insert_data_new_st
    global insert_data_st_process_detail
    global num1
    global num2
    insert_data_new_st = []
    insert_data_st_process_detail = []
    num1 = 0
    num2 = 0

    content_str = get_content['content']
    content = json.loads(content_str)
    steps = content["steps"][0]
    report_only_find(steps)
    print("++++++++")
    print(insert_data_new_st)
    print(insert_data_st_process_detail)
    # scenario_id =MetersphereUtils.get_scenario_detail_id_by_search_id(replace_id) if id.isdigit() else id
    new_insert_data_new_st = []
    new_insert_data_st_process_detail = []

    for i, get_one_dict in enumerate(insert_data_new_st):
        tmp = []
        for k, v in dict(get_one_dict).items():
            tmp.append({'valid': True, 'expect': str(v), 'expression': str(k), 'enable': True,
                        'description': (str(k) + "expect: " + str(v)), 'type': 'JSON', 'option': 'REGEX'})
        new_insert_data_new_st.append(tmp)
    for i, get_one_dict in enumerate(insert_data_st_process_detail):
        tmp = []
        for k, v in dict(get_one_dict).items():
            tmp.append({'valid': True, 'expect': str(v), 'expression': str(k), 'enable': True,
                        'description': (str(k) + "expect: " + str(v)), 'type': 'JSON', 'option': 'REGEX'})
        new_insert_data_st_process_detail.append(tmp)

    data = MetersphereUtils.get_scenario_detail_all_info(replace_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)

    fibonacci_handler(result, new_insert_data_new_st, new_insert_data_st_process_detail)

    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]

    get_info_udpate = MetersphereUtils.update_scenario_detail(get_post_data)
    print(get_info_udpate)

    # print(content)


if __name__ == '__main__':
    # 输入用例id
    all_report_id = "bd48be62-8aca-4d5c-8a47-bc1027e746a7"

    # repalce_id = "37065b9a-9022-4c22-bf09-45d1516aadcd"

    list_case_report_ids, list_case_case_ids = get_batch_report_id(all_report_id)
    case_report_id_map_into_case_case_id = []
    if len(list_case_report_ids) == len(list_case_case_ids):
        for i, get_one_id in enumerate(list_case_report_ids):
            case_report_id_map_into_case_case_id.append({get_one_id:list_case_case_ids[i]})

        print(case_report_id_map_into_case_case_id)

        for get_one in case_report_id_map_into_case_case_id:
            for case_report_id,case_case_id in dict(get_one).items():

                data_process(case_report_id, case_case_id)
