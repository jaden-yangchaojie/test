import datetime
import json

import jsonpath

from MetersphereInterface import MetersphereUtils

insert_data_list = []

insert_data_num = 0
#需要修改str(get_data['label']).count("联合查询")

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

    if get_data["type"] == "JDBCSampler" :
        # and str(get_data['label']).count("联合查询"):

        step_id = get_data['stepId']
        get_step_id_result = MetersphereUtils.report_step_id(step_id)
        print(get_step_id_result)
        responseResult = get_step_id_result["responseResult"]
        assertions = responseResult["assertions"]
        body = responseResult["body"]
        if len(str(body)) > 0:
            get_rows = str(body).replace("\nOutput variables by position:\n", "").split("\n")
            all_get_header_field_name_list = []
            # 全字段做断言
            for get_field_name in get_rows[0].split("\t"):
                all_get_header_field_name_list.append(get_field_name)
            # 需要修改看取哪些部分字段做断言
            get_header_field_name_list = ["sum_type", "type", "sub_type"]
            tmp = []
            for i, get_fileds_values in enumerate(get_rows):
                if i != 0 :
                    get_fileds_values_split = str(get_fileds_values).split("\t")
                    if len(get_fileds_values_split) > 0:
                        for j, get_fileds_value in enumerate(get_fileds_values_split):
                            if all_get_header_field_name_list[j] in get_header_field_name_list and len(str(get_fileds_value))>0:
                                tmp.append({str(get_header_field_name_list[j]) + "_" + str(i ):str(get_fileds_value)})

            insert_data_list.append(tmp)
            # print(insert_data_list)




# 更新自动化case
def only_find(get_data, new_insert_data_mul_list):
    if get_data["type"] == "JDBCSampler" and get_data["enable"] == True :
        # and str(get_data["query"]).count(
        #     "corebankingA1.cc_pmt_payment_allocation.account_id") \
        #     and str(get_data["name"]).count("联合查询"):
        print()
        for i, get_one in enumerate(get_data['hashTree']):
            if get_one['type'] == 'Assertions':

                global insert_data_num
                #new_insert_data_mul_list对应第几个sql list
                inser_one=new_insert_data_mul_list[insert_data_num]

                get_one["jsr223"] = inser_one
                get_data['hashTree'][i] = get_one

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
    new_insert_data_mul_list = []

    for i, get_one_list in enumerate(insert_data_list):
        tmp = []

        # 插入sql接口
        for get_one in (get_one_list):
            for k,v in dict(get_one).items():
                tmp.append(
                    {'valid': True, 'jsrEnable': True, 'scriptLanguage': 'beanshell', 'enable': True, 'variable': str(k),
                     'type': 'JSR223', 'value': str(v), 'operator': '==',
                     'script': 'value = vars.get("' + str(k) + '");\nresult = "' + str(
                         v) + '".equals(value);\nif (!result){\n\tmsg = "assertion [" + value + " == \'' + str(
                         v) + '\']: false;";\n\tAssertionResult.setFailureMessage(msg);\n\tAssertionResult.setFailure(true);\n}',
                     'desc': "${" + str(k) + "} == '" + str(v) + "'"})
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

    # print(content)


if __name__ == '__main__':
    # 输入用例id

    all_report_id = "0ed59b31-5a05-4ee0-b8c7-d29310c2345b"

    list_case_report_ids, list_case_case_ids = get_batch_report_id(all_report_id)
    case_report_id_map_into_case_case_id = []
    if len(list_case_report_ids) == len(list_case_case_ids):
        for i, get_one_id in enumerate(list_case_report_ids):
            case_report_id_map_into_case_case_id.append({get_one_id: list_case_case_ids[i]})

        data_process("e99a5ce8-d797-4f10-a12a-c80ec9e6570d", "fb2242a3-fccc-4c5d-9869-78e781f47fe0")
        # case_report_id_map_into_case_case_id=[]
        # for get_one in case_report_id_map_into_case_case_id:
        #     for case_report_id,case_case_id in dict(get_one).items():
        #         data_process(case_report_id, case_case_id)
