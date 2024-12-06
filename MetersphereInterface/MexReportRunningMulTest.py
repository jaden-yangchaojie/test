import MetersphereUtils


def report_data(id):
    list_object = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_report_ids2(id)
    return  list_object


if __name__ == '__main__':
    # 输入用例id
    #报告用例id，正在执行时
    # all_report_id="6904a6f4-0e51-4f41-a0b1-a10c902f2c71"
    all_report_id="ceaf223b-3073-4056-b81b-9f87ca3fde4b"
    list_object = report_data(all_report_id)
    get_list=[]
    for get_one in list_object:
        get_tmp={"id":str(get_one["id"]),"userId":str(get_one["userId"]),"reportId":str(get_one["reportId"]),"name":str(get_one["name"])}
        print(str(get_tmp) +",")
        get_list.append(get_tmp)
    # print(get_list)
    #
    rerun_list= [
        {'id': 'e64bff51-db05-4e83-9f24-b39b65db17ed', 'userId': 'admin',
         'reportId': '3e44c771-db52-46e4-aca3-aeeedd067b1c',
         'name': '第1账期提前退款部分本金，出账之后AMP可以创建成功大于5w，ADJ_INS>0,分期分1期），失败'},


    ]

    result=MetersphereUtils.rerun_report_mul_plan_test(all_report_id,rerun_list)
    print(result)
