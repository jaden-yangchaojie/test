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
            {'id': '822c0f18-6b97-402d-a1b3-e6d45b341c7b', 'userId': 'admin',
             'reportId': 'ade973e1-d713-4173-b51a-570dd1011448',
             'name': '10期DQ91-180-还完所有欠款,账单日 还完所有欠款无入账的利息，关户关卡'},
            {'id': '4a8a8f56-d30c-424a-9cb6-63eb61f5a477', 'userId': 'admin',
             'reportId': '71d0213b-f4d3-40be-99f4-df69ff97e617',
             'name': '10期DQ91-180-还完所有欠款,非账单日 还完所有欠款但有未入账的利息，不关户不关卡'},
            {'id': 'a6ec5405-3b95-4c51-9ace-092bcbae7b6b', 'userId': 'admin',
             'reportId': '8c2dbc5e-5e19-4e40-b08c-dd134160e95f', 'name': '3期DQ180+,有未入账利息关闭合约不能关闭'},
            {'id': 'da9fda86-23ab-43ae-a325-916775e00e96', 'userId': 'jaden.yang',
             'reportId': 'ac166711-6f71-4d04-9152-a7c409a1822f', 'name': '多笔-混合交易类型，第1期无交易，第2期所有交易'},
            {'id': 'aa8b20ab-33c5-43fd-a611-e69ce4c40417', 'userId': 'admin',
             'reportId': 'e8015c85-d9d4-4332-b472-7ccecd67114f',
             'name': '3期DQ1-60,blockcode D001\\D002收取管理费，滞纳金'},
            {'id': 'f6d534d6-cd32-4109-aa73-b5e6695b8d4a', 'userId': 'admin',
             'reportId': '4ab378df-3002-4809-b712-316bfa909dbe',
             'name': '3期DQ61-90,blockcodeD004-》全额还款无DQ，按dqday为0'},
            {'id': 'f92d0a37-f956-4f4d-a818-67ff86fc11a3', 'userId': 'admin',
             'reportId': '2ae0ecd4-77c8-4679-929a-d96341270c64',
             'name': '10期DQ91-180,DQ91d->150d->180d，不能换卡,card block，不收取管理费、滞纳金，利息在其他90+用例看到'},
            {'id': 'e8aa14fb-581b-4c58-8454-733974e44a7c', 'userId': 'admin',
             'reportId': '141fafe1-fa91-4316-a10e-b31de555f784',
             'name': '3期DQ61-90,blockcodeD004-》完成最小还款再次进入DQ，按dqday为1'},
            {'id': '56e7bf7e-d430-4d3b-ac60-7bb7e8aca49b', 'userId': 'admin',
             'reportId': '1ee2905f-22ed-4e0c-a742-b7883c59265f',
             'name': '3期DQ1-60,blockcodeD001-》未完成最小还款-》完成最小还款，恢复dqdays为0  =》再进入DQ'},
        ]


        result=MetersphereUtils.rerun_report_mul_plan_test(all_report_id,rerun_list)
        print(result)
