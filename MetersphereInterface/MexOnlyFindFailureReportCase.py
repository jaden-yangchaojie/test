import sys

from MetersphereInterface import MetersphereUtils


#批量修改任务id和其他参数用例

def get_batch_report_id(get_id):
    get_batch_ids = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_and_unrun_and_success_cases_report_ids4(get_id)
    return get_batch_ids


def find_process(id,keyword):
    get_content = MetersphereUtils.get_test_plan_report_id_get_content(id)
    if str(get_content).count(keyword)>0:
        print(str(get_content["name"])+"+++++")
        # sys.exit()


if __name__ == '__main__':
    # 输入用例id
    #要找的keyword
    # keyword="13130011000019075040"
    keyword = "11110011000148893945"
    get_list_id = get_batch_report_id("949e124f-d294-4edd-be53-b1d0014f793c")
    for get_one_id in get_list_id:
        find_process(get_one_id, keyword)
    # get_list_id = get_batch_report_id("0f24039d-e152-45f2-80f3-de63e62ea936")
    # for get_one_id in get_list_id:
    #     find_process(get_one_id,keyword)

    # find_process("6cbf57db-ee2e-4965-8b71-d661d56e9932")
