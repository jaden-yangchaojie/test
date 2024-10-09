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

# trade ins apr mpr
apr = 0.899000

real_interest_rates = {}


def cal_adb(get_cur_statement_one, cur_statement_time, get_all_statement_data):
    if cur_statement_time == 0 and get_cur_statement_one.dq_is==True:
        get_cur_statement_one.init_balance = (get_cur_statement_one.min_payment_late_fee +
                                              get_cur_statement_one.min_payment_fee_replace +
                                              get_cur_statement_one.min_payment_vat +
                                              get_cur_statement_one.min_payment_ins_vat +
                                              get_cur_statement_one.min_payment_ins_prin +
                                              get_cur_statement_one.min_payment_principal)
        get_cur_statement_one.last_init_balance = 0
    if cur_statement_time >= 1 and get_cur_statement_one.dq_is==True:
        last_statement_one = get_all_statement_data[cur_statement_time - 1]
        get_bal = last_statement_one.init_balance
        start_day = get_cur_statement_one.start_statemet_day
        end_day = get_cur_statement_one.end_statemet_day
        get_cur_statement_start_day = datetime.datetime.strptime(start_day, '%Y%m%d')
        get_cur_statement_end_day = datetime.datetime.strptime(end_day, '%Y%m%d')
        cycle_days = get_cur_statement_end_day - get_cur_statement_start_day
        get_record = get_cur_statement_one.adb_record
        get_cur_adb_cal_all = []
        get_date_trigger = []
        for get_num, get_one_record in enumerate(get_record):
            get_tmp_str = list(dict(get_one_record).keys())[0]
            get_date_str = get_tmp_str.replace("-", "")
            get_date = datetime.datetime.strptime(get_date_str, '%Y%m%d')
            get_date_trigger.append(get_date_str)

        for ii in range(0, cycle_days.days + 1):
            get_t = get_cur_statement_start_day + datetime.timedelta(days=ii)
            get_str_date = str(get_t.year) + str(get_t.month if get_t.month > 9 else "0" + str(get_t.month)) + str(
                get_t.day if get_t.day > 9 else "0" + str(get_t.day))
            if get_str_date in list(get_date_trigger):
                get_num = get_date_trigger.index(get_str_date)
                get_tmp_str_value = list(dict(get_record[get_num]).values())[0]
                if get_tmp_str_value < 0:
                    get_tmp_str_interest = (
                            last_statement_one.min_payment_interest + last_statement_one.min_payment_ins_interest)
                    get_tmp_str_value_bal = get_tmp_str_value + get_tmp_str_interest
                    get_bal = get_bal + get_tmp_str_value_bal
                    get_cur_adb_cal_all.append({"cycle_day": ii + 1, "date": get_str_date, "bal": get_bal})
                else:
                    get_tmp_str_value_bal = get_tmp_str_value
                    get_bal = get_bal + get_tmp_str_value_bal
                    get_cur_adb_cal_all.append({"cycle_day": ii + 1, "date": get_str_date, "bal": get_bal})
            else:
                get_cur_adb_cal_all.append({"cycle_day": ii + 1, "date": get_str_date, "bal": get_bal})

        adb_total = 0
        for get_num, get_dict in enumerate(get_cur_adb_cal_all):
            adb_total = adb_total + get_dict["bal"]
        get_cur_statement_one.adb = round(adb_total / len(get_cur_adb_cal_all), 0)
        get_cur_statement_one.init_balance = get_bal
        get_cur_statement_one.last_init_balance = last_statement_one.init_balance
        print()
        # for get_num, get_one_record in enumerate(get_record):
        #     if get_num == 0:
        #         get_tmp_str = list(dict(get_one_record).keys())[0]
        #         get_date_str = get_tmp_str.replace("-", "")
        #         get_date = datetime.datetime.strptime(get_date_str, '%Y%m%d')
        #         get_diff_days = get_date - get_cur_statement_start_day
        #         print(get_diff_days)
        #         get_tmp_str_value = float(list(dict(get_one_record).values())[0])
        #         get_tmp_str_interest = (
        #                     last_statement_one.min_payment_interest + last_statement_one.min_payment_ins_interest)
        #         get_tmp_str_value_bal = get_tmp_str_value + get_tmp_str_interest
        #         get_bal = (get_bal) * (1 if get_diff_days.days == 0 else get_diff_days.days + 1) + get_tmp_str_value_bal
        #         print(get_bal)
        #     else:
        #
        #         get_tmp_str = list(dict(get_one_record).keys())[0]
        #         get_date_str = get_tmp_str.replace("-", "")
        #         get_date = datetime.datetime.strptime(get_date_str, '%Y%m%d')
        #         get_tmp_str_value = float(list(dict(get_one_record).values())[0])
        #
        #         get_tmp_last_str = list(dict(get_record[get_num - 1]).keys())[0]
        #         get_date_last_str = get_tmp_last_str.replace("-", "")
        #         get_date_last = datetime.datetime.strptime(get_date_last_str, '%Y%m%d')
        #         get_diff_days = get_date - get_date_last
        #
        #         get_bal = (get_bal) * (1 if get_diff_days.days == 0 else get_diff_days.days) + (
        #                     get_cur_statement_one.min_payment_late_fee +
        #                     get_cur_statement_one.min_payment_fee_replace +
        #                     get_cur_statement_one.min_payment_vat +
        #                     get_cur_statement_one.min_payment_ins_vat +
        #                     get_cur_statement_one.min_payment_ins_prin +
        #                     get_cur_statement_one.min_payment_principal)
        #
        #         print(get_diff_days.days)
        # get_cur_statement_one.adb = round(get_bal / cycle_days.days, 2)
        # get_cur_statement_one.init_balance = get_bal
        # get_cur_statement_one.last_init_balance = last_statement_one.init_balance

        print()


