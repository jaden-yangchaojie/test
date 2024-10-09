import json
import math
import sys

from MexInstallment.MexTrail import CurrentStatement
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
    c1 = 0
    c2 = 0
    c3 = 0
    if get_cur_statement_one.dq_is == False:
        c1 = (end_stmt_posted_bal - ins_all - vat - interest) * 1.5 / 100 + ins_all + vat + interest
        c2 = credit_limit_amt * 1.25 / 100 + ins_all
        c3 = (end_stmt_posted_bal - ins_all - interest - vat - fee) * 1.6 / 100 + interest + vat + fee + ins_all
    else:
        unpaid_min_pmt_bal = get_cur_statement_one.last_min_payment
        c1 = (end_stmt_posted_bal - ins_all - interest - vat - unpaid_min_pmt_bal) * 1.5 / 100 + interest + vat + unpaid_min_pmt_bal + ins_all
        c2 = credit_limit_amt * 1.25 / 100 + unpaid_min_pmt_bal + ins_all
        c3 = (
                     end_stmt_posted_bal - ins_all - interest - vat - fee - unpaid_min_pmt_bal) * 1.6 / 100 + interest + vat + fee + unpaid_min_pmt_bal + ins_all

    print("按元来计算单位")
    print("bal:"+str(end_stmt_posted_bal))
    print("c1:" + str(c1))
    print("c2:" + str(c2))
    print("c3:" + str(c3))
    if end_stmt_posted_bal <= 0:
        return 0
    elif end_stmt_posted_bal <= 100:
        return end_stmt_posted_bal
    elif c2 > end_stmt_posted_bal:
        tmp = max(c1, c3)
        if tmp < 100:
            return 100
        else:
            return tmp
    else:
        tmp = max(c1, c2, c3)
        if tmp < 100:
            return 100
        else:
            return tmp
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
    c5=100
    # print(json.loads(get_cur_statement_one))
    if get_cur_statement_one.dq_is == False:
        c1 = (end_stmt_posted_bal - ins_all - vat - interest) * 1.5 / 100 + ins_all + vat + interest
        c2 = credit_limit_amt * 1.25 / 100
        c3 = (end_stmt_posted_bal - ins_all - interest - vat - fee) * 1.6 / 100 + interest + vat + fee + ins_all
    else:
        print("DQ了")
        unpaid_min_pmt_bal = get_cur_statement_one.last_min_payment
        c1 = (
                     end_stmt_posted_bal - ins_all - interest - vat - unpaid_min_pmt_bal) * 1.5 / 100 + interest + vat + unpaid_min_pmt_bal + ins_all
        c2 = credit_limit_amt * 1.25 / 100 + unpaid_min_pmt_bal
        c3 = (
                     end_stmt_posted_bal - ins_all - interest - vat - fee - unpaid_min_pmt_bal) * 1.6 / 100 + interest + vat + fee + unpaid_min_pmt_bal + ins_all
    print("按元来计算单位")
    print("bal:" + str(end_stmt_posted_bal))
    print("c1:"+str(c1))
    print("c2:" + str(c2))
    print("c3:" + str(c3))
    if end_stmt_posted_bal<=0:
        return 0
    elif end_stmt_posted_bal<=100:
        return end_stmt_posted_bal
    elif c2>end_stmt_posted_bal:
       tmp= max(c1,c3)
       if tmp<100:
           return  100
       else:
           return tmp
    else:
        tmp = max(c1,c2,c3)
        if tmp < 100:
            return 100
        else:
            return tmp
def cal_adb(adbCalculationList,interestCalculation):
    adb_total=0
    for get_one in adbCalculationList:
        adb_total=float(get_one["endBalance"])+adb_total

    get_abd=round(adb_total / len(adbCalculationList), 2)

    print("adb")
    print(get_abd)
    start_udi =float(interestCalculation["startUdi"])
    end_udi = float(interestCalculation["endUdi"])
    apr=float(interestCalculation["apr"])
    daysInterval=int(interestCalculation["daysInterval"])

    inflation = round(math.fabs(float(end_udi) / float(start_udi)) - 1, 6)
    real_interest_rate = round(apr / 12 - inflation, 6)
    inflationNonTax = inflation
    daily_interest = get_abd * real_interest_rate / 30
    realdailyInt = round(daily_interest * daysInterval, 2)
    interest_not_tax = round((get_abd * inflation / 30) * daysInterval, 2)
    total_interest = round(realdailyInt + interest_not_tax, 2)
    interest_vat = realdailyInt * 0.16

    print("realdailyInt:"+str(realdailyInt))
    print("interest_not_tax:" + str(interest_not_tax))
    print("interest_vat:" + str(interest_vat))
    print("total_interest:" + str(total_interest))





if __name__ == '__main__':
    get_one="/Users/ycj/pytest/pytest/MexInstallment/MexTrail/ceshi.txt"
    with open(get_one , 'r') as file:
        content = file.read()
        get_data=json.loads(content)
        get_cur_statement_one= CurrentStatement.CurrentStatement()
        minPayment=get_data["data"]["minPayment"]
        get_cur_statement_one.end_stmt_posted_bal= float(minPayment["endStatementBalance"])
        get_cur_statement_one.min_payment_ins_vat=float(minPayment["insVat"])
        get_cur_statement_one.min_payment_ins_interest = float(minPayment["insInterest"])
        get_cur_statement_one.min_payment_ins_prin = float(minPayment["insPrincipal"])

        get_cur_statement_one.min_payment_principal = float(minPayment["principal"])
        get_cur_statement_one.min_payment_vat = float(minPayment["vat"])
        get_cur_statement_one.min_payment_interest = float(minPayment["interest"])
        get_cur_statement_one.min_payment_fee_replace=0
        get_cur_statement_one.min_payment_late_fee= float(minPayment["fee"])
        get_cur_statement_one.credit_line = float(minPayment["creditLimit"])
        get_cur_statement_one.last_min_payment= float(minPayment["unpaidMinPayment"])
        if minPayment["accountDQ"]=="DQ":
            get_cur_statement_one.dq_is=True
        else:
            get_cur_statement_one.dq_is = False
        print("old")
        get_min_payment=cal_minpayment_result_old(get_cur_statement_one)
        print(get_min_payment)
        print("new")
        get_min_payment = cal_minpayment_result(get_cur_statement_one)
        print("min payment")
        print(get_min_payment)
        file.close()
        adbCalculationList = get_data["data"]["adbCalculationList"]
        interestCalculation = get_data["data"]["interestCalculation"]
        cal_adb(adbCalculationList,interestCalculation)
