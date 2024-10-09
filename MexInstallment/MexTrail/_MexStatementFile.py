import json

if __name__ == '__main__':
    get_one="/Users/ycj/pytest/pytest/MexInstallment/MexTrail/ceshi_statement_file.txt"
    with open(get_one , 'r') as file:
        content = file.read()
        get_data=json.loads(content)
        balanceSummaryInfo=get_data["balanceSummaryInfo"]
        balanceSummaryInfo = eval(balanceSummaryInfo)
        print(balanceSummaryInfo)

        statementInfo = get_data["statementInfo"]
        print(statementInfo)

        installmentDetailSummaryInfo = get_data["installmentDetailSummaryInfo"]
        installmentDetailSummaryInfo=eval(installmentDetailSummaryInfo)
        print(installmentDetailSummaryInfo)

        transactionDetailSummaryInfo = get_data["transactionDetailSummaryInfo"]
        transactionDetailSummaryInfo = eval(transactionDetailSummaryInfo)
        transactionDetailList=transactionDetailSummaryInfo["transactionDetailList"]
        for get_one in transactionDetailList:
            print(str(get_one["type"])+" "+str(get_one["billingAmount"]))

        file.close()
