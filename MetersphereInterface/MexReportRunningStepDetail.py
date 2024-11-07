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
    get_result_all_steps_status = running_process("c5f8c064-7b7b-40ff-8675-e04a9014a94f")
    print(get_result_all_steps_status)
    if str(get_result_all_steps_status).count("ERROR")>0:
        print("有报错。。。。。。。。。")
    # find_process("6cbf57db-ee2e-4965-8b71-d661d56e9932")
