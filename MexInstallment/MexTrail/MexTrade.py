import math

import MexInitData

mpr = {3: 0.025, 6: 0.033333, 9: 0.0417, 12: 0.05}
# mpr = {3: 0.0499, 6: 0.0541, 9: 0.0583, 12: 0.0624}

def purchaseMSI(purchase_data_all, quantity, local_date_time, statement_period, cur_statement_time, amount):
    set_purchase_data_one = {}
    if quantity == 1 or quantity == 0:
        set_purchase_data_one = {"purchase_1_" + str(local_date_time):
                                     {statement_period[cur_statement_time]: {"interest_cal": 0.00,
                                                                             "vat_cal": 0.00,
                                                                             "ins_prin_cal": amount,
                                                                             "repaid_prin": 0.00,
                                                                             "repaid_interest_cal": 0.00,
                                                                             "repaid_vat_cal": 0.00,
                                                                             "ins_peroid": 1}},
                                 "quantity": quantity, "prin_amount": amount, "p_rate": 0}
    else:

        get_avg_ins_prin = int(round(amount / quantity, 0))
        amount_ins_prin = 0
        set_purchase_data_one_dict = {}
        get_tmp_str = statement_period[cur_statement_time]
        get_tmp_i = MexInitData.neum.index(get_tmp_str)
        for i in range(quantity):
            if i == quantity - 1:
                # 判断可忽略
                get_statment_period = MexInitData.neum[get_tmp_i + i]
                set_ins_prin = {get_statment_period: {"interest_cal": 0.00,
                                                      "vat_cal": 0.0,
                                                      "ins_prin_cal": int(
                                                          amount - amount_ins_prin),
                                                      "repaid_interest_cal": 0.00,
                                                      "repaid_vat_cal": 0.00,
                                                      "repaid_prin": 0,
                                                      "ins_peroid": (i + 1)}}
                set_purchase_data_one_dict.update(set_ins_prin)
            else:
                amount_ins_prin = amount_ins_prin + get_avg_ins_prin
                get_statment_period = MexInitData.neum[get_tmp_i + i]
                set_ins_prin = {get_statment_period: {"interest_cal": 0.00,
                                                      "vat_cal": 0.0,
                                                      "ins_prin_cal": get_avg_ins_prin,
                                                      "repaid_interest_cal": 0.00,
                                                      "repaid_vat_cal": 0.00,
                                                      "repaid_prin": 0,
                                                      "ins_peroid": (i + 1)}}
                set_purchase_data_one_dict.update(set_ins_prin)
        set_purchase_data_one = {
            "purchase_" + str(quantity) + "_" + str(local_date_time): set_purchase_data_one_dict,
            "quantity": quantity, "prin_amount": amount, "p_rate": 0 if quantity > 1 else 0}
    print(set_purchase_data_one)
    purchase_data_all.append(set_purchase_data_one)
    return purchase_data_all

#计算分期的息税本金
def purchaseTradeIns_cal_vat_interest_prin(quantity, amount):
    get_mpr = mpr[quantity]
    vat_interest_prin_list=[]
    balance=amount
    get_cal_part1 = math.pow(1 + get_mpr, quantity)
    #每期本金和利息之和
    avg_ins_all = round(math.prod([balance,get_mpr, get_cal_part1]) / (get_cal_part1 - 1), 0)
    for i in range(quantity):
        if i==quantity-1:
            interest = round(math.prod([balance, get_mpr]), 0)
            interest_vat = round(math.prod([interest, 0.16]), 0)
            get_one = {"interest_cal": interest, "vat_cal": interest_vat, "ins_prin_cal": (balance),"monthlyAmount":(balance+interest_vat)}

        else:
            interest = round(math.prod([balance, get_mpr]),0)
            interest_vat = round(math.prod([interest, 0.16]), 0)
            get_one={"interest_cal":interest,"vat_cal":interest_vat,"ins_prin_cal":(avg_ins_all-interest),"monthlyAmount":(balance+interest_vat)}
            balance=balance-(avg_ins_all-interest)
        vat_interest_prin_list.append(get_one)
    # print(vat_interest_prin_list)
    return vat_interest_prin_list
if __name__ == '__main__':
    purchaseTradeIns_cal_vat_interest_prin(3,12300)
def purchaseTradeIns(purchase_data_all, quantity, local_date_time, statement_period, cur_statement_time, amount):
    set_purchase_data_one = {}
    vat_interest_prin_list=purchaseTradeIns_cal_vat_interest_prin(quantity,amount)
    get_avg_ins_prin = int(round(amount / quantity, 0))
    amount_ins_prin = 0
    set_purchase_data_one_dict = {}
    get_tmp_str = statement_period[cur_statement_time]
    get_tmp_i = MexInitData.neum.index(get_tmp_str)
    for i in range(quantity):
        get_had_cal_vat_interest_prin=vat_interest_prin_list[i]
        if i == quantity - 1:
            # 判断可忽略
            get_statment_period = MexInitData.neum[get_tmp_i + i]
            set_ins_prin = {get_statment_period: {"interest_cal": get_had_cal_vat_interest_prin["interest_cal"],
                                                  "vat_cal": get_had_cal_vat_interest_prin["vat_cal"],
                                                  "ins_prin_cal": get_had_cal_vat_interest_prin["ins_prin_cal"],
                                                  "repaid_interest_cal": 0.00,
                                                  "repaid_vat_cal": 0.00,
                                                  "repaid_prin": 0,
                                                  "ins_peroid": (i + 1)}}
            set_purchase_data_one_dict.update(set_ins_prin)
        else:
            amount_ins_prin = amount_ins_prin + get_avg_ins_prin
            get_statment_period = MexInitData.neum[get_tmp_i + i]
            set_ins_prin = {get_statment_period: {"interest_cal": get_had_cal_vat_interest_prin["interest_cal"],
                                                  "vat_cal": get_had_cal_vat_interest_prin["vat_cal"],
                                                  "ins_prin_cal": get_had_cal_vat_interest_prin["ins_prin_cal"],
                                                  "repaid_interest_cal": 0.00,
                                                  "repaid_vat_cal": 0.00,
                                                  "repaid_prin": 0, "ins_peroid": (i + 1)}}
            set_purchase_data_one_dict.update(set_ins_prin)
    set_purchase_data_one = {
        "purchase_" + str(quantity) + "_" + str(local_date_time): set_purchase_data_one_dict,
        "quantity": quantity, "prin_amount": amount, "mpr_rate": mpr[quantity]}

    print(set_purchase_data_one)
    purchase_data_all.append(set_purchase_data_one)
    return purchase_data_all
