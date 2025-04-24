import random

import MetersphereUtils


def report_data(id):
    list_object = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_and_unrun_cases_report_ids3(id)
    return  list_object


if __name__ == '__main__':
    # 输入用例id
    #报告用例id，正在执行时
    all_report_id="654dde97-7617-4c16-b4c3-6a63382dced3"
    # all_report_id="e49e1876-4792-4e0f-9b3f-577fca386f49"
    list_object = report_data(all_report_id)
    get_list=[]
    for get_one in list_object:
        get_tmp={"id":str(get_one["id"]),"userId":str(get_one["userId"]),"reportId":str(get_one["reportId"]),"name":str(get_one["name"])}
        print(str(get_tmp) +",")
        get_list.append(get_tmp)
    bool_is=True
    # bool_is=False
    if bool_is==False:
        #用例id
        rerun_list=[

        ]
        result=MetersphereUtils.rerun_report_mul_plan_test(all_report_id,rerun_list)
        print(result)
