from time import sleep

import MetersphereUtils
from UpdateUseCase import MexReportRunningStepDetail


def report_data(id):
    list_object = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_and_unrun_cases_report_ids3(id)
    return  list_object


if __name__ == '__main__':
    # 输入用例id
    #报告用例id，正在执行时
    # all_report_id="6904a6f4-0e51-4f41-a0b1-a10c902f2c71"
    all_report_id="ab6a7393-ac5a-4f26-92ab-96ab02372932"
    list_object = report_data(all_report_id)
    for get_one in list_object:
        get_tmp={"id":str(get_one["id"]),"userId":str(get_one["userId"]),"reportId":str(get_one["reportId"]),"name":str(get_one["name"])}
        print(get_tmp)

    get_tmp= \
        {'id': '25da8814-5116-4dec-9b76-d46e3fb33485', 'userId': 'admin',
         'reportId': '8f4ee202-6761-485c-bc9a-0f6783ded847',
         'name': '第1期账期，第2期账期-部分还款->DQ->完成最小还款（出账有息费税），第3期账期DQ&完成最小还款,第4期无DQ'}
    id=get_tmp["id"]
    user_id=get_tmp["userId"]
    sub_report_id=get_tmp["reportId"]

    result=MetersphereUtils.rerun_report_single_plan_test(all_report_id,id,sub_report_id,user_id)
    print(result)
    for i in range(0,100):
        sleep(30)
        MexReportRunningStepDetail.running_process(sub_report_id)
    #
