#!/usr/bin/python3
# -*- coding:utf-8 -*-
import calendar
import datetime
import json
import math
import sys

import jsonpath

import MexTrade
import CurrentStatement
import MexPaymentAllocation


dds = []
gov_rate_config = {"2022-09": 0.317, "2022-10": 0.337, "2022-11": 0.317, "2022-12": 0.317, "2023-01": 0.337,
                   "2023-02": 0.317}
purchase_config = {"2022-09": 0.348, "2022-10": 0.348, "2022-11": 0.348, "2022-12": 0.348, "2023-01": 0.348,
                   "2023-02": 0.348}
#trade ins apr mpr
apr=[]

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
                    ins_prin_cal_list = jsonpath.jsonpath(get_purchase_data_one,
                                                            "$..ins_prin_cal")
                    repaid_prin_list = jsonpath.jsonpath(get_purchase_data_one,
                                                         "$..repaid_prin")
                    get_total_prin = math.fsum(ins_prin_cal_list)
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


def cal_minpayment_result(dq):
    ins_vat=0
    ins_interest=0
    ins_principal=0
    ins_all=ins_vat + ins_interest + ins_principal
    end_stmt_posted_bal=0
    vat=0
    interest=0
    fee=0
    credit_limit_amt=0
    c1=0
    c2=0
    c3=0
    if dq==False:
        c1=(end_stmt_posted_bal -ins_all -vat -interest) * 1.5% +ins_all + vat +interest
        c2 = credit_limit_amt*1.25% + ins_all
        c3= (end_stmt_posted_bal-ins_all - interest - vat - fee) * 1.6% + interest + vat + fee + ins_all
    else:
        unpaid_min_pmt_bal=0
        c1 = ( end_stmt_posted_bal -ins_all - interest - vat - unpaid_min_pmt_bal) * 1.5 % + interest + vat + unpaid_min_pmt_bal + ins_all
        c2= credit_limit_amt * 1.25 % + unpaid_min_pmt_bal + ins_all
        c3=(end_stmt_posted_bal - ins_all - interest - vat - fee - unpaid_min_pmt_bal) * 1.6 % + interest + vat + fee + unpaid_min_pmt_bal + ins_all
    return max(c1, c2, c3)
     # ,其他逻辑没写 todo

