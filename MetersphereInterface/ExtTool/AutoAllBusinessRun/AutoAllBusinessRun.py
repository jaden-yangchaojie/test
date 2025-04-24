import datetime
import json
import math
import time

import jsonpath

from MetersphereInterface import MetersphereUtils


    # print(content)
def clear_id_list(page_no, page_size, plan_id, priorit_list):

    get_scenario_id_list, item_count, page_count = MetersphereUtils.test_plan_scenario_list1(page_no, page_size,
                                                                                                plan_id,
                                                                                                priorit_list=priorit_list)
    names = jsonpath.jsonpath(get_scenario_id_list, "$..name")
    print(names)
    id_list = jsonpath.jsonpath(get_scenario_id_list, "$..id")

    for i in range(page_no+1,page_count+1):
        # page_no = page_no + 1
        get_scenario_id_list_p1, item_count, page_count = MetersphereUtils.test_plan_scenario_list1(i,
                                                                                                    page_size,
                                                                                                    plan_id,
                                                                                                    priorit_list=priorit_list)
        tmp = jsonpath.jsonpath(get_scenario_id_list_p1, "$..id")
        for get_tmp_case_id in tmp:
            id_list.append(get_tmp_case_id)
    return id_list


def handler_case_id(page_no, page_size, plan_id, priorit_list):
    get_scenario_id_list_p1, item_count, page_count = MetersphereUtils.test_plan_scenario_list1(page_no, page_size,
                                                                                                plan_id,
                                                                                                priorit_list=priorit_list)
    names = jsonpath.jsonpath(get_scenario_id_list_p1, "$..name")
    print(names)
    case_id_list = jsonpath.jsonpath(get_scenario_id_list_p1, "$..caseId")
    for i in range(page_no+1,page_count+1):
        # page_no = page_no + 1
        get_scenario_id_list_p1, item_count, page_count = MetersphereUtils.test_plan_scenario_list1(i,
                                                                                                    page_size,
                                                                                                    plan_id,
                                                                                                    priorit_list=priorit_list)
        tmp = jsonpath.jsonpath(get_scenario_id_list_p1, "$..caseId")
        for get_tmp_case_id in tmp:
            case_id_list.append(get_tmp_case_id)
    return list(set(case_id_list))

if __name__ == '__main__':
    # 参考metersphere页面上的测试工具
    #https://stori-sdc-cn.feishu.cn/wiki/Ce4mwidhridw9mkSGiGc12jTnmb
    business_plan_ids = {
        "plan_id": "b0990c64-622e-45ee-934b-9d23cc763e15", "name": "【QA-TEST】营销Cashback&redemption全量回归",
         "env_id": "343ca1b7-f080-4f5d-ad65-867e3308f2b7", "project_id": "11406dc7-8340-401f-813f-3511a97d3fbb",
         "split_times_run": 7
        # "61d77374-656d-4008-ae9d-00220fc7d251": "【QA-test】墨西哥分期新规则"
        # ,                 "2312279c-5747-4e83-ab81-c9a9ae106df6": "【QA-Test】定时跑-墨西哥信用卡只含账单回归测试计划new"
                         }

    # insert_plan_id="63ae9097-5cf1-46fa-b596-574dcb67a43b"
    insert_plan_id="3b0960d8-6773-49a2-8b55-a64128955b54"
    MetersphereUtils.test_plan_scenario_case_relevance(case_ids=["fdfa4f0d-0c04-4866-a2c2-6c9f56d2054e"],plan_id=insert_plan_id)
    #清空数据
    # case_id_list_p0_p1_p2_p3 = clear_id_list(1, 50, insert_plan_id,
    #                                          ["P0", "P1", "P2", "P3"])
    # MetersphereUtils.test_plan_scenario_case_batch_delete(case_id_list_p0_p1_p2_p3)

    #制定规则拆分跑
    # for plan_id in business_plan_ids:
    #     page_no = 1
    #     page_size = 50
    #     case_id_list_p0=handler_case_id(page_no,page_size,plan_id,["P0"])
    #     print(page_no)
    #     print(page_size)
    #     case_id_list_p1_p2_p3 = handler_case_id(page_no, page_size, plan_id, ["P1","P2","P3"])
    #     list(set(case_id_list_p1_p2_p3))
    #     MetersphereUtils.test_plan_scenario_case_relevance(case_ids=case_id_list_p0)
    #     get_num=len(case_id_list_p1_p2_p3)
    #     split_times_run=3
    #     avg_num=int(get_num/split_times_run)
    #     insert_into_case_id=[]
    #     date2 = datetime.datetime.strptime("2025-01-10", "%Y-%m-%d")
    #     now_date=datetime.datetime.now()
    #     get_days=(now_date-date2).days+2
    #     get_ls=get_days % (split_times_run if split_times_run*avg_num==get_num else split_times_run+1)
    #     start=avg_num*get_ls
    #     end=avg_num*(get_ls+1)
    #     for i,case_id in enumerate(case_id_list_p1_p2_p3):
    #         if i>=start and i<=end:
    #             insert_into_case_id.append(case_id_list_p1_p2_p3[i])
    #     MetersphereUtils.test_plan_scenario_case_relevance(case_ids=insert_into_case_id)


