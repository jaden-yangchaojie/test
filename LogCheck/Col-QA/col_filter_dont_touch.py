import os
import pathlib
import sys
import time
import subprocess

# 执行一个Linux命令,如果出现returned non-zero exit status 1，是没有捞取到数据
view_filter_word = ["the auth info of transaction not found", "The number of mq delivery times is"
    , "credit view not find unsettled statement.",
                    "statement.activity.consume.msg.times.log.error"
                    ]

trading_filter_word = ["error.charge.interest.auth",
                       "Transaction rolled back because it has been marked as rollback-only",
                       "installment | refundAllocation fail."  # 合理的用户级锁
    , "min.paid.statements.can.not.be.empty.after.ignore.non.dq.statement",
                       "Ignore task process",
                       "CertPathValidatorException"
    , "Installment task processing occurs system error."
    , "Application run failed"
    , "post fail caused by auth apply status not pending"
    , "credit line is insufficient"
    , "secretID",
                       # "error.interest.comp.charge",
                       # "unifiedChargeFacade chargeInterestWithoutCal error"
                       # ,'Installment task processing occurs business error.',
                       #    "13130011000017697126","post update left repay plan fail",
                       # "Not statement date, repay plan can not be posted",
                       # "13130011000018717238","flow process biz error！post date adjust fail"
                       ]
statement_filter_word = ["total.payment.amount.calc.error.",
                         "Transaction rolled back because it has been marked as rollback-only.",

                         "DAY_CUT_SCHEDULE", ".aws.",
                         "CertPathValidatorException",
                         "Application run failed",
                         "openFlag:credit.view.statement.list.no.activity.open.flag",
                         "Origin tx not exist",
                         "auth.transaction.not.exist",
                         # "error.payment.statement.",
                         # "error.statement.payment.",
                         #
                         # "DELINQUENCY",
                         #  "Origin tx not exist",
                         # "error.process.charge.transaction"
                         ]
if __name__ == '__main__':
    # assert "123"==1
    get_path = os.getcwd()
    print(get_path)
    get_files_name = []
    for get_file_name in os.listdir(get_path):
        if ".txt" in get_file_name:
            get_files_name.append(get_file_name)
    print(get_files_name)
    for file_name in get_files_name:
        with open(file_name, 'r') as file:
            get_read = file.readline()
            while get_read:

                get_read = file.readline()
                tmp_bool = False
                if "view" in file_name:
                    for get_tmp in view_filter_word:
                        if get_tmp in get_read:
                            tmp_bool = True
                    if tmp_bool == False:
                        print(file_name)
                        print(get_read)
                # elif "trading" in file_name:
                #     for get_tmp in trading_filter_word:
                #         if get_tmp in get_read:
                #             tmp_bool=True
                #     if tmp_bool == False:
                #         print(file_name)
                #         print(get_read)
                elif "statement" in file_name:
                    for get_tmp in statement_filter_word:
                        if get_tmp in get_read:
                            tmp_bool = True
                    if tmp_bool == False:
                        print(file_name)
                        print(get_read)

        # file.write(get_info)
        # file.close()