# todo
def cal_interest_and_vat(get_cur_statement_one, cur_statement_time):
    if cur_statement_time >= 1 and get_cur_statement_one.dq_is==True:
        udi = {"20220926": 7.521027000, "20220927": 7.521027000, "20221026": 7.559441000, }
        start_udi = udi[get_cur_statement_one.start_statemet_day]
        end_udi = udi[get_cur_statement_one.end_statemet_day]
        adb = get_cur_statement_one.adb

        inflation = round(math.fabs(float(end_udi) / float(start_udi)) - 1, 6)
        real_interest_rate = round(apr / 12 - inflation, 6)
        inflationNonTax = inflation

        day_cycle = 30
        daily_interest = adb * real_interest_rate / 30
        realdailyInt = round(daily_interest * day_cycle, 0)
        interest_not_tax = round((adb * inflation / 30) * day_cycle, 0)

        total_interest = round(realdailyInt + interest_not_tax, 0)
        interest_vat = realdailyInt * 0.16
        if get_cur_statement_one.dq_is == True:
            total_fee = 3500
            total_vat = round(total_fee * 0.16 + interest_vat, 0)
        else:
            total_fee = 0
            total_vat = 0

        get_cur_statement_one.min_payment_interest = get_cur_statement_one.min_payment_interest + total_interest
        get_cur_statement_one.min_payment_vat = get_cur_statement_one.min_payment_vat + total_vat
        get_cur_statement_one.min_payment_late_fee = get_cur_statement_one.min_payment_late_fee + total_fee

        print(total_interest)
        print(total_vat)
        print(total_fee)
        print("+++++")


# todo
def cal_minpayment_result_old(get_cur_statement_one):
    ins_vat = get_cur_statement_one.min_payment_ins_vat
    ins_interest = get_cur_statement_one.min_payment_ins_interest
    ins_principal = get_cur_statement_one.min_payment_ins_prin
    ins_all = ins_vat + ins_interest + ins_principal
    end_stmt_posted_bal = get_cur_statement_one.end_stmt_posted_bal
    vat = get_cur_statement_one.min_payment_vat
    interest = get_cur_statement_one.min_payment_interest
    fee = get_cur_statement_one.min_payment_fee_replace + get_cur_statement_one.min_payment_late_fee
    credit_limit_amt = float(get_cur_statement_one.credit_line)
    if end_stmt_posted_bal<=0:
        return 0
    c1 = 0
    c2 = 0
    c3 = 0
    if get_cur_statement_one.dq_is == False:
        c1 = (end_stmt_posted_bal - ins_all - vat - interest) * 1.5 / 100 + ins_all + vat + interest
        c2 = credit_limit_amt * 1.25 / 100 + ins_all
        c3 = (end_stmt_posted_bal - ins_all - interest - vat - fee) * 1.6 / 100 + interest + vat + fee + ins_all
    else:
        unpaid_min_pmt_bal = get_cur_statement_one.last_min_payment
        c1 = (
                     end_stmt_posted_bal - ins_all - interest - vat - unpaid_min_pmt_bal) * 1.5 / 100 + interest + vat + unpaid_min_pmt_bal + ins_all
        c2 = credit_limit_amt * 1.25 / 100 + unpaid_min_pmt_bal + ins_all
        c3 = (
                     end_stmt_posted_bal - ins_all - interest - vat - fee - unpaid_min_pmt_bal) * 1.6 / 100 + interest + vat + fee + unpaid_min_pmt_bal + ins_all

    if (c2 > c3 or c2 > c3):
        if c2 > ins_all:
            return max(c1, c3)
    else:
        return max(c1, c2, c3)
    # ,其他逻辑没写 todo

