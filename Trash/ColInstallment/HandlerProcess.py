#!/usr/bin/python3
# -*- coding:utf-8 -*-
import calendar
import datetime
import json
import math
import sys

import jsonpath

import ColTrade
import CurrentStatement
import PaymentAllocation

dds = []
gov_rate_config = {"2022-09": 0.317, "2022-10": 0.337, "2022-11": 0.317, "2022-12": 0.337, "2023-01": 0.317,
                   "2023-02": 0.337}
purchase_config = {"2022-09": 0.317, "2022-10": 0.337, "2022-11": 0.317, "2022-12": 0.337, "2023-01": 0.317,
                   "2023-02": 0.337}


def cal_interest(cur_statement_time, purchase_data_all, statement_period, interest_time_line, get_more_day_cal_interest,
                 get_more_day_cal_late_interest):
    interest_init_amount = 0
    get_cur_time_line = datetime.datetime.strptime(interest_time_line, "%Y-%m-%d %H:%M:%S")
    get_cur_time_line_year_month = interest_time_line.split("-")[0] + "-" + interest_time_line.split("-")[1]
    days_in_month = calendar.monthrange(get_cur_time_line.year, get_cur_time_line.month)[1]
    get_cur_time_line_day1 = get_cur_time_line - datetime.timedelta(days=1)
    get_cur_time_line_day2 = get_cur_time_line - datetime.timedelta(days=2)
    get_cur_time_line_day3 = get_cur_time_line - datetime.timedelta(days=3)
    for get_purchase_data_one in purchase_data_all:
        for get_key in get_purchase_data_one.keys():
            # 一天一天计息 或者隔天修改日切利息date
            if get_key.count("purchase_"):
                #用例计息不会这么多天，临时处理下
                if get_key.count(get_cur_time_line_day1.strftime("%Y-%m-%d")) or get_key.count(
                        get_cur_time_line_day2.strftime("%Y-%m-%d")) or get_key.count(
                        get_cur_time_line_day3.strftime("%Y-%m-%d")) or get_more_day_cal_interest == True:
                    # 总本金相加-已还本金
                    # for get_ins_repaid_info in get_purchase_data_one[get_key]:
                    get_ins_repaid_info = get_purchase_data_one[get_key]
                    interest_cal_list = jsonpath.jsonpath(get_purchase_data_one, "$..interest_cal")
                    late_interest_cal_list = jsonpath.jsonpath(get_purchase_data_one,
                                                               "$..late_interest_cal")
                    ins_total_prin_list = jsonpath.jsonpath(get_purchase_data_one,
                                                            "$..ins_total_prin")
                    repaid_prin_list = jsonpath.jsonpath(get_purchase_data_one,
                                                         "$..repaid_prin")
                    get_total_prin = math.fsum(ins_total_prin_list)
                    get_repaid_prin = math.fsum(repaid_prin_list)
                    if get_more_day_cal_interest == True and get_more_day_cal_late_interest == True:
                        # 罚息可能会有问题
                        print("罚息+++++")
                        get_info = get_ins_repaid_info[statement_period[cur_statement_time]]
                        last_time_late_interest_cal = get_info["late_interest_cal"]
                        month_rate = gov_rate_config[get_cur_time_line_year_month] if gov_rate_config[
                                                                                          get_cur_time_line_year_month] < \
                                                                                      get_purchase_data_one[
                                                                                          "p_rate"] else \
                            get_purchase_data_one["p_rate"]
                        get_cal_part = math.pow(1 + month_rate, float(1 / 12)) - 1
                        get_cal = round(math.prod([get_total_prin - get_repaid_prin, get_cal_part]) / days_in_month, 0)

                        interest_init_amount = interest_init_amount + get_cal
                        del get_info["late_interest_cal"]
                        get_info.setdefault("late_interest_cal", get_cal + last_time_late_interest_cal)

                        del get_ins_repaid_info[statement_period[cur_statement_time]]
                        get_ins_repaid_info.setdefault(statement_period[cur_statement_time], get_info)
                    else:
                        get_info = get_ins_repaid_info[statement_period[cur_statement_time]]
                        last_time_interest_cal = get_info["interest_cal"]
                        month_rate = gov_rate_config[get_cur_time_line_year_month] if gov_rate_config[
                                                                                          get_cur_time_line_year_month] < \
                                                                                      get_purchase_data_one[
                                                                                          "p_rate"] else \
                            get_purchase_data_one["p_rate"]
                        get_cal_part = math.pow(1 + month_rate, float(1 / 12)) - 1
                        get_cal = round(math.prod([get_total_prin - get_repaid_prin, get_cal_part]) / days_in_month, 0)

                        interest_init_amount = interest_init_amount + get_cal
                        del get_info["interest_cal"]
                        get_info.setdefault("interest_cal", get_cal + last_time_interest_cal)

                        del get_ins_repaid_info[statement_period[cur_statement_time]]
                        get_ins_repaid_info.setdefault(statement_period[cur_statement_time], get_info)
    print("++计息数据展示start++")
    for get_one1 in purchase_data_all:
        print(get_one1)
    print("++计息数据展示end++")
    return purchase_data_all, interest_init_amount
    #                          计算利息


