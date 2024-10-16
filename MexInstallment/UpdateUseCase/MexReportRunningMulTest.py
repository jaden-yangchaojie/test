import MetersphereUtils


def report_data(id):
    list_object = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_report_ids2(id)
    return  list_object


if __name__ == '__main__':
    # 输入用例id
    #报告用例id，正在执行时
    # all_report_id="6904a6f4-0e51-4f41-a0b1-a10c902f2c71"
    all_report_id="fa636d8a-a8ca-4dcb-91ef-0f1410bd8daf"
    list_object = report_data(all_report_id)
    get_list=[]
    for get_one in list_object:
        get_tmp={"id":str(get_one["id"]),"userId":str(get_one["userId"]),"reportId":str(get_one["reportId"]),"name":str(get_one["name"])}
        print(get_tmp)
        get_list.append(get_tmp)
    # print(get_list)

    rerun_list= [
        {'id': '6c786bd6-2ded-483c-93a7-c3479c6df356', 'userId': 'admin',
         'reportId': 'f4085c79-d95d-4c61-a5a0-f5c30a74d9b4',
         'name': '3期DQ61-90,DQ61d->85d->89d->90d，不能purchase\\换卡'},{'id': '2e9693eb-619e-4248-976c-89c6a8685d98', 'userId': 'admin', 'reportId': '1c155a8a-431b-4d65-9383-6c5a12e0e8d2', 'name': '3期DQ1-60,blockcodeD001-》D002,D001还款未post，D002做post'},
        {'id': '174070a6-23bc-497b-af85-cb68212fb059', 'userId': 'admin',
         'reportId': '7f4853d4-343c-4e3e-8e0e-6fee99dd5385',
         'name': '3期DQ61-90,blockcodeD004-》完成最小还款再次进入DQ，按dqday为1'},{'id': '2e9693eb-619e-4248-976c-89c6a8685d98', 'userId': 'admin', 'reportId': '1c155a8a-431b-4d65-9383-6c5a12e0e8d2', 'name': '3期DQ1-60,blockcodeD001-》D002,D001还款未post，D002做post'},{'id': '04b324a8-56fc-46c6-a259-9da94b22f43a', 'userId': 'admin', 'reportId': '738bcdca-6b2a-455d-bf4e-2278d14c7463', 'name': '多笔部分退款&逾期-重要'}
    ,{'id': '84847221-5d1b-491c-a115-ca726531b77b', 'userId': 'jaden.yang', 'reportId': 'e7846265-d83b-4a3e-9323-3569242bf0e1', 'name': '3期已出账&部分还款&逾期'}
    ]

    result=MetersphereUtils.rerun_report_mul_plan_test(all_report_id,rerun_list)
    print(result)
