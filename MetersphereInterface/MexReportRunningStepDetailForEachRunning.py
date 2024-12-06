from time import sleep

import MetersphereUtils


def running_process():
    for i in range(0, 100):

        get_dict_ids_names=MetersphereUtils.get_test_plan_report_all_running_detail_info()
        for k,v in get_dict_ids_names.items():
            print(v)
            get_content = MetersphereUtils.get_test_plan_report_running_report_test_ids(k)
            print(get_content)
            if str(get_content).count("ERROR") > 0:
                print("有报错。。。。。。。。。")
        sleep(30)



if __name__ == '__main__':
    running_process()
