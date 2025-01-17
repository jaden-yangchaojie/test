import MetersphereUtils


def report_data(id):
    list_object = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_and_unrun_cases_report_ids3(id)
    return  list_object


if __name__ == '__main__':
    # 输入用例id
    #报告用例id，正在执行时
    # all_report_id="6904a6f4-0e51-4f41-a0b1-a10c902f2c71"
    all_report_id="b11d9176-acd2-43ff-8da3-0a9b539d8c88"
    list_object = report_data(all_report_id)
    get_list=[]
    for get_one in list_object:
        get_tmp={"id":str(get_one["id"]),"userId":str(get_one["userId"]),"reportId":str(get_one["reportId"]),"name":str(get_one["name"])}
        print(str(get_tmp) +",")
        get_list.append(get_tmp)
    # bool_is=True
    bool_is=False
    if bool_is==False:
        rerun_list=[
            {'id': 'e6faa34b-fe8e-4e36-be42-99c63ec23d58', 'userId': 'admin',
             'reportId': 'dd02e007-1ba0-4372-b23e-d94d927e4f8a', 'name': 'copy_用户卡block A001_ca79'},
            {'id': 'c1086f94-a726-415d-b3e4-8b7d66cc4f16', 'userId': 'admin',
             'reportId': '136cc8df-2ef2-47de-8e60-46685466e1c6', 'name': 'copy_墨西哥创建分期3期_c45f'},
            {'id': '6d3be1f1-b7fc-469d-9557-5f4f8dd150f8', 'userId': 'admin',
             'reportId': 'c23f1e5d-14fe-45d4-88d4-d5bf105f30db', 'name': 'copy_发生逾期DQ不能分期_b548'},
            # {'id': 'f591a830-e677-4c19-bf58-640fef5a39f1', 'userId': 'admin',
            #  'reportId': 'abe4f887-97ae-4bfc-8661-efa04965e21e', 'name': 'DQ & end_bal<100'},
        ]

        result=MetersphereUtils.rerun_report_mul_plan_test(all_report_id,rerun_list)
        print(result)
