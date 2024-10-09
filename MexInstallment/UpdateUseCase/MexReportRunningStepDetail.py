import MetersphereUtils


def running_process(id):
    get_content = MetersphereUtils.get_test_plan_report_running_report_test_ids(id)
    print(get_content)
    if str(get_content).count("ERROR") > 0:
        print("有报错。。。。。。。。。")
    return  get_content


if __name__ == '__main__':
    # 输入用例id
    #报告用例id，正在执行时

    get_result_all_steps_status = running_process("f357771a-bca5-4f8d-adce-30617fcb47d0")
    print(get_result_all_steps_status)
    if str(get_result_all_steps_status).count("ERROR")>0:
        print("有报错。。。。。。。。。")
    # find_process("6cbf57db-ee2e-4965-8b71-d661d56e9932")
