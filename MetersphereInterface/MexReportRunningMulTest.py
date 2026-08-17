import random
import time

import jsonpath

import MetersphereUtils


def report_data(id):
    list_object = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_and_unrun_cases_report_ids3(id)
    # list_object = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_and_unrun_and_success_cases_report_ids7(id)

    return  list_object
true=True
null=None

if __name__ == '__main__':
    # 输入用例id
    #报告用例id，正在执行时
    all_report_id="461ad4e2-8f29-47a3-a77f-af32a6c4ab9a"
    list_object = report_data(all_report_id)
    get_list=[]

    for get_one in list_object:
        # if str(get_one["reportId"]) in report_ids:
        get_tmp={"id": str(get_one["id"]), "userId": str(get_one["userId"]), "reportId": str(get_one["reportId"]),
                   "name": str(get_one["name"]), "caseId": str(get_one["caseId"])}
        # if str(get_tmp).count("五期")>0:
        #     print(str(get_tmp) +",")
        print(str(get_tmp) + ",")
        get_list.append(get_tmp)
    # bool_is=True
    bool_is=False
    if bool_is==False:
        #用例id
        rerun_list=[
            {'id': '3eebe301-631c-4920-bd21-3be2b7d5a97d', 'userId': 'admin',
             'reportId': '6403cb2f-b140-4cb7-9c13-46550b614769', 'name': 'copy_八期账单，duebucket6账单文件_173e',
             'caseId': '2c2d3dba-6a0c-402e-8ff5-e67c715d960f'},
            {'id': 'ac553cd0-3ade-4fea-ba17-11798745ef1e', 'userId': 'admin',
             'reportId': 'e8127515-741c-491a-b5bf-1375c73fefbc',
             'name': 'copy_二期账单，1期有争议费，DQ产生late fee后还款_0976',
             'caseId': '4a00329a-c13c-4c5a-bb3e-195e1b57f0d5'},
            {'id': '3b2fc57f-88f4-499a-b1da-e26572b566e5', 'userId': 'admin',
             'reportId': '7e35fac9-0be8-457e-9e71-b0940a9ec07c', 'name': 'copy_二期账单，1期有争议费，完成最小还款_9756',
             'caseId': 'acfeb89e-7e6e-42ed-a79d-329d27081595'},
        ]

        result=MetersphereUtils.rerun_report_mul_plan_test(all_report_id,rerun_list)
        print(result)
 
