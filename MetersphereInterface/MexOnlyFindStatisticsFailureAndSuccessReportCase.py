import datetime

from MetersphereInterface import MetersphereUtils


# 批量修改任务id和其他参数用例

def get_batch_report_id(get_id):
    get_batch_ids = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_and_unrun_and_success_cases_report_ids4(
        get_id)
    return get_batch_ids


global global_var

global_var = 0

UAT=0

def find_process(id):
    get_content = MetersphereUtils.get_test_plan_report_id_get_content(id)
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
    get_list_id = get_batch_report_id("fdefaeb4-f439-461e-a9ab-8a95bd13fd84")
    for get_one_id in get_list_id:
        find_process(get_one_id)
