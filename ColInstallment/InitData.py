import json

neum = ["20220825~20220924", "20220925~20221024", "20221025~20221124", "20221125~20221224", "20221225~20230124",
            "20221225~20230124", "20230125~20230224", "20230225~20230324", "20230325~20230424"]
due_days_neum=["20221005","20221105","20221205","20230105","20230205","20230305","20230405","20230505","20230605"]
def init_data(get_list):
    statement_count = 0
    credit_line = 0
    statement_day = 0
    get_time_line = []
    for get_one in get_list:

        if get_one["path"] == "/backoffice/dfl/credit/statement/create":
            statement_count = statement_count + 1

        elif get_one["path"] == "/v1.0/credit/contracts":
            get_raw = json.loads(get_one["body"]["raw"])
            statement_day = get_raw["product"]["params"]["statementDay"]
            credit_line = get_raw["product"]["params"]["initialCreditLine"]
        elif get_one["path"] == "/api/admin/system/faketime":
            get_raw = json.loads(get_one["body"]["raw"])
            if str(get_raw["time"]).count("__timeShift") > 0:
                continue
            else:
                get_time_line.append(get_raw["time"])

    statement_period = []
    get_time_i = 0

    for get_time_one in get_time_line:
        if get_time_i == 0 and get_time_one.count("-25") > 0:
            for i in range(statement_count+1):
                statement_period.append(neum[i + 1])
            break
        elif get_time_i == 0 and get_time_one.count("2022-09-24") > 0 or get_time_one.count(
                "2022-09-23") > 0 or get_time_one.count("2022-09-22") > 0 or get_time_one.count("2022-09-21") > 0:
            for i in range(statement_count):
                statement_period.append(neum[i])

    due_days={}
    for i in statement_period:
        get_peroid_number=neum.index(i)  
        due_days.update({i:due_days_neum[get_peroid_number]})
    
    get_init_data = {"credit_line": credit_line, "statement_day": statement_day, "statement_count": statement_count,
                     "get_time_line": get_time_line, "statement_period": statement_period,"due_days":due_days}
    print(get_init_data)
    print("+++初始化数据结束+++++")

    return get_init_data