def handler(get_list, get_init_data):
    purchase_data_all = []
    get_time_line = get_init_data["get_time_line"]
    init_credit_line = get_init_data["credit_line"]
    avilibale_credit_line = int(get_init_data["credit_line"])
    statement_period = get_init_data["statement_period"]
    due_days=get_init_data["due_days"]
    get_cur_time_point = 0
    cur_statement_time = 0
    get_more_day_cal_interest = False
    get_more_day_cal_late_interest = False
    get_all_statement_data = []
    dq_bucket = -1
    dq_bucket_record=0
    dq_days = 0
    show_info={}
    # 处理账期
    for i in statement_period:
        get_c = CurrentStatement.CurrentStatement()
        get_all_statement_data.append(get_c)
    #没有出账不会执行
    if len(statement_period) == 0:
        print("没有出账，不会继续执行")
        sys.exit()
    get_cur_statement_one = get_all_statement_data[cur_statement_time]
    get_cur_statement_one.start_statemet_day = statement_period[cur_statement_time].split("~")[0]
    get_cur_statement_one.end_statemet_day = statement_period[cur_statement_time].split("~")[1]
    get_cur_statement_one.statement_peroid=statement_period[cur_statement_time].split("~")[0]+"~"+statement_period[cur_statement_time].split("~")[1]
    get_cur_statement_one.credit_line = init_credit_line
    get_cur_statement_one.due_day=due_days[statement_period[cur_statement_time]]
    cur_time_line = ""
    trigger_del_set_repeat={}
    for get_one in get_time_line:
        trigger_del_set_repeat.update({get_one:[]})
    #process
    for get_one in get_list:

        if get_one["path"] == "/api/admin/system/faketime":
            get_raw = json.loads(get_one["body"]["raw"])
            if str(get_raw["time"]).count("__timeShift") > 0:
                continue
            elif get_time_line[get_cur_time_point] == get_raw["time"]:
                print(get_time_line[get_cur_time_point])
                cur_time_line = get_time_line[get_cur_time_point]
                get_cur_time_point = get_cur_time_point + 1
        elif get_one["path"] == "/xxl-job-admin/jobinfo/trigger":
            get_kvs = get_one["body"]["kvs"]
            get_id=""
            for get_kvs_one in get_kvs:
                if "name" in get_kvs_one and "value" in get_kvs_one and get_kvs_one["name"] == 'id':
                    get_id = get_kvs_one["value"]
                    break
            # # 同一天去重
            # if trigger_del_set_repeat[cur_time_line] == []:
            #     trigger_del_set_repeat[cur_time_line].append(get_id)

            #计息&罚息，隔天、多天处理罚息
            if get_id == "1887":
                print("计息")
                # 同一天去重
                if trigger_del_set_repeat[cur_time_line] == []:
                    trigger_del_set_repeat[cur_time_line].append(get_id)
                elif get_id in trigger_del_set_repeat[cur_time_line]:
                    continue
                #processs
                interest_time_line = cur_time_line
                purchase_data_all, interest_init_amount = cal_interest(cur_statement_time, purchase_data_all,
                                                                       statement_period, interest_time_line,
                                                                       get_more_day_cal_interest,
                                                                       get_more_day_cal_late_interest)
                if get_more_day_cal_interest == True:
                    get_more_day_cal_interest = False
                if get_more_day_cal_late_interest == True:
                    get_more_day_cal_late_interest = False
                get_cur_statement_one.min_payment_interest = get_cur_statement_one.min_payment_interest + interest_init_amount
                avilibale_credit_line = avilibale_credit_line - interest_init_amount
            #25号入账
            elif get_id == "1773" and get_time_line[get_cur_time_point - 1].count("-25"):
                print("入账")
                for get_purchase_data_one in purchase_data_all:
                    for get_key in get_purchase_data_one.keys():
                        if get_key.count("purchase_"):
                            get_ins_repaid_info = get_purchase_data_one[get_key]
                            cur_statement_period = statement_period[cur_statement_time]
                            if cur_statement_period in get_ins_repaid_info:
                                cur_ins_info = get_ins_repaid_info[cur_statement_period]

                                get_cur_statement_one.min_payment_ins_prin = (
                                        get_cur_statement_one.min_payment_ins_prin
                                        + cur_ins_info['ins_total_prin']
                                        - cur_ins_info['repaid_prin'])
            #罚息校验
            elif get_id == "1783":
                # 同一天去重
                if trigger_del_set_repeat[cur_time_line] == []:
                    trigger_del_set_repeat[cur_time_line].append(get_id)
                elif get_id in trigger_del_set_repeat[cur_time_line]:
                    continue
                get_more_day_cal_late_interest = True
                get_more_day_cal_interest = True
                # 1775 1776 依赖计息任务
                print("罚息校验")
            #DQ
            elif get_id == "1823":
                if get_cur_statement_one.last_min_payment > get_cur_statement_one.min_payment_reverse:
                    dq_bucket = dq_bucket + 1
                    get_cur_statement_one.dq_bucket = dq_bucket
                    dq_bucket_record=dq_bucket_record+1
                    if dq_bucket==-1 and dq_bucket_record>=1:
                        dq_bucket =2
                        get_cur_statement_one.dq_bucket = 2
                    # if cur_statement_time==1:
                    #     dq_days=1
                    #     get_cur_statement_one.dq_days = 1
                    # else:
                    #     # get_tmp_statement_period=cur_statement_period[cur_statement_time]
                    #     get_due_day=due_days[cur_statement_period]
                    #     get_due_day_datatime=datetime.datetime.strptime(get_due_day, "%Y%m%d")
                    #     get_cur_time_line_datetime = datetime.datetime.strptime(cur_time_line, "%Y-%m-%d %H:%M:%S")
                        # cal_day=get_cur_time_line_datetime-get_due_day_datatime
                        # print("计算dq_day")
                        # print(cal_day.days)
                        # dq_days=dq_days+cal_day.days
                        # print(dq_days)
                    print("dq_bucket:" + str(get_cur_statement_one.dq_bucket))
                elif get_cur_statement_one.last_min_payment <= get_cur_statement_one.min_payment_reverse:
                    get_cur_statement_one.dq_bucket = - 1
                    dq_bucket = -1
                    print("dq_bucket:" + str(
                        get_cur_statement_one.dq_bucket) + "")
            # 收取费
            elif get_id == "1892":
                if get_time_line[get_cur_time_point - 1].count("-25"):
                    if int(init_credit_line) >= 200000:
                        get_cur_statement_one.min_payment_fee_management = get_cur_statement_one.min_payment_fee_management + 1490000;
                        avilibale_credit_line = avilibale_credit_line - 1490000
                    else:
                        get_cur_statement_one.min_payment_fee_management = get_cur_statement_one.min_payment_fee_management + 790000;
                        avilibale_credit_line = avilibale_credit_line - 790000
                    print("收管理费：" + str(get_cur_statement_one.min_payment_fee_management))
                elif get_time_line[get_cur_time_point - 1].count("-24"):
                    get_cur_statement_one.min_payment_fee_late_management = get_cur_statement_one.min_payment_fee_late_management + 2092400
                    get_cur_statement_one.min_payment_vat = get_cur_statement_one.min_payment_vat + 2092400 * 0.16
                    avilibale_credit_line = avilibale_credit_line - 2092400
                    avilibale_credit_line = avilibale_credit_line - 2092400 * 0.16
                    print("收滞纳金&vat:" + str(
                        get_cur_statement_one.min_payment_fee_late_management) + " " + str(
                        get_cur_statement_one.min_payment_vat))
            
               
        elif get_one["path"] == "/transactions/authorizations":
            print()
        elif get_one["path"] == "/backoffice/dfl-ng/credit/authorizations/posting":

            get_raw = json.loads(get_one["body"]["raw"])
            if get_raw["transaction"]["type"] == "PURCHASE":
                print("purchase初始化")
                quantity = int(get_raw["installments"]["quantity"])
                amount = float(get_raw["amount"]["local"]["total"]) * 100
                avilibale_credit_line = avilibale_credit_line - amount
                local_date_time = get_raw["transaction"]["local_date_time"]
                purchase_data_all = ColTrade.purchase(purchase_data_all, quantity, local_date_time, statement_period,
                                                      cur_statement_time, amount)

            if get_raw["transaction"]["type"] == "PAYMENT":
                amount = float(get_raw["amount"]["local"]["total"]) * 100
                avilibale_credit_line = avilibale_credit_line + amount
                print("还款操作 金额：" + str(int(amount)))
                local_date_time = get_raw["transaction"]["local_date_time"]
                get_cur_statement_one.min_payment_reverse = get_cur_statement_one.min_payment_reverse + amount
                # 未出账提前还款
                # if cur_statement_time == 0:
                #     get_cur_statement_one.min_payment_ins_prin = get_cur_statement_one.min_payment_ins_prin + amount
                # else:
                PaymentAllocation.handler_payment(statement_period, cur_statement_time, purchase_data_all,
                                                  get_all_statement_data,
                                                  amount)

            if get_raw["transaction"]["type"] == "REFUND":
                amount = float(get_raw["amount"]["local"]["total"]) * 100
                avilibale_credit_line = avilibale_credit_line - amount
                print("退款操作 金额：" + str(amount))
                get_cur_statement_one.min_payment_reverse = get_cur_statement_one.min_payment_reverse + amount
                purchase_data_all, get_all_statement_data = PaymentAllocation.handler_refund(statement_period,
                                                                                             cur_statement_time,
                                                                                             purchase_data_all,
                                                                                             get_all_statement_data,
                                                                                             amount)

                for get_one1 in purchase_data_all:
                    print(get_one1)
                    print("每笔退款+++")

        elif get_one["path"] == "/backoffice/dfl/credit/statement/create":
            print("出账" + "第" + str(cur_statement_time + 1) + "期:出账数据")

            get_cur_statement_one.min_payment_all = (get_cur_statement_one.min_payment_interest
                                                     + get_cur_statement_one.min_payment_fee_management
                                                     + get_cur_statement_one.min_payment_fee_late_management
                                                     + get_cur_statement_one.min_payment_fee_replace
                                                     + get_cur_statement_one.min_payment_late_interest
                                                     + get_cur_statement_one.min_payment_vat
                                                     + get_cur_statement_one.min_payment_ins_prin
                                                     - get_cur_statement_one.min_payment_reverse
                                                     + get_cur_statement_one.last_min_payment)
            get_cur_statement_one.credit_line = avilibale_credit_line

            print(vars(get_cur_statement_one))
            last_min_payment = get_cur_statement_one.last_min_payment
            cur_min_payment = get_cur_statement_one.min_payment_all
            get_all_statement_data[cur_statement_time] = get_cur_statement_one
            # print(purchase_data_all)
            print("出账" + "第" + str(cur_statement_time + 1) + "期:end+++")
            #       处理账期，到下个账期初始化

            cur_statement_time = cur_statement_time + 1
            if cur_statement_time < len(statement_period):
                get_cur_statement_one = get_all_statement_data[cur_statement_time]
                get_cur_statement_one.start_statemet_day = statement_period[cur_statement_time].split("~")[0]
                get_cur_statement_one.end_statemet_day = statement_period[cur_statement_time].split("~")[1]
                get_cur_statement_one.last_min_payment = cur_min_payment
                get_cur_statement_one.statement_peroid=statement_period[cur_statement_time].split("~")[0]+"~"+statement_period[cur_statement_time].split("~")[1]

        elif get_one["path"] == "/v1.0/credit/cards/replacement":
            get_cur_statement_one.min_payment_fee_replace = get_cur_statement_one.min_payment_fee_replace + 2500000
            avilibale_credit_line = avilibale_credit_line - 2500000
        elif get_one["path"] == "update_sql":
            get_sql = get_one["update_sql"]
            # 隔很多天计息
            if get_sql.count("cc_ins_installment_info") and get_sql.count("interest_date"):
                get_more_day_cal_interest = True


    print("查看下所有账期数据情况+++")
    for get_one1 in get_all_statement_data:
        print(vars(get_one1))
        print("+all_statement_data++")


    # import pandas as pd
    # # 创建DataFrame
    # df = pd.DataFrame(columns=["总数据"])
    # df.loc["初始化数据"]=[str(get_init_data)]
    # for get_one1 in get_all_statement_data:
    #     df.loc[str(get_one1.statement_peroid)+"账期"]=[str(vars(get_one1))]

    # # 将DataFrame转换为HTML
    # html = df.to_html()

    # # 打印生成的HTML
    # file = open("file.html", "w")  # 打开文件，如果文件不存在则创建新文件
    # file.write(html)  # 写入文件内容
    # file.close()
