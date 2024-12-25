import MetersphereUtils


def report_data(id):
    list_object = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_and_unrun_cases_report_ids3(id)
    return  list_object


if __name__ == '__main__':
    # 输入用例id
    #报告用例id，正在执行时
    # all_report_id="6904a6f4-0e51-4f41-a0b1-a10c902f2c71"
    all_report_id="5f29023f-0fb9-4d06-a19e-971ebd350ac0"
    list_object = report_data(all_report_id)
    get_list=[]
    for get_one in list_object:
        get_tmp={"id":str(get_one["id"]),"userId":str(get_one["userId"]),"reportId":str(get_one["reportId"]),"name":str(get_one["name"])}
        print(str(get_tmp) +",")
        get_list.append(get_tmp)
    # bool_is=True
    bool_is=False
    if bool_is==False:
        rerun_list=\
            [
                {'id': 'd4ff64ad-52be-42d2-a126-c6238005774e', 'userId': 'admin', 'reportId': '5d02dfcf-4df7-4603-8748-bd6baf1c9b04', 'name': 'copy_普通交易&MSI&MCI，第1期完成最小还款，第2期完成最小还款_49c4'},
                {'id': 'e4b7d796-8343-409f-8357-35c3fa6a283e', 'userId': 'admin',
                 'reportId': 'c2450911-ba4f-41ac-9069-d030d4ba9621',
                 'name': 'STC101_普通交易&MSI&MCI，第1期完成最小还款，第2期完成最小还款'},
                {'id': '52b91b2e-c94d-4ef1-b1bd-4e4d524a2430', 'userId': 'admin',
                 'reportId': '5c593687-7a2b-4e76-843f-a9f45ba37d19', 'name': 'STC003_MSI创建分期_合约存在且期数存在'},
                {'id': '038570b4-9ec1-470e-aac2-e85ee5724b7e', 'userId': 'admin',
                 'reportId': '9509f351-abd8-4bcb-bd85-a7be3814f301',
                 'name': '第1期账期，第2账期部分还款->DQ(出账有息费税），第3期账期部分还款->DQ(出账有息费税),第4期完成最小还款'},
                {'id': 'db20b2aa-68e1-4c12-8d43-3c1c7dd66e87', 'userId': 'admin',
                 'reportId': '5a04a28c-85af-4d0b-b6e9-993eda1c497b',
                 'name': 'copy_分期6期已出账，完成最小还款之后下期手动退款取消分期,本金同时入账_67d7'},
                {'id': '62dd0d7f-dfab-43bb-b62a-2376841242b3', 'userId': 'admin',
                 'reportId': '6a09ace8-64ee-4ed6-87ac-f72ac83b25ef',
                 'name': 'copy_已出账还款（多笔多期）-多笔已出账&未完成最小还款&DQ_a557'},
                {'id': 'b59db5d4-ed63-4386-819e-3d881df256cd', 'userId': 'admin',
                 'reportId': '7b25eb86-c2ab-4069-91f1-fad31c4c8211',
                 'name': 'copy_第一次DQ，完成最小还款，再次DQ终止，不连续不会终止_430c'},
                # {'id': 'b59db5d4-ed63-4386-819e-3d881df256cd', 'userId': 'admin',
                #  'reportId': '7b25eb86-c2ab-4069-91f1-fad31c4c8211',
                #  'name': 'copy_第一次DQ，完成最小还款，再次DQ终止，不连续不会终止_430c'},
                # {'id': 'bde73ee7-515c-4f89-8aca-301317091898', 'userId': 'admin',
                #  'reportId': '36eef0aa-d58b-4487-847d-7bc0ad44a72f',
                #  'name': '第1期账期，第2期账期DQ~第7期账期DQ&DQbucket4终止'},
                # {'id': 'e4b7d796-8343-409f-8357-35c3fa6a283e', 'userId': 'admin',
                #  'reportId': 'c2450911-ba4f-41ac-9069-d030d4ba9621',
                #  'name': 'STC101_普通交易&MSI&MCI，第1期完成最小还款，第2期完成最小还款'},
                # {'id': 'b1ee419d-742d-4b4e-a3e8-29d5b9071382', 'userId': 'admin',
                #  'reportId': '99cb3162-4c88-46ed-bea5-2ac9c1911182', 'name': 'copy_MSI-DQ-bucket=4分期终止_f9cc'},
                # {'id': '52b91b2e-c94d-4ef1-b1bd-4e4d524a2430', 'userId': 'admin',
                #  'reportId': '5c593687-7a2b-4e76-843f-a9f45ba37d19', 'name': 'STC003_MSI创建分期_合约存在且期数存在'},
                # {'id': 'a81dbf35-4978-4970-bd91-6675a68f4d1c', 'userId': 'dong.wang',
                #  'reportId': 'f39026ff-c349-4940-9dcb-50c5d5b986d5', 'name': 'MCI_分期提前还款1期_下个账期提前还款2期'},
                # {'id': '2550b98b-40ff-4fa5-af0f-4647242f25fe', 'userId': 'admin',
                #  'reportId': '72f6a67a-dfc9-4e20-bd22-a9efc1e3a888',
                #  'name': 'copy_普通交易&MSI&MCI，第1期未完成最小还款，第2期未完成最小还款（部分还款）_e045'},
                # {'id': '038570b4-9ec1-470e-aac2-e85ee5724b7e', 'userId': 'admin',
                #  'reportId': '9509f351-abd8-4bcb-bd85-a7be3814f301',
                #  'name': '第1期账期，第2账期部分还款->DQ(出账有息费税），第3期账期部分还款->DQ(出账有息费税),第4期完成最小还款'},
                # {'id': 'd4ff64ad-52be-42d2-a126-c6238005774e', 'userId': 'admin',
                #  'reportId': '5d02dfcf-4df7-4603-8748-bd6baf1c9b04',
                #  'name': 'copy_普通交易&MSI&MCI，第1期完成最小还款，第2期完成最小还款_49c4'},

         ]

        result=MetersphereUtils.rerun_report_mul_plan_test(all_report_id,rerun_list)
        print(result)