def handler(get_list, get_init_data):
    purchase_data_all = []
    get_time_line = get_init_data["get_time_line"]
    init_credit_line = get_init_data["credit_line"]
    avilibale_credit_line = int(get_init_data["credit_line"])
    statement_period = get_init_data["statement_period"]
    due_days=get_init_data["due_days"]
    get_cur_time_point = 0
    cur_statement_time = 0
    statement_days=get_init_data["statement_days"]
    statement_days_reduce_1=get_init_data["statement_days_reduce_1"]

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
    #init第一账单
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
    quantity=0
    amount=0
    for i,get_one in enumerate(get_list):

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


            if  get_id=="${xxl_task_id_posted}":
                get_time_day=str(get_time_line[get_cur_time_point - 1]).split(" ")[0]
                if get_time_day in statement_days_reduce_1:
                    print("分期入账")
                    for get_purchase_data_one in purchase_data_all:
                        for get_key in get_purchase_data_one.keys():
                            if get_key.count("purchase_"):
                                get_ins_repaid_info = get_purchase_data_one[get_key]
                                cur_statement_period = statement_period[cur_statement_time]
                                if cur_statement_period in get_ins_repaid_info:
                                    cur_ins_info = get_ins_repaid_info[cur_statement_period]

                                    get_cur_statement_one.min_payment_ins_prin = (
                                            get_cur_statement_one.min_payment_ins_prin
                                            + cur_ins_info['ins_prin_cal']
                                            - cur_ins_info['repaid_prin'])

            #DQ
            elif get_id == "":
                if get_cur_statement_one.last_min_payment > get_cur_statement_one.min_payment_reverse:
                    dq_bucket = dq_bucket + 1
                    get_cur_statement_one.dq_bucket = dq_bucket
                    dq_bucket_record=dq_bucket_record+1
                    if dq_bucket==-1 and dq_bucket_record>=1:
                        dq_bucket =2
                        get_cur_statement_one.dq_bucket = 2

                    print("dq_bucket:" + str(get_cur_statement_one.dq_bucket))
                elif get_cur_statement_one.last_min_payment <= get_cur_statement_one.min_payment_reverse:
                    get_cur_statement_one.dq_bucket = - 1
                    dq_bucket = -1
                    print("dq_bucket:" + str(
                        get_cur_statement_one.dq_bucket) + "")

        elif get_one["path"] == "/v1.0/credit/installments/consult":
            get_consult_result_script=get_one["script"]
            quantity=0
            if str(get_consult_result_script).count(".get(0).")>0:
                quantity=3
            elif str(get_consult_result_script).count(".get(1).")>0:
                quantity = 6
            elif str(get_consult_result_script).count(".get(2).")>0:
                quantity = 9
            elif str(get_consult_result_script).count(".get(3).")>0:
                quantity = 12
            for k in range(i-1,0,-1):
                if get_list[k]["path"]=="/backoffice/dfl-ng/credit/authorizations/posting":
                    get_info=json.loads(get_list[k]["body"]["raw"])
                    local_date_time=get_info["transaction"]["local_date_time"]
                    amount= float(get_info["amount"]["local"]["total"]) * 100

                    purchase_data_all = MexTrade.purchaseTradeIns(purchase_data_all, quantity, local_date_time ,statement_period,
                                                                 cur_statement_time, amount)
                    break
               
        elif get_one["path"] == "/transactions/authorizations":
            print()

        elif get_one["path"] == "/backoffice/dfl-ng/credit/authorizations/posting":

            get_raw = json.loads(get_one["body"]["raw"])
            if get_raw["transaction"]["type"] == "PURCHASE":
                print("purchase初始化")
                #MSI
                if "installments" in get_raw.keys():
                    quantity = int(get_raw["installments"]["quantity"])
                    amount = float(get_raw["amount"]["local"]["total"]) * 100
                    credit_type=get_raw["installments"]["credit_type"]
                    avilibale_credit_line = avilibale_credit_line - amount
                    local_date_time = get_raw["transaction"]["local_date_time"]
                    if credit_type=="WITHOUT_INTEREST":
                        purchase_data_all = MexTrade.purchaseMSI(purchase_data_all, quantity, local_date_time, statement_period,
                                                          cur_statement_time, amount)

                # else:
                #     quantity = int(get_raw["installments"]["quantity"])
                #     amount = float(get_raw["amount"]["local"]["total"]) * 100
                #     avilibale_credit_line = avilibale_credit_line - amount
                #     local_date_time = get_raw["transaction"]["local_date_time"]
                #     purchase_data_all = MexTrade.purchaseTradeIns(purchase_data_all, quantity, local_date_time,
                #                                              statement_period,
                #                                              cur_statement_time, amount)


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
                MexPaymentAllocation.handler_payment(statement_period, cur_statement_time, purchase_data_all,
                                                  get_all_statement_data,
                                                  amount)

            if get_raw["transaction"]["type"] == "REFUND":
                amount = float(get_raw["amount"]["local"]["total"]) * 100
                avilibale_credit_line = avilibale_credit_line - amount
                print("退款操作 金额：" + str(amount))
                get_cur_statement_one.min_payment_reverse = get_cur_statement_one.min_payment_reverse + amount
                purchase_data_all, get_all_statement_data = MexPaymentAllocation.handler_refund(statement_period,
                                                                                             cur_statement_time,
                                                                                             purchase_data_all,
                                                                                             get_all_statement_data,
                                                                                             amount)

                for get_one1 in purchase_data_all:
                    print(get_one1)
                    print("每笔退款+++")

        elif get_one["path"] == "/backoffice/dfl/credit/statement/create":
            print("出账" + "第" + str(cur_statement_time + 1) + "期:出账数据")

            get_cur_statement_one.min_payment_all = cal_minpayment_result()
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

