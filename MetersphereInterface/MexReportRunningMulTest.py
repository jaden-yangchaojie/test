import MetersphereUtils


def report_data(id):
    list_object = MetersphereUtils.get_test_plan_report_db_sce_failure_cases_and_unrun_cases_report_ids3(id)
    return  list_object


if __name__ == '__main__':
    # 输入用例id
    #报告用例id，正在执行时
    # all_report_id="6904a6f4-0e51-4f41-a0b1-a10c902f2c71"
    all_report_id="6978833b-d39f-426f-8487-e81d8a1f96c8"
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
            {'id': 'c61bfe29-842f-46c7-8f11-0d6bd4bdb0a1', 'userId': 'katherine.lv',
             'reportId': 'de305cc4-527e-48ac-8b4c-a39d2d85265c', 'name': '第二期用例5.3'},
            {'id': '8721129a-c8e3-4bcf-b2ab-ab3f4c38f666', 'userId': 'katherine.lv',
             'reportId': '25148a92-7dfb-4724-853c-5330c9fb9659', 'name': '第二期用例1.3'},
            {'id': '6f0ba53f-5789-4c8e-b75e-88114ad7dab7', 'userId': 'katherine.lv',
             'reportId': '14cd74d5-b490-46c4-8dcd-ba32111827ef', 'name': '第二期用例1.2'},
            {'id': 'c90ad769-2824-4499-9787-9efb4032fc89', 'userId': 'katherine.lv',
             'reportId': '2e06efdb-d719-4284-820c-a4249f6ef040', 'name': '第二期用例9.3'},
            {'id': 'a2b2413c-e9c5-4a44-8c04-d5da8967ab5f', 'userId': 'katherine.lv',
             'reportId': '283704be-595a-4b21-9c9f-25486a45e41a', 'name': '第二期用例13.1'},
            {'id': 'ea3db26b-5037-418c-9d21-4cc6ba07206a', 'userId': 'katherine.lv',
             'reportId': '90f9638a-65b2-414c-8330-67d6a80b72d3', 'name': '第二期用例2.3'},
            {'id': 'c2b1a524-7a2c-486d-a7fc-264a48de2cf2', 'userId': 'katherine.lv',
             'reportId': '194dc9b4-ce76-45f0-9a55-dc7a18d34b2d', 'name': '第二期用例1.1'},
            {'id': 'a0efa097-8f68-488e-bc1c-4c680c74a3b6', 'userId': 'katherine.lv',
             'reportId': '1580c0bf-dad6-47f6-a277-04152aa8e9d2', 'name': '第二期用例19.4'},
            {'id': 'f798c4a1-bd78-41fa-856c-09f4a0ff8839', 'userId': 'katherine.lv',
             'reportId': '1823b0c8-ebf8-4c57-8491-76d2b2415a18', 'name': '第二期用例6.1'},
            {'id': '6baa1879-8473-4b3f-887e-6cee8deb301a', 'userId': 'katherine.lv',
             'reportId': '71e246d5-aeb1-484a-9ba7-29801f973a9e', 'name': '第二期用例42.2'},
            {'id': 'fab37607-865a-45a6-9087-d62b97b1e610', 'userId': 'katherine.lv',
             'reportId': 'fe4e76b6-b581-4de0-a104-e7d8370cbf6c', 'name': '第二期用例14.1'},
            {'id': 'c89a983f-4b8b-4206-917f-f20361d92696', 'userId': 'katherine.lv',
             'reportId': 'a185f651-eae7-4b1b-9752-d4a8365e7b41', 'name': '第二期用例5.2'},
            {'id': 'a9e8fac3-1733-43e6-b56a-f77737afa3b7', 'userId': 'katherine.lv',
             'reportId': '907469c1-535c-4cd0-b52e-06ddfd14326e', 'name': '第二期用例10.3'},
            {'id': 'ed93f824-a342-484a-aa1c-78e504de3197', 'userId': 'katherine.lv',
             'reportId': 'c1179431-7b53-4a23-aa68-b5d10f7ace1c', 'name': '第二期用例5.1'},
            {'id': 'd4a8abae-5eb3-4caa-b07b-f870bb7c5264', 'userId': 'katherine.lv',
             'reportId': '881c85b5-cf85-4df8-b433-e11aa451922a', 'name': '第二期用例42.3'},
            {'id': '7f81dd32-8b53-417f-bd45-59bdffccdd71', 'userId': 'katherine.lv',
             'reportId': 'e33f6af6-8d3f-4a4d-ae10-29000cd01881', 'name': '第二期用例8.1'},
            {'id': '8dd6c209-65e1-4b41-9f38-40013346ef2c', 'userId': 'katherine.lv',
             'reportId': '9de6e914-4770-4d00-af11-7b99a563a288', 'name': '第二期用例7.1'},
            {'id': 'c7ae6a49-e8de-4397-b5bd-5727e19b6bb3', 'userId': 'katherine.lv',
             'reportId': 'e172ad24-1791-46f1-94cc-14f98308a52f', 'name': '第二期用例13.2'},
            {'id': 'bbe75c17-cd20-46d6-856c-5c0952d2a63e', 'userId': 'katherine.lv',
             'reportId': '78aa596f-8913-42a2-a799-85a00e366502', 'name': '第二期用例15.1'},
            {'id': 'aa3c3d28-cc53-4b9b-b693-f342d74f0d08', 'userId': 'katherine.lv',
             'reportId': '1ec26ac6-a290-445b-ace0-86285261fdab', 'name': '第二期用例10.2'},
            {'id': '53b2ba5c-3c1a-4a7d-8996-48503cef8165', 'userId': 'katherine.lv',
             'reportId': '72db6f4d-1676-4156-b466-2657a1adce1a', 'name': '第二期用例10.1'},
            {'id': 'a5c3a441-bb22-4f59-9a7a-383a90b5a041', 'userId': 'katherine.lv',
             'reportId': '9dee2b44-da15-4056-afa3-8a73767e8d98', 'name': '第二期用例16.1'},
            {'id': '6ecc73ce-cbec-4bfd-9b1d-3b4747e3a74d', 'userId': 'katherine.lv',
             'reportId': '6c733644-025e-4658-80e0-bf7fecd6346b', 'name': '第二期用例19.5'},
            {'id': 'd0780a44-795a-4768-88aa-5b538ea57cae', 'userId': 'katherine.lv',
             'reportId': '9f4fa972-df58-47ff-8233-4c4f2a0f5f0f', 'name': '第二期用例13.3'},
            {'id': '709dbf8e-ef07-42d7-ae81-8bbb208a94ba', 'userId': 'katherine.lv',
             'reportId': 'c400768c-6ef1-4928-8380-f3da40084fab', 'name': '第二期用例16.3'},
            {'id': '103cbb40-6755-4aeb-a246-38800969eb5b', 'userId': 'katherine.lv',
             'reportId': 'fa30854d-b718-4bb4-9391-5d6a3abee90a', 'name': '第二期用例9.2'},
            {'id': '1f8da392-9301-4b3b-9f66-83f8377d0839', 'userId': 'katherine.lv',
             'reportId': 'e490ef27-444d-41a2-87e8-455f80fa29d3', 'name': '第二期用例16.2'},
            {'id': '2674ab32-f749-4773-8a68-2969539a26eb', 'userId': 'katherine.lv',
             'reportId': 'f563fe32-398d-4d17-bc0e-a84a95c2a6df', 'name': '第二期用例12.1'},
            {'id': '1a958ace-e0e4-423d-abaf-7b10d18e61c6', 'userId': 'katherine.lv',
             'reportId': '049a8432-1ce2-4ba2-aa5d-2fb49f7683c9', 'name': '第二期用例2.2'},
            {'id': '06a02df1-a60b-4f85-add8-66292cef1727', 'userId': 'katherine.lv',
             'reportId': '08d9a379-e031-4b5a-93b0-050befa53a01', 'name': '第二期用例2.1'},

        ]


        result=MetersphereUtils.rerun_report_mul_plan_test(all_report_id,rerun_list)
        print(result)
