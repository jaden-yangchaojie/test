import json

from ColInstallment import ColScenarioHandler
from MexInstallment import MetersphereUtils
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
    keyword="11110011000058961401"
    get_list_id = get_batch_report_id("adb017d1-00ae-49a8-b2cb-29ccad4ccdb5")
    for get_one_id in get_list_id:
        find_process(get_one_id,keyword)
    # find_process("6cbf57db-ee2e-4965-8b71-d661d56e9932")