import MetersphereUtils


def report_data(id):
    list_object = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_and_unrun_cases_report_ids3(id)
    return  list_object


if __name__ == '__main__':
    # 输入用例id
    #报告用例id，正在执行时
    # all_report_id="6904a6f4-0e51-4f41-a0b1-a10c902f2c71"
    all_report_id="b8cce8e7-5b87-4654-b9a4-22df62b7c0b1"
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
             {'id': 'c85944c1-b4ee-4f25-b899-6fe92577a7db', 'userId': 'admin',
              'reportId': 'e12591b4-e250-41ea-acfd-cbc7dca7ee58',
              'name': '已出账单_dueDate前还款+graceDate前还款+gradeDate后'},
             {'id': '31ecb29c-83f7-41ea-a918-655d65a6c6d2', 'userId': 'admin',
              'reportId': '9ee3ff4b-61d6-437b-af1f-5bc2a480fd52', 'name': '已出多期账单_优先还款(转普通还款)+明细还款'},
             {'id': '8b92e858-630c-4e8b-a0ae-8c747486755e', 'userId': 'admin',
              'reportId': '1b157cb4-9304-4655-8893-2b68476d8b04', 'name': '已出账单=0_优先还款(转普通还款)+明细还款'},
             {'id': '7044179e-ccc5-4e64-89f3-75070168b329', 'userId': 'admin',
              'reportId': 'e7889bf7-9973-40c2-bcbe-306504d94e53',
              'name': '已出账单_优先还款(无转普通还款)+普通还款+明细还款'},
             {'id': 'b5961ac2-f075-44a2-9106-2a49b1304b90', 'userId': 'admin',
              'reportId': 'f595d049-1d56-444b-a584-20a7cb423acd', 'name': '已出账单_优先还款(转普通还款)+明细还款'},
             {'id': '6fc6dca4-c5e4-4f9f-a614-45265462f9a5', 'userId': 'admin',
              'reportId': '11b0299a-4ac2-4606-a314-5f046450aea6', 'name': '首期账单已出_dueDate前payment1小于最小还款'},

          ]

        result=MetersphereUtils.rerun_report_mul_plan_test(all_report_id,rerun_list)
        print(result)
