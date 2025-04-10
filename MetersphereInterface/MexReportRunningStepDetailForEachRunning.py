from time import sleep

import MetersphereUtils


def running_process():
    for i in range(0, 100):

        get_dict_ids_names=MetersphereUtils.get_test_plan_report_all_running_detail_info(userId="admin")
        if get_dict_ids_names==False:
            sleep(30)
            continue
        for k,v in get_dict_ids_names.items():
            print(v)
            get_content = MetersphereUtils.get_test_plan_report_running_report_test_ids(k)
            print(get_content)
            if str(get_content).count("ERROR") > 0:
                print("有报错。。。。。。。。。")
        sleep(30)


#userId需要才能看到对应的用例执行，默认admin
if __name__ == '__main__':
    running_process()
