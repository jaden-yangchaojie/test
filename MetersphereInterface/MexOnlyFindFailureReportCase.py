from MetersphereInterface import MetersphereUtils


#批量修改任务id和其他参数用例

def get_batch_report_id(get_id):
    get_batch_ids = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_report_ids(get_id)
    return get_batch_ids


def find_process(id,keyword):
    get_content = MetersphereUtils.get_test_plan_report_id_get_content(id)
    if str(get_content).count(keyword)>0:
        print(get_content["name"])


if __name__ == '__main__':
    # 输入用例id
    #要找的keyword
    # keyword="13130011000019075040"
    keyword = "13130011000019165494"
    get_list_id = get_batch_report_id("0c76e475-6562-4d3f-aef7-36633896f40b")
    for get_one_id in get_list_id:
        find_process(get_one_id, keyword)
    get_list_id = get_batch_report_id("0f24039d-e152-45f2-80f3-de63e62ea936")
    for get_one_id in get_list_id:
        find_process(get_one_id,keyword)

    # find_process("6cbf57db-ee2e-4965-8b71-d661d56e9932")
