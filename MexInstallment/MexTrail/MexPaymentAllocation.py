# PaymentOrderList = ["vat",
#                     "card_replacement_fee",
#                     "late_fee",
#                     "card_management_fee",
#                     "late_interest",
#                     "interest",
#                     "posted_prin"
#                     ]
import copy

# 非DQ
PaymentOrderList = [#分期交易
                    "min_payment_ins_vat",
                    "min_payment_ins_interest",
                    "min_payment_ins_prin",

                    #普通交易
                    "min_payment_vat",
                    "min_payment_fee_replace",
                    "min_payment_late_fee",
                    "min_payment_interest",

                    "min_payment_principal"
                    ]


# 已出账还款
def ins_handler_had_accounting_allocation(statement_period, cur_statement_time, purchase_data_all,
                                          get_all_statement_data, amount):
    get_cur_statment = None
    get_pre_statment = None
    cur_statement_period = statement_period[cur_statement_time]
    # 查找当期账期
    for get_one_statement in get_all_statement_data:
        if get_one_statement.end_statemet_day == cur_statement_period.split("~")[1]:
            get_cur_statment = get_one_statement
            break

    if cur_statement_period in statement_period:
        get_cur_statement_number = statement_period.index(cur_statement_period)
        # 第一期做为前期，其他设置前期还款分配
        get_pre_statement_period = statement_period[
            get_cur_statement_number] if get_cur_statement_number == 0 else statement_period[
            get_cur_statement_number - 1]
    for get_one_statement in get_all_statement_data:
        if get_one_statement.statement_peroid == get_pre_statement_period:
            get_pre_statment = get_one_statement
            break
    get_pre_statment_dict = vars(get_pre_statment)
    for get_pay_order in PaymentOrderList:

        if get_pay_order == "min_payment_ins_vat":
            if amount > 0:
                for get_purchase_data_one in purchase_data_all:
                    if amount > 0:
                        for get_key in get_purchase_data_one.keys():
                            if get_key.count("purchase_"):
                                get_ins_repaid_info = get_purchase_data_one[get_key]
                                get_veryone_statement_list = sorted(get_ins_repaid_info,
                                                                    key=lambda x: get_ins_repaid_info[x][
                                                                        "ins_peroid"])
                                # 当前账期存在
                                if cur_statement_period in get_veryone_statement_list:
                                    get_cur_statement_number = get_veryone_statement_list.index(
                                        cur_statement_period)
                                    # 第一期做为前期，其他设置前期
                                    get_pre_statement_period = get_veryone_statement_list[
                                        get_cur_statement_number] if get_cur_statement_number == 0 else \
                                        get_veryone_statement_list[
                                            get_cur_statement_number - 1]

                                    get_one_info = get_ins_repaid_info[get_pre_statement_period]
                                    if get_one_info["vat_cal"] == get_one_info["repaid_vat_cal"]:
                                        continue
                                    elif amount > 0:
                                        amount = amount - int(get_one_info["vat_cal"])
                                        if amount > 0:
                                            get_one_info = get_ins_repaid_info[get_pre_statement_period]
                                            get_one_info["repaid_vat_cal"] = get_one_info["vat_cal"]
                                        else:
                                            get_one_info["repaid_vat_cal"] = get_one_info[
                                                                                 "repaid_vat_cal"] - amount
                                    get_ins_repaid_info[get_pre_statement_period] = get_one_info
        elif get_pay_order == "min_payment_ins_interest":
            # get_one_statement.min_payment_all_repaid = get_one_statement.min_payment_all
            if amount > 0:
                for get_purchase_data_one in purchase_data_all:
                    if amount > 0:
                        for get_key in get_purchase_data_one.keys():
                            if get_key.count("purchase_"):
                                get_ins_repaid_info = get_purchase_data_one[get_key]
                                get_veryone_statement_list = sorted(get_ins_repaid_info,
                                                                    key=lambda x: get_ins_repaid_info[x][
                                                                        "ins_peroid"])
                                # 当前账期存在
                                if cur_statement_period in get_veryone_statement_list:
                                    get_cur_statement_number = get_veryone_statement_list.index(
                                        cur_statement_period)
                                    # 第一期做为前期，其他设置前期
                                    get_pre_statement_period = get_veryone_statement_list[
                                        get_cur_statement_number] if get_cur_statement_number == 0 else \
                                        get_veryone_statement_list[
                                            get_cur_statement_number - 1]

                                    get_one_info = get_ins_repaid_info[get_pre_statement_period]
                                    if get_one_info["interest_cal"] == get_one_info["repaid_interest_cal"]:
                                        continue
                                    elif amount > 0:
                                        amount = amount - int(get_one_info["interest_cal"])
                                        if amount > 0:
                                            get_one_info = get_ins_repaid_info[get_pre_statement_period]
                                            get_one_info["repaid_interest_cal"] = get_one_info["interest_cal"]
                                        else:
                                            get_one_info["repaid_interest_cal"] = get_one_info[
                                                                                      "repaid_interest_cal"] - amount
                                    get_ins_repaid_info[get_pre_statement_period] = get_one_info
        elif get_pay_order == "min_payment_ins_prin":
            if amount > 0:
                for get_purchase_data_one in purchase_data_all:
                    if amount > 0:
                        for get_key in get_purchase_data_one.keys():
                            if get_key.count("purchase_"):
                                get_ins_repaid_info = get_purchase_data_one[get_key]
                                get_veryone_statement_list = sorted(get_ins_repaid_info,
                                                                    key=lambda x: get_ins_repaid_info[x][
                                                                        "ins_peroid"])
                                if cur_statement_period in get_veryone_statement_list:
                                    get_cur_statement_number = get_veryone_statement_list.index(
                                        cur_statement_period)
                                    get_pre_statement_period = ""
                                    if get_cur_statement_number == 0:
                                        get_pre_statement_period = get_veryone_statement_list[
                                            get_cur_statement_number]
                                    else:
                                        get_pre_statement_period = get_veryone_statement_list[
                                            get_cur_statement_number - 1]

                                if cur_statement_period in get_ins_repaid_info.keys():
                                    get_one_info = get_ins_repaid_info[get_pre_statement_period]
                                    if get_one_info["repaid_prin"] == get_one_info["ins_prin_cal"]:
                                        continue
                                    elif amount > 0:
                                        amount_less_0 = copy.deepcopy(amount)
                                        amount = amount - (int(get_one_info["ins_prin_cal"]) - int(
                                            get_one_info["repaid_prin"]))
                                        if amount >= 0:
                                            get_one_info = get_ins_repaid_info[get_pre_statement_period]
                                            get_one_info["repaid_prin"] = get_one_info["ins_prin_cal"]

                                        else:
                                            # get_one_info["repaid_prin"] = int(get_one_info["repaid_prin"]) - amount
                                            get_one_info["repaid_prin"] = amount_less_0
                                    get_ins_repaid_info[get_pre_statement_period] = get_one_info

        elif get_pre_statment_dict[get_pay_order] > 0 and amount > 0:
            amount = amount - get_pre_statment_dict[get_pay_order]

    return purchase_data_all


