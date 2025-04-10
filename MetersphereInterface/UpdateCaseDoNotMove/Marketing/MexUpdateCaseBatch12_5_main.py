from time import sleep

from MetersphereInterface import MetersphereUtils
from MetersphereInterface.UpdateCaseDoNotMove.Marketing import \
    MexUpdateCaseBatch12_2_marketing_assert_update_time_sub_time, MexUpdateCaseBatch12_4_data_campaigns_campaign_type

if __name__ == '__main__':

    dir_dict_data_list = [
        # {"id":"ad23325c-292e-4c98-b0eb-adb5b65beab5","name":"账期限额","time":"2024-01-28 13:39:59"},
        # {"id":"32f262dc-16fe-41f7-abfd-abb52755077a","name":"账期限次","time":"2024-01-28 05:39:59"},
        # {"id":"49372faa-695a-4add-aa5e-b7a92d4fa86b","name":"账期限额限次","time":"2024-01-28 06:39:59"},
        # {"id":"3653b516-2c90-4922-a409-3072a47c5665","name":"账期固定金额限次","time":"2024-01-28 07:39:59"},
        # {"id":"00c67fd5-26ba-40a8-857b-0446a3325cf9","name":"区间限次","time":"2024-01-28 01:39:59"},
        # {"id":"1a507c10-ee53-40d5-a345-d3fc485e14c4","name":"区间限额","time":"2024-01-28 03:39:59"},
        # {"id":"dbab2217-17cf-4568-bca4-97478f835319","name":"活动限额","time":"2024-01-28 08:39:59"},
        # {"id":"751eba06-a992-469b-a76f-879581fe12bc","name":"活动限次","time":"2024-01-28 09:39:59"},
        # {"id":"32b769a2-330a-44e5-8e4c-c9627ca014b6","name":"活动限额限次","time":"2024-01-28 08:39:59"},
        # {"id":"02a5e826-191d-46ec-b129-6580ccfbdd82","name":"活动固定金额限次","time":"2024-01-28 10:39:59"},
        # #
        # {"id":"9467c339-b1eb-4c86-9034-45df6c26d14c","name":"用户维度返现有效期","time":""},
        # {"id":"cfded6de-8bb6-4e98-8939-71060a550581","name":"用户维度限额","time":""},
        # {"id":"15c2fae4-1a3a-4b39-b816-7c2c1e775282","name":"自然月限额限次","time":"2024-01-28 11:39:59"},
    ]

    for get_one in dir_dict_data_list:

        get_module_id = get_one["id"]
        get_ids = MetersphereUtils.get_batch_ids(1, 50, [get_module_id])
        for get_id in get_ids:
            MexUpdateCaseBatch12_2_marketing_assert_update_time_sub_time.handler_process_data(get_id, "")
            sleep(10)
            # MexUpdateCaseBatch12_3_xxljob_need_add_config_usenewconfig.handler_process_data(get_id, "")
            # sleep(10)
            MexUpdateCaseBatch12_4_data_campaigns_campaign_type.handler_process_data(get_id, "")
            sleep(10)
