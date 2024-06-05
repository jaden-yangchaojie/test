import InitData


def purchase(purchase_data_all,quantity,local_date_time,statement_period,cur_statement_time,amount):

    set_purchase_data_one = {}
    if quantity == 1 or quantity == 0:
        set_purchase_data_one = {"purchase_1_" + str(local_date_time):
                                     {statement_period[cur_statement_time]: {"interest_cal": 0.00,
                                                                             "late_interest_cal": 0.00,
                                                                             "ins_total_prin": amount,
                                                                             "repaid_prin": 0.00,
                                                                             "repaid_interest_cal": 0.00,
                                                                             "repaid_late_interest_cal": 0.00,
                                                                             "ins_peroid": 1}},
                                 "quantity": quantity, "prin_amount": amount, "p_rate": 0}
    else:
        get_avg_ins_prin = int(round(amount / quantity, 0))
        amount_ins_prin = 0
        set_purchase_data_one_dict = {}
        get_tmp_str = statement_period[cur_statement_time]
        get_tmp_i = InitData.neum.index(get_tmp_str)
        for i in range(quantity):
            if i == quantity - 1:
                # 判断可忽略
                get_statment_period= InitData.neum[get_tmp_i + i]
                set_ins_prin = {get_statment_period: {"interest_cal": 0.00,
                                                                        "late_interest_cal": 0.00,
                                                                        "ins_total_prin": int(
                                                                            amount - amount_ins_prin),
                                                                        "repaid_interest_cal": 0.00,
                                                                        "repaid_late_interest_cal": 0.00,
                                                                        "repaid_prin": 0,
                                                                        "ins_peroid": (i + 1)}}
                set_purchase_data_one_dict.update(set_ins_prin)
            else:
                amount_ins_prin = amount_ins_prin + get_avg_ins_prin
                get_statment_period = InitData.neum[get_tmp_i + i]
                set_ins_prin = {get_statment_period: {"interest_cal": 0.00,
                                                                        "late_interest_cal": 0.00,
                                                                        "repaid_interest_cal": 0.00,
                                                                        "repaid_late_interest_cal": 0.00,
                                                                        "ins_total_prin": get_avg_ins_prin,
                                                                        "repaid_prin": 0, "ins_peroid": (i + 1)}}
                set_purchase_data_one_dict.update(set_ins_prin)
        # 取最低利率作为购买利率#todo  d8b3c4e7-df63-48d1-a2ad-2664629683d0

        # get_cur_time_line = datetime.datetime.strptime(, "%Y-%m-%d %H:%M:%S")
        # get_cur_time_line_year_month = get_cur_time_line.split("-")[0] + "-" + \
        #                                get_cur_time_line.split("-")[1]
        # month_rate = gov_rate_config[get_cur_time_line_year_month] if gov_rate_config[
        #                                                                   get_cur_time_line_year_month] < \
        #                                                               get_purchase_data_one[
        #                                                                   "p_rate"] else get_purchase_data_one["p_rate"]

        set_purchase_data_one = {
            "purchase_" + str(quantity) + "_" + str(local_date_time): set_purchase_data_one_dict,
            "quantity": quantity, "prin_amount": amount, "p_rate": 0.348 if quantity > 1 else 0}
    print(set_purchase_data_one)
    purchase_data_all.append(set_purchase_data_one)
    return purchase_data_all