# 本金退款
def ins_refund_prin(cur_statement_period, purchase_data_all, get_all_statement_data, amount):
    if amount > 0:
        for get_purchase_data_one in purchase_data_all:
            if amount > 0:
                for get_key in get_purchase_data_one.keys():
                    if get_key.count("purchase_"):
                        get_ins_repaid_info = get_purchase_data_one[get_key]
                        get_veryone_statement_list = sorted(get_ins_repaid_info,
                                                            key=lambda x: get_ins_repaid_info[x][
                                                                "ins_peroid"])

                        for get_statement_period_one in get_veryone_statement_list:
                            # # 第一期做为前期，其他设置前期
                            # get_pre_statement_period = get_veryone_statement_list[get_cur_statement_number] if get_cur_statement_number == 0 else \
                            #     get_veryone_statement_list[
                            #         get_cur_statement_number - 1]
                            get_one_info = get_ins_repaid_info[get_statement_period_one]
                            if int(get_one_info["ins_prin_cal"]) == int(get_one_info["repaid_prin"]):
                                continue
                            elif amount > 0:
                                amount_less_0 = copy.deepcopy(amount)
                                amount = amount - (int(get_one_info["ins_prin_cal"]) - int(get_one_info["repaid_prin"]))

                                if amount >= 0:
                                    get_one_info = get_ins_repaid_info[get_statement_period_one]
                                    get_one_info["repaid_prin"] = get_one_info["ins_prin_cal"]
                                else:
                                    # get_one_info["repaid_prin"] = int(get_one_info["repaid_prin"]) - amount
                                    get_one_info["repaid_prin"] = amount_less_0
                            get_ins_repaid_info[get_statement_period_one] = get_one_info
    return purchase_data_all, amount


