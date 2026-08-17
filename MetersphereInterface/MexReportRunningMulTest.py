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
            {'id': '1aad1b3b-6268-4cf2-8f31-2fa8145c02f6', 'userId': 'admin',
             'reportId': 'b91ce964-4008-4a38-9423-db7636dc8dbe',
             'name': '第三期用例2.2，滞纳金direct收费，出账》完成最小还款，无DQ-》出账-》DQ-》溢缴款',
             'caseId': '6f98e529-38b2-45de-a8f1-9859f8cd5c4e'},


        ]

        result=MetersphereUtils.rerun_report_mul_plan_test(all_report_id,rerun_list)
        print(result)
 
