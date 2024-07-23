import json

neum = ["20220827~20220926", "20220927~20221026", "20221027~20221127", "20221128~20221226", "20221227~20230126",
            "20230127~20230126"]
statement_days=["2022-09-27","2022-10-27","2022-11-28","2022-12-27","2023-01-27"]
statement_days_reduce_1=["2022-09-26","2022-10-26","2022-11-27","2022-12-26","2023-01-26"]
# , "20230125~20230224"
due_days_neum=["20221017","20221116","20221219","20230116","20230216","20230321"]
grace_days_neum=["20221019","20221118","20221221","20230118","20230220","20230323"]
def init_data(get_list):
    statement_count = 0
    credit_line = 0
    # statement_day = statement_day
    get_time_line = []
    for get_one in get_list:

        if get_one["path"] == "/backoffice/dfl/credit/statement/create":
            statement_count = statement_count + 1

        elif get_one["path"] == "/v1.0/credit/contracts":
            get_raw = json.loads(get_one["body"]["raw"])
            # statement_day = get_raw["product"]["params"]["statementDay"]
            credit_line = get_raw["product"]["params"]["initialCreditLine"]
        elif get_one["path"] == "/api/admin/system/faketime":
            get_raw = json.loads(get_one["body"]["raw"])
            if str(get_raw["time"]).count("__timeShift") > 0:
                continue
            else:
                get_time_line.append(get_raw["time"])

    statement_period = []
    ki = 0

    for get_time_one in get_time_line:
        get_day=str(get_time_one).split(" ")[0]
        if get_day in statement_days:
            statement_period.append(neum[ki])
            ki=ki+1


    due_days={}
    for i in statement_period:
        get_peroid_number=neum.index(i)  
        due_days.update({i:due_days_neum[get_peroid_number]})
    
    get_init_data = {"credit_line": credit_line, "statement_days": statement_days,"statement_days_reduce_1":statement_days_reduce_1, "statement_count": statement_count,
                     "get_time_line": get_time_line, "statement_period": statement_period,"due_days":due_days}
    print(get_init_data)
    print("+++初始化数据结束+++++")

    return get_init_data