import MetersphereUtils


def report_data(id):
    list_object = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_report_ids2(id)
    return  list_object


if __name__ == '__main__':
    # 输入用例id
    #报告用例id，正在执行时
    # all_report_id="6904a6f4-0e51-4f41-a0b1-a10c902f2c71"
    all_report_id="446ddb23-7915-434b-a363-c24fa06fd342"
    list_object = report_data(all_report_id)
    get_list=[]
    for get_one in list_object:
        get_tmp={"id":str(get_one["id"]),"userId":str(get_one["userId"]),"reportId":str(get_one["reportId"]),"name":str(get_one["name"])}
        print(str(get_tmp) +",")
        get_list.append(get_tmp)
    # print(get_list)

    rerun_list= [
        {'id': '1d02f898-56af-4fd4-b27d-7c9ca15e55f3', 'userId': 'admin',
         'reportId': 'fd7905e0-2ab2-40f4-98ac-ea4fd7390d7f', 'name': 'copy_分期之后退款不影响已有分期_138d'},
        {'id': '1a8292fc-305a-4442-8dd4-1a8cb0fb01ad', 'userId': 'admin',
         'reportId': '489d9e4d-7043-430b-a01d-b9afe24fed15', 'name': 'copy_用户卡block A001_ca79'},
        {'id': 'dad03849-239f-4c0e-a1cd-93959011b45e', 'userId': 'admin',
         'reportId': '66cfdcd1-23f8-408e-bd48-b39d8b6cc2f0', 'name': 'copy_试算总本金、税、利息3~12期_fcc0'},
        {'id': '3f80f0db-6210-4f91-934e-27fbc2a2451f', 'userId': 'admin',
         'reportId': '668e2616-941f-40f5-8161-a05e94f76c7f', 'name': 'copy_分期咨询正常查询_d423'},
        {'id': '3f522007-1488-4cac-93d4-c36d62928608', 'userId': 'admin',
         'reportId': '01678512-1ccc-47a9-9794-b2255c6cb7f0', 'name': 'copy_账单列表分期入账_e2b7'},
        {'id': '2377b9d9-5315-4457-85f4-f4854af9bb74', 'userId': 'admin',
         'reportId': 'f850293a-87df-4aae-becb-d8d1fc8a3899', 'name': 'STC003_MSI创建分期_合约存在且期数存在'},
        {'id': '2b520da8-16b8-47f6-9794-d1e1629dc199', 'userId': 'admin',
         'reportId': '3145debe-7464-45ef-a792-0d759cb55be7', 'name': 'DQ & end_bal>100 & min_pmt <100'},
        {'id': 'ae403a5e-7aee-4398-9380-d52fe5ea3d64', 'userId': 'admin',
         'reportId': '8959a66e-94e7-448c-879b-cfc6f0b5e376',
         'name': '第1期账期，第2期账期DQ（出账有息费税），第3期账期完成最小还款'},
        {'id': 'c85b742d-c8f2-49c1-8409-0106dd445944', 'userId': 'admin',
         'reportId': 'aaa275ee-aff7-4033-9f4a-a5171b338f7b',
         'name': 'copy_MSI已出账退款（多笔多期）-多笔已出账&全额退款_8458'},
    ]

    result=MetersphereUtils.rerun_report_mul_plan_test(all_report_id,rerun_list)
    print(result)
