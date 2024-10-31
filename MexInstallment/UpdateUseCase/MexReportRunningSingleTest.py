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
    all_report_id="446ddb23-7915-434b-a363-c24fa06fd342"
    # get_result=MetersphereUtils.stop_report_single_plan_test(all_report_id)
    # print(get_result)
    list_object = report_data(all_report_id)
    for get_one in list_object:
        get_tmp={"id":str(get_one["id"]),"userId":str(get_one["userId"]),"reportId":str(get_one["reportId"]),"name":str(get_one["name"])}
        print(get_tmp)
    #查看单个用例情况
    get_tmp= \
    {'id': '7d210c66-e4f1-43d0-a34f-b505cb9f802e', 'userId': 'admin',
     'reportId': 'cb3f57f6-c3ff-4c8c-b178-fe47099fe377', 'name': 'copy_小于100金额无分期_3f03'}
    id=get_tmp["id"]
    user_id=get_tmp["userId"]
    sub_report_id=get_tmp["reportId"]
    #执行用例
    result=MetersphereUtils.rerun_report_single_plan_test(all_report_id,id,sub_report_id,user_id)
    print(result)
    #查看执行用例进度
    for i in range(0,100):
        sleep(30)
        MexReportRunningStepDetail.running_process(sub_report_id)