def cal_minpayment_result(get_cur_statement_one):
    ins_vat = get_cur_statement_one.min_payment_ins_vat
    ins_interest = get_cur_statement_one.min_payment_ins_interest
    ins_principal = get_cur_statement_one.min_payment_ins_prin
    #修改点
    ins_all = ins_vat + ins_interest
    end_stmt_posted_bal = get_cur_statement_one.end_stmt_posted_bal
    vat = get_cur_statement_one.min_payment_vat
    interest = get_cur_statement_one.min_payment_interest
    fee = get_cur_statement_one.min_payment_fee_replace + get_cur_statement_one.min_payment_late_fee
    credit_limit_amt = float(get_cur_statement_one.credit_line)
    if end_stmt_posted_bal<=0:
        return 0
    c1 = 0
    c2 = 0
    c3 = 0
    c4=end_stmt_posted_bal
    c5=10000
    if get_cur_statement_one.dq_is == False:
        c1 = (end_stmt_posted_bal - ins_all - vat - interest) * 1.5 / 100 + ins_all + vat + interest
        c2 = credit_limit_amt * 1.25 / 100
        c3 = (end_stmt_posted_bal - ins_all - interest - vat - fee) * 1.6 / 100 + interest + vat + fee + ins_all
    else:
        unpaid_min_pmt_bal = get_cur_statement_one.last_min_payment
        c1 = (
                     end_stmt_posted_bal - ins_all - interest - vat - unpaid_min_pmt_bal) * 1.5 / 100 + interest + vat + unpaid_min_pmt_bal + ins_all
        c2 = credit_limit_amt * 1.25 / 100 + unpaid_min_pmt_bal
        c3 = (
                     end_stmt_posted_bal - ins_all - interest - vat - fee - unpaid_min_pmt_bal) * 1.6 / 100 + interest + vat + fee + unpaid_min_pmt_bal + ins_all
    if end_stmt_posted_bal<=0:
        return 0
    elif end_stmt_posted_bal<=10000:
        return end_stmt_posted_bal
    elif c2>end_stmt_posted_bal:
       tmp= max(c1,c3)
       if tmp<10000:
           return  10000
       else:
           return tmp
    else:
        tmp = max(c1,c2,c3)
        if tmp < 10000:
            return 10000
        else:
            return tmp