def handler_payment(statement_period, cur_statement_time, purchase_data_all, get_all_statement_data, amount_payment):
    cur_statement_period = statement_period[cur_statement_time]

    # 先还已出账账单，再还已经入账的未出账单（包含本金、费用），有多的钱再还未入账的分期本金。剩余的钱作为溢缴款转到存款账户
    get_cur_statment = None
    for get_one_statement in get_all_statement_data:
        if get_one_statement.end_statemet_day == cur_statement_period.split("~")[1]:
            get_cur_statment = get_one_statement
            break
    # 先还已出账账单
    if amount_payment > 0 and cur_statement_time > 0 and get_cur_statment.last_min_payment_had_payoff == False:
        amount = amount_payment - get_cur_statment.last_min_payment

        if amount > 0:
            get_cur_statment.last_min_payment_had_payoff = True
            get_cur_statment.last_min_payment=0
        else:
            get_cur_statment.last_min_payment_had_payoff = False
            get_cur_statment.last_min_payment = get_cur_statment.last_min_payment-amount_payment


        purchase_data_all = ins_handler_had_accounting_allocation(statement_period, cur_statement_time,
                                                                  purchase_data_all,
                                                                  get_all_statement_data,
                                                                  get_cur_statment.last_min_payment)

        if amount > 0:
            # todo 已经入账的未出账单
            if cur_statement_time == 0:
                print()
            elif cur_statement_time > 0:
                print()
                # get_cur_statment=get_all_statement_data[cur_statement_time]

    # 退还未入账的分期本金
    if amount_payment > 0:
        if cur_statement_time == 0:
            get_cur_statment.min_payment_ins_prin = get_cur_statment.min_payment_ins_prin + amount
        for get_one_statement in get_all_statement_data:
            if get_one_statement.min_payment_reverse == (
                    get_one_statement.min_payment_all + get_one_statement.last_min_payment):
                continue
            else:
                get_one_statement_copy = vars(get_one_statement)
                purchase_data_all, amount = ins_refund_prin(cur_statement_period, purchase_data_all,
                                                            get_all_statement_data, amount)

    for get_one1 in purchase_data_all:
        print(get_one1)
        print("还款操作 每笔还款的信息+++")
    # for get_one1 in get_all_statement_data:
    #     print(vars(get_one1))
    #     print("all+++")
    print()


def handler_refund(statement_period, cur_statement_time, purchase_data_all, get_all_statement_data, amount):
    cur_statement_period = statement_period[cur_statement_time]
    # 先还已出账账单，再按照交易时间从早到晚还剩余分期交易的本金，有多的钱再还已入账的费用。剩余的钱作为溢缴款转到存款账户
    get_cur_statment = None
    for get_one_statement in get_all_statement_data:
        if get_one_statement.end_statemet_day == cur_statement_period.split("~")[1]:
            get_cur_statment = get_one_statement
            break
    # 先还已出账账单
    if amount > 0 and cur_statement_time > 0 and get_cur_statment.last_min_payment_had_payoff == False:
        amount = amount - get_cur_statment.last_min_payment
        if amount > 0:
            get_cur_statment.last_min_payment_had_payoff == True
        handler_accounting_amount = get_cur_statment.last_min_payment
        purchase_data_all = ins_handler_had_accounting_allocation(statement_period, cur_statement_time,
                                                                  purchase_data_all,
                                                                  get_all_statement_data, handler_accounting_amount)
    # 退本金
    if amount > 0:
        if cur_statement_time == 0:
            get_cur_statment.min_payment_ins_prin = get_cur_statment.min_payment_ins_prin + amount
        purchase_data_all, amount = ins_refund_prin(cur_statement_period, purchase_data_all, get_all_statement_data,
                                                    amount)
    # 多的钱再还已入账的费用
    if amount > 0:
        if cur_statement_time == 0:
            # todo
            print()
    return purchase_data_all, get_all_statement_data
