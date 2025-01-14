import datetime

from MetersphereInterface import MetersphereUtils


#批量修改任务id和其他参数用例

def get_batch_report_id(get_id):
    get_batch_ids = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_and_unrun_and_success_cases_report_ids4(get_id)
    return get_batch_ids


def find_process(id):
    get_content = MetersphereUtils.get_test_plan_report_id_get_content(id)
    createTime=get_content['createTime']
    endTime=get_content['endTime']
    print(get_content["name"])
    elasped_time=endTime-createTime
    print("耗时："+str(elasped_time/1000) +"秒 ~~= "+str(elasped_time/1000/60) +"分"  )



if __name__ == '__main__':
    # 输入用例id
    get_list_id = get_batch_report_id("86188735-a267-4635-821f-25223174038a")
    for get_one_id in get_list_id:
        find_process(get_one_id)
    # get_list_id = get_batch_report_id("0f24039d-e152-45f2-80f3-de63e62ea936")
    # for get_one_id in get_list_id:
    #     find_process(get_one_id,keyword)

    # find_process("6cbf57db-ee2e-4965-8b71-d661d56e9932")
