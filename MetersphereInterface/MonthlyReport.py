import random

import jsonpath

import MetersphereUtils


def report_data(id):
    list_object = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_and_unrun_cases_report_ids3(id)
    # list_object = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_and_unrun_and_success_cases_report_ids7(id)

    return  list_object
true=True
null=None

if __name__ == '__main__':
    # 输入用例id
    #报告用例id，正在执行时
    # get_list_object=MetersphereUtils.get_test_plan_report_list("11406dc7-8340-401f-813f-3511a97d3fbb","墨西哥信用卡相关用例（账单/分期/营销/贷款",1,20)
    get_list_object = MetersphereUtils.get_test_plan_report_list("11406dc7-8340-401f-813f-3511a97d3fbb",
                                                                 "交易回归测试-", 1, 50)

    get_report_ids=[]

    for get_one  in get_list_object:
        if get_one["passRate"] is not None and float(get_one["passRate"])>float(0.5):
                print(get_one["passRate"])
                get_report_ids.append(get_one["id"])
    get_list = []
    print("data times run :"+str(len(get_report_ids)))
    print("------------------")
    for get_report_id in get_report_ids:
        list_object = report_data(get_report_id)
        for get_one in list_object:
            # if str(get_one["reportId"]) in report_ids:
            get_tmp={"id": str(get_one["id"]), "userId": str(get_one["userId"]), "reportId": str(get_one["reportId"]),
                       "name": str(get_one["name"]), "caseId": str(get_one["caseId"]),'modulePath':get_one['modulePath']}
            # if str(get_tmp).count("五期")>0:
            #     print(str(get_tmp) +",")
            print(str(get_tmp) + ",")
            get_list.append(get_tmp)
    print("总共多少个："+str(len(get_list)))
    total_times={}
    for get_one in get_list:
        if get_one["caseId"] in list(total_times.keys()):
            get_case_id=get_one["caseId"]

            get_map=total_times[get_case_id]
            get_times=get_map["time"]
            get_times=get_times+1
            get_map["time"]=get_times
            total_times[get_case_id]=get_map
        else:
            total_times[get_one["caseId"]]={"time":1,"name":get_one["name"],"userId":get_one["userId"],'modulePath':get_one['modulePath']}

    print(total_times)

    sorted_dict = sorted(total_times.values(), key=lambda item:item['time'],reverse=True)
    print(sorted_dict)
    for get_one in sorted_dict:
        print(get_one)


