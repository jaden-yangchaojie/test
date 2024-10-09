import time
import subprocess
# 执行一个Linux命令,如果出现returned non-zero exit status 1，是没有捞取到数据
trading_filter_word=["error.charge.interest.auth",
             "Transaction rolled back because it has been marked as rollback-only"]
statement_filter_word=["total.payment.amount.calc.error.",
                       "Transaction rolled back because it has been marked as rollback-only.",
                       "error.payment.statement.",
                       "error.statement.payment."]
if __name__ == '__main__':
    file_name='statement-7f987cc7b9-97vq51728463852.txt'
    with open(file_name, 'r') as file:
        get_read=file.readline()
        while get_read:

            get_read = file.readline()
            tmp_bool=False
            if "trading" in file_name:
                for get_tmp in trading_filter_word:
                    if get_tmp in get_read:
                        tmp_bool=True
            if "statement" in file_name:
                for get_tmp in statement_filter_word:
                    if get_tmp in get_read:
                        tmp_bool=True

            if tmp_bool==False:
                print(get_read)

        # file.write(get_info)
        # file.close()



