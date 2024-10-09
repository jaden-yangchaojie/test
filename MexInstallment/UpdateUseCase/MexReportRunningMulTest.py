import MetersphereUtils


def report_data(id):
    list_object = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_report_ids2(id)
    return  list_object


if __name__ == '__main__':
    # 输入用例id
    #报告用例id，正在执行时
    # all_report_id="6904a6f4-0e51-4f41-a0b1-a10c902f2c71"
    all_report_id="ab6a7393-ac5a-4f26-92ab-96ab02372932"
    list_object = report_data(all_report_id)
    get_list=[]
    for get_one in list_object:
        get_tmp={"id":str(get_one["id"]),"userId":str(get_one["userId"]),"reportId":str(get_one["reportId"]),"name":str(get_one["name"])}
        print(get_tmp)
        get_list.append(get_tmp)
    print(get_list)

    rerun_list= [{'id': '7c3e4e5b-bee2-471f-bef8-4514ee57bcd2', 'userId': 'admin', 'reportId': '34971522-16cd-4e39-ae1b-bfeefcf5252d', 'name': '普通交易&MSI&MCI，第1期账期，第2期账期无DQ，第3账期无DQ(5种取值方式s1\\s2\\s3\\s4bal\\s5 100），正常场景（覆盖s2、s4、s5,公式推导s1是取不到的）'}
        ,{'id': '25da8814-5116-4dec-9b76-d46e3fb33485', 'userId': 'admin', 'reportId': '8f4ee202-6761-485c-bc9a-0f6783ded847', 'name': '第1期账期，第2期账期-部分还款->DQ->完成最小还款（出账有息费税），第3期账期DQ&完成最小还款,第4期无DQ'}
                 ,{'id': '93d89894-665d-4ac0-9555-6dab56f317fc', 'userId': 'admin', 'reportId': 'c45917b7-dced-4815-ae11-173d9312323a', 'name': '第1期账期，第2期账期DQ之后&完成最小还款 （出账有息费税），第3期账期完成最小还款出账'}
                 ,{'id': 'f077ff3a-d161-46d8-a040-1545bbc7d130', 'userId': 'admin', 'reportId': 'dd29b853-dc91-4eb5-9c24-e3d19fc06ce0', 'name': 'copy_MSI已出账还款（多笔多期）-多笔已出账&未完成最小还款&DQ_1b9c'}
                 ,{'id': 'c2d4c90f-eaf4-4676-9c8d-8f9e65b27941', 'userId': 'admin', 'reportId': '4ec0893f-c97b-4dbd-b248-96b19eac9ffd', 'name': 'copy_已出账退款（多笔多期）-多笔已出账&部分还款&DQ_13e2'}
                 ,{'id': 'd4a189aa-661f-4f79-9088-d3d7effe944b', 'userId': 'admin', 'reportId': '1eafba1a-5753-44a7-98c0-9c4942588082', 'name': 'copy_普通交易&MSI&MCI，第1期未完成最小还款，第2期未完成最小还款（部分还款）_e045'}]

    result=MetersphereUtils.rerun_report_mul_plan_test(all_report_id,rerun_list)
    print(result)
