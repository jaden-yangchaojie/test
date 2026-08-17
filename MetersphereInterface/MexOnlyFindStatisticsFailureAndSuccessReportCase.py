import datetime

from MetersphereInterface import MetersphereUtils


# 批量修改任务id和其他参数用例




global global_var

global_var = 0

UAT=0

def find_process(i,get_one_id, list_case_case_ids, modulePaths):
    get_content = MetersphereUtils.get_test_plan_report_id_get_content(get_one_id)
    createTime = get_content['createTime']
    endTime = get_content['endTime']
    print(get_content["name"])

    global global_var
    global UAT
    elasped_time = endTime - createTime
    global_var = global_var + elasped_time
    print("耗时：" + str(elasped_time / 1000) + "秒 ~~= " + str(elasped_time / 1000 / 60) + "分")

    print("global_var：" + str(global_var) )

    if str(get_content["name"]).count("UAT")>0:
        UAT=elasped_time+UAT
        print("目前UAT：" + str(UAT))



if __name__ == '__main__':
    # 输入用例id
    report_id="15439fa8-7119-4171-9c65-6baa17485c1b"
    list_case_report_ids, list_case_case_ids, modulePaths = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_and_unrun_and_success_cases_report_ids6(report_id)

    for i,get_one_id in enumerate(list_case_report_ids):
        try:
            find_process(i,get_one_id, list_case_case_ids[i], modulePaths[i])
        except :
            print("+++++++++++")