def handler(get_list, get_init_data):
    purchase_data_all = []
    get_time_line = get_init_data["get_time_line"]
    init_credit_line = get_init_data["credit_line"]
    avilibale_credit_line = int(get_init_data["credit_line"])
    statement_period = get_init_data["statement_period"]
    due_days = get_init_data["due_days"]
    get_cur_time_point = 0
    cur_statement_time = 0
    statement_days = get_init_data["statement_days"]
    statement_days_reduce_1 = get_init_data["statement_days_reduce_1"]

    get_all_statement_data = []
    dq_bucket = -1
    dq_bucket_record = 0
    dq_days = 0
    show_info = {}
    # 处理账期
    for i in statement_period:
        get_c = CurrentStatement.CurrentStatement()
        get_all_statement_data.append(get_c)
    # 没有出账不会执行
    if len(statement_period) == 0:
        print("没有出账，不会继续执行")
        sys.exit()
    # init第一账单
    get_cur_statement_one = get_all_statement_data[cur_statement_time]
    get_cur_statement_one.start_statemet_day = statement_period[cur_statement_time].split("~")[0]
    get_cur_statement_one.end_statemet_day = statement_period[cur_statement_time].split("~")[1]
    get_cur_statement_one.statement_peroid = statement_period[cur_statement_time].split("~")[0] + "~" + \
                                             statement_period[cur_statement_time].split("~")[1]
    get_cur_statement_one.credit_line = init_credit_line
    get_cur_statement_one.due_day = due_days[statement_period[cur_statement_time]]
    cur_time_line = ""
    trigger_del_set_repeat = {}
    for get_one in get_time_line:
        trigger_del_set_repeat.update({get_one: []})
    # process
    quantity = 0
    amount = 0
    for i, get_one in enumerate(get_list):

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
            get_id = ""
            for get_kvs_one in get_kvs:
                if "name" in get_kvs_one and "value" in get_kvs_one and get_kvs_one["name"] == 'id':
                    get_id = get_kvs_one["value"]
                    break

            # # 同一天去重
            # if trigger_del_set_repeat[cur_time_line] == []:
            #     trigger_del_set_repeat[cur_time_line].append(get_id)

            if get_id == "${xxl_task_id_posted}":
                get_time_day = str(get_time_line[get_cur_time_point - 1]).split(" ")[0]
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
                                    get_cur_statement_one.min_payment_ins_interest = (
                                            get_cur_statement_one.min_payment_ins_interest
                                            + cur_ins_info['interest_cal']
                                            - cur_ins_info['repaid_interest_cal'])
                                    get_cur_statement_one.min_payment_ins_vat = (
                                            get_cur_statement_one.min_payment_ins_vat
                                            + cur_ins_info['vat_cal']
                                            - cur_ins_info['repaid_vat_cal'])

                    # adb_record
                    get_time_day = str(get_time_line[get_cur_time_point - 1]).split(" ")[0]
                    get_cur_statement_one.adb_record.append({get_time_day: (
                            get_cur_statement_one.min_payment_ins_vat + get_cur_statement_one.min_payment_ins_prin)})
            # DQ
            elif get_id == "":
                get_cur_statement_one.dq_is = True
                # if get_cur_statement_one.last_min_payment > get_cur_statement_one.min_payment_reverse:
                #     dq_bucket = dq_bucket + 1
                #     get_cur_statement_one.dq_bucket = dq_bucket
                #     dq_bucket_record = dq_bucket_record + 1
                #     if dq_bucket == -1 and dq_bucket_record >= 1:
                #         dq_bucket = 2
                #         get_cur_statement_one.dq_bucket = 2
                #
                #     print("dq_bucket:" + str(get_cur_statement_one.dq_bucket))
                # elif get_cur_statement_one.last_min_payment <= get_cur_statement_one.min_payment_reverse:
                #     get_cur_statement_one.dq_bucket = - 1
                #     dq_bucket = -1
                #     print("dq_bucket:" + str(
                #         get_cur_statement_one.dq_bucket) + "")
        elif get_one["path"] == "/backoffice/dfl/credit/dqTask/create":
            get_cur_statement_one.dq_is = True
            # get_cur_statement_one.min_payment_late_fee = get_cur_statement_one.min_payment_late_fee


        elif get_one["path"] == "/v1.0/credit/installments/consult":
            get_consult_result_script = get_one["script"]
            quantity = 0
            if str(get_consult_result_script).count(".get(0).") > 0:
                quantity = 3
            elif str(get_consult_result_script).count(".get(1).") > 0:
                quantity = 6
            elif str(get_consult_result_script).count(".get(2).") > 0:
                quantity = 9
            elif str(get_consult_result_script).count(".get(3).") > 0:
                quantity = 12
            for k in range(i - 1, 0, -1):
                if get_list[k]["path"] == "/backoffice/dfl-ng/credit/authorizations/posting":
                    get_info = json.loads(get_list[k]["body"]["raw"])
                    local_date_time = get_info["transaction"]["local_date_time"]
                    amount = float(get_info["amount"]["local"]["total"]) * 100
                    get_cur_statement_one.end_stmt_posted_bal = get_cur_statement_one.end_stmt_posted_bal - amount
                    purchase_data_all = MexTrade.purchaseTradeIns(purchase_data_all, quantity, local_date_time,
                                                                  statement_period,
                                                                  cur_statement_time, amount)
                    break

        elif get_one["path"] == "/transactions/authorizations":
            print()

        elif get_one["path"] == "/backoffice/dfl-ng/credit/authorizations/posting":

            get_raw = json.loads(get_one["body"]["raw"])
            if get_raw["transaction"]["type"] == "PURCHASE":
                print("purchase初始化")
                # MSI
                if "installments" in get_raw.keys():
                    quantity = int(get_raw["installments"]["quantity"])
                    amount = float(get_raw["amount"]["local"]["total"]) * 100
                    credit_type = get_raw["installments"]["credit_type"]
                    avilibale_credit_line = avilibale_credit_line - amount
                    local_date_time = get_raw["transaction"]["local_date_time"]
                    if credit_type == "WITHOUT_INTEREST":
                        purchase_data_all = MexTrade.purchaseMSI(purchase_data_all, quantity, local_date_time,
                                                                 statement_period,
                                                                 cur_statement_time, amount)
                else:
                    amount = float(get_raw["amount"]["local"]["total"]) * 100
                    avilibale_credit_line = avilibale_credit_line - amount
                    get_cur_statement_one.end_stmt_posted_bal=get_cur_statement_one.end_stmt_posted_bal+amount

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
                # adb_record
                get_time_day = str(get_time_line[get_cur_time_point - 1]).split(" ")[0]
                get_cur_statement_one.adb_record.append({get_time_day: -amount})

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
                # adb_record
                get_time_day = str(get_time_line[get_cur_time_point - 1]).split(" ")[0]
                get_cur_statement_one.adb_record.append({get_time_day: -amount})

                for get_one1 in purchase_data_all:
                    print(get_one1)
                    print("每笔退款+++")

        elif get_one["path"] == "/backoffice/dfl/credit/statement/create":
            print("出账" + "第" + str(cur_statement_time + 1) + "期:出账数据")

            get_cur_statement_one.credit_line = avilibale_credit_line
            # adb
            cal_adb(get_cur_statement_one, cur_statement_time, get_all_statement_data)
            # 息费税
            cal_interest_and_vat(get_cur_statement_one, cur_statement_time)
            get_cur_statement_one.end_stmt_posted_bal = (
                get_cur_statement_one.min_payment_ins_vat +
                get_cur_statement_one.min_payment_ins_interest +
                get_cur_statement_one.min_payment_ins_prin +
                get_cur_statement_one.min_payment_vat +
                get_cur_statement_one.min_payment_interest +
                get_cur_statement_one.min_payment_late_fee -
                get_cur_statement_one.min_payment_reverse +
                get_cur_statement_one.last_min_payment if get_cur_statement_one.last_min_payment_had_payoff == False else 0
            )

            get_cur_statement_one.min_payment_all = cal_minpayment_result(get_cur_statement_one,)
            print(vars(get_cur_statement_one))

            last_min_payment = get_cur_statement_one.last_min_payment
            cur_min_payment = get_cur_statement_one.min_payment_all
            get_all_statement_data[cur_statement_time] = get_cur_statement_one

            print("出账" + "第" + str(cur_statement_time + 1) + "期:end+++")
            #       处理账期，到下个账期初始化

            cur_statement_time = cur_statement_time + 1
            if cur_statement_time < len(statement_period):
                get_cur_statement_one = get_all_statement_data[cur_statement_time]
                get_cur_statement_one.start_statemet_day = statement_period[cur_statement_time].split("~")[0]
                get_cur_statement_one.end_statemet_day = statement_period[cur_statement_time].split("~")[1]
                get_cur_statement_one.last_min_payment = cur_min_payment
                get_cur_statement_one.statement_peroid = statement_period[cur_statement_time].split("~")[0] + "~" + \
                                                         statement_period[cur_statement_time].split("~")[1]

        elif get_one["path"] == "/v1.0/credit/cards/replacement":
            get_cur_statement_one.min_payment_fee_replace = get_cur_statement_one.min_payment_fee_replace + 2500000
            avilibale_credit_line = avilibale_credit_line - 2500000
        # elif get_one["path"] == "update_sql":
        #     get_sql = get_one["update_sql"]
        #     # 隔很多天计息
        #     if get_sql.count("cc_ins_installment_info") and get_sql.count("interest_date"):
        #         get_more_day_cal_interest = True

    print("查看下所有账期数据情况+++")
    for get_one1 in get_all_statement_data:
        print(vars(get_one1))
        print("+all_statement_data++")
