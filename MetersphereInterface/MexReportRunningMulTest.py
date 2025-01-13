import MetersphereUtils


def report_data(id):
    list_object = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_and_unrun_cases_report_ids3(id)
    return  list_object


if __name__ == '__main__':
    # 输入用例id
    #报告用例id，正在执行时
    # all_report_id="6904a6f4-0e51-4f41-a0b1-a10c902f2c71"
    all_report_id="aadf47dc-04c6-4e1b-a2b9-46296cbf3a47"
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
            {'id': 'a6ec5405-3b95-4c51-9ace-092bcbae7b6b', 'userId': 'admin',
             'reportId': '8c2dbc5e-5e19-4e40-b08c-dd134160e95f', 'name': '3期DQ180+,有未入账利息关闭合约不能关闭'},
            {'id': 'da9fda86-23ab-43ae-a325-916775e00e96', 'userId': 'jaden.yang',
             'reportId': 'ac166711-6f71-4d04-9152-a7c409a1822f', 'name': '多笔-混合交易类型，第1期无交易，第2期所有交易'},
        ]


        result=MetersphereUtils.rerun_report_mul_plan_test(all_report_id,rerun_list)
        print(result)
