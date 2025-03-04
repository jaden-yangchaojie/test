
from StoriStatement import Statement
from StoriCif import StoriCif
from StoriBill import StoriBill
from StoriTrade import convertToTradingType, TradingType
from datetime import datetime, time
from StoriUtils import round_to_even
import json
from typing import List  

def checkVariables(data, variables) :
    if (type(data) is str) :
        if (data.startswith("${") and data in variables) :
            data = variables[data]
    elif (type(data) is dict) :
        for key, value in data.items() :
            data[key] = checkVariables(value, variables)
    return data

class StoriUser:
    def __init__(self, accountId:str, cif :StoriCif, startTime, forRecovery=False):  
        self.accountId = accountId
        self.userName = accountId
        self.cif = cif
        self.curStatement:Statement = None
        self.statementList : List[Statement] = []
        if forRecovery == False :
            self.addStatement(startTime)
            self.curStatement.handleOpenCard()
        self.insIndex = -1
        self.billedNumber = 0
    
    def addStatement(self, startTime=None, createTime = None) :
        lastStatement = self.curStatement
        if startTime == None and lastStatement:
            startTime = lastStatement.curTime
        self.curStatement = Statement(startTime, self.cif, lastStatement)
        self.curStatement.createTime = createTime
        self.statementList.append(self.curStatement)
        return self.curStatement

    def changeTime(self, systime: datetime, autoGenStatement = False) :
        self.checkIns(systime)
        curDate = systime.date()
        if autoGenStatement :
            if curDate != self.curStatement.curDate :                
                while curDate > self.curStatement.bill.statementDate :
                    statementTime = datetime.combine(self.curStatement.bill.statementDate, time(0,1))
                    self.curStatement.changeTime(statementTime)
                    self.genBill()
        if systime.date() < self.curStatement.curDate :
            print(self.accountId, self.curStatement.curDate, systime.date())
        # else :
        #     self.curStatement.changeTime(systime)
        self.curStatement.changeTime(systime)
    
    def handleIns(self, insDataList = None) :
        self.insIndex = -1
        self.insDataList = insDataList
        if len(self.insDataList) > 0 :
            self.insIndex = 0

    def benefits(self, benefitList = []) :
        for benefit in benefitList :
            data = {}
            status = benefit["status"]
            benefit_type = benefit["benefit_type"]
            benefit_name = benefit["benefit_name"]
            benefit_no = benefit["benefit_no"]
            benefit_snapshot = benefit["benefit_snapshot"]
            instanceRules = json.loads(benefit_snapshot)
            usageRules = instanceRules["usageRules"].replace("'","\"")
            usageRules = json.loads(usageRules)
            instanceRules["usageRules"]=usageRules
            data["instanceRules"] = instanceRules
            data["instance"] = {"benefitName":benefit_name, "benefitType":benefit_type}
            data["benefit_no"] = benefit_no
            # data["usage_time"] =  benefit["usage_time"].to_pydatetime() if benefit["usage_time"] != None else None
            # data["usage_amount"] = benefit["usage_amount"]

            self.curStatement.handleMarketingAddBenefit(data)
            if status == "CANCELED" :
                self.curStatement.handleMarketingCancelBenefit(benefit_no)
            elif status == "EXPIRED" :
                self.curStatement.handleMarketingExpiredBenefit(benefit_no)

    def exchangeCard(self, data, cardId) :
        self.curStatement.handleChangeCard(data, cardId)

    def activeCard(self, data) :
        cardId = data["cardId"]
        self.curStatement.handleActiveCard(cardId)

    def createDQ(self) :
        self.curStatement.handleDQCreate()

    def updateDQ(self) :
        self.curStatement.handleDQUpdate()

    def genBill(self, isLast = False) :
        if self.curStatement.isBilled :
            return
        
        statementTime = datetime.combine(self.curStatement.bill.statementDate, time(0,1))
        self.changeTime(statementTime)
        self.curStatement.generateBill()
        self.billedNumber += 1

        if not isLast :
            self.addStatement()
    
    def handleMarketingRequestData(self, path, data, variables) :
        if (path == "/v1.0/backoffice-ng/credit/marketing/benefits") :
            data = checkVariables(data, variables)
            instanceRules = data["instanceRules"]
            usageRules = instanceRules["usageRules"].replace("'","\"")
            usageRules = json.loads(usageRules)
            usageRules = checkVariables(usageRules, variables)
            instanceRules["usageRules"] = usageRules
            self.curStatement.handleMarketingAddBenefit(data)
        elif (path == "/v1.0/backoffice-ng/credit/marketing/benefits/revisal/benefit") :
            self.curStatement.handleMarketingCancelBenefit()
        elif (path == "/v1.0/backoffice-ng/credit/marketing/activity") :
            print("活动")

    def tradingInsRequestData(self, data, variables) :
        tid = None
        if "referenceId" in data :
            tid = data["referenceId"]
            tid = checkVariables(tid, variables)
        self.curStatement.handleInstallmentTrading(tid, data)

    def tradingAdjRequestData(self, data) :
        # 调整交易(credit)
        # if path == '/backoffice/dfl-ng/credit/adjustment' :
            # print("app adjustment")
        amountDetail = data["amountDetail"]
        # tid = data["requestId"]
        # tid = checkVariables(tid, variables)

        for detail in amountDetail :
            type = detail["type"]
            subType = detail["subType"]
            amount = int(detail["amount"]["total"])/100
            self.curStatement.handleAdjustmentTrading(amount, type, subType)

    def tradingAppRequestData(self, path, data, variables, tid = None) :
        txnAmount = data['txnAmount']
        txnAmount = checkVariables(txnAmount, variables) 

        if type(txnAmount) is str :
            txnAmount = int(txnAmount)
        amount = txnAmount/100.0
        
        # 正向交易
        if path == '/v1.0/credit/authorizations':
            print("app auth", amount)
            self.curStatement.handleOriginTrading(amount, isPomelo=False, tid=tid, sync=False)

        # 逆向交易(payment)
        elif path == '/v1.0/credit/payments':
            print("app payments", amount)

            # timeString:str = data['txnBizDetail']["txnTime"].split(".")[0]
            # txnTime = datetime.strptime(timeString,  "%Y-%m-%dT%H:%M:%S") - timedelta(hours=6)

            self.curStatement.handleOriginTrading(amount, tradingType=TradingType.PAYMENT, isPomelo=False)
        else :
            # 交易入账
            if path == '/v1.0/credit/authorizations/posting':
                print("app posting", amount)
                transcationID = data["relTxnId"]
                transcationID = checkVariables(transcationID, variables)
                self.curStatement.handlePostingTrading(transcationID, amount = amount, isPomelo=False)
            else :
                print(path)
                assert 0

    def tradingPomeloRequestData(self, path, data:dict, variables:dict) :
        if path == '/transactions/v1/notifications' :
            data = data["event_detail"]

        transcation = data["transaction"]
        amount = float(data["amount"]["local"]["total"])

        tradingType = transcation["type"]

        transcationID = checkVariables(transcation["id"], variables)
      
        original_transaction_id = checkVariables(transcation["original_transaction_id"], variables)

        installments = data.get("installments")
            
        # 正向交易（purchase/purchase_increase）
        if path == '/transactions/authorizations' :
            if original_transaction_id == None or original_transaction_id=="":
                print("pomelo auth purchase", amount)
                self.curStatement.handleOriginTrading(amount, tid=transcationID, sync=False, installments=installments)
            else :
                # 商户侧的增量预授权
                print("pomelo auth purchase increase", amount)
                self.curStatement.handleChangeTrading(tid = transcationID, originTid = original_transaction_id, amount = amount, fromPomelo = False)
        # 交易入账 
        elif path == '/backoffice/dfl-ng/credit/authorizations/posting' :
            print("pomelo posting", amount)
            self.curStatement.handlePostingTrading(transcationID, amount = amount, installments = installments)
        # 正向交易adjustment-increase
        elif path == '/transactions/adjustments/debit':
            # pomelo发现入账金额于授权金额不一致时调增，调增金额0，延长预授权有效期
            print("pomelo purchase-increase", amount)
            self.curStatement.handleChangeTrading(tid = transcationID, originTid = original_transaction_id, amount = amount)
        # 撤销交易(reject/reversal)
        elif path == '/transactions/v1/notifications':
            # 交易撤销（比如请求超时的情况）
            # tradingType : "PURCHASE"/"REFUND"/"PAYMENT"
            # data['status'] : "REJECTED"
            print("pomelo reject or reversal", amount)
            assert(data['status'] == "REJECTED")
            self.curStatement.handleRejectedTrading(transcationID, amount = amount)
        # 逆向交易(purchase-decrease/payment/refund)  
        elif path == '/transactions/adjustments/credit':
            if (tradingType == "PAYMENT") :
                print("pomelo PAYMENT", amount)
                self.curStatement.handleOriginTrading(amount, tradingType=TradingType.PAYMENT, tid=transcationID, sync=False)
            elif (tradingType == "REFUND") :
                print("pomelo REFUND", amount)
                self.curStatement.handleOriginTrading(amount, tradingType=TradingType.REFUND, tid=transcationID, sync=False)
            else :
                # pomelo发现入账金额于授权金额不一致时调减，商户主动调减，商户撤销交易， 预授权到期pomelo撤销交易
                print("pomelo purchase-decrease", amount)
                self.curStatement.handleChangeTrading(tid = transcationID, originTid = original_transaction_id, amount = -amount)
        else :
            print(path)
            assert 0

    # 数据库data
    def trading(self, data) :
        isPomelo = data["channel"] == "POMELO"
        activityType = data["type"]
        sub_type = data["sub_type"] if "sub_type" in data else ""
        action_type = data["action_type"]
        tid = data["reference_id"] if "reference_id" in data else None
        ref_order_id = data["ref_order_id"] if "ref_order_id" in data else tid
        amt = round_to_even(data["amt"]/100)
        status = data["status"] if  "status" in data else ""
        effective_time_local = data["effective_time_local"].to_pydatetime()
        curStatement = self.curStatement

        if status == "rejected" :
            return
        
        if sub_type == "OPEN_FEE" :
            # if activityType == "ADJUSTMENT" : 
            #     curStatement.handleOpenCard()
            return

        if sub_type == "CARD_REPLACEMENT_FEE" :
            # if activityType == "CARD_REPLACEMENT_FEE" :
                # curStatement.handleChangeCard({"reason":"LOST"}, self.cardId)
                # curStatement.handleActiveCard(self.cardId)
                # self.cardId += 1
            return

        if activityType.startswith("ADJ") :
            curStatement.handleAdjustmentTrading(amount=amt, type=activityType, subType=sub_type)
            return

        if sub_type == "LATE_FEE" :
            if not activityType in ["LATE_FEE", "VAT_LATE_FEE"] :
                assert(0)
            return

        if sub_type == "INTEREST" :
            # curStatement.addCheckData(activityType, row)
            if not activityType in ["INTEREST", "VAT_INT"] :
                assert(0)
            return

        if "VAT" in activityType :
                assert(0)
        
        tradingType = convertToTradingType(typeStr=activityType, subType=sub_type)

        assert(tradingType != None)

        if action_type == "create" :
            if activityType == "PAYMENT" and isPomelo == False :
                effective_time_local = data["transaction_local_time"].to_pydatetime()
            curStatement.handleOriginTrading(amount=amt, tradingType=tradingType, isPomelo=isPomelo, tid=tid, sync=(status == "posted"), curTime=effective_time_local)
        elif action_type == "posting" :
            curStatement.handlePostingTrading(tid=tid, amount=amt, isPomelo=isPomelo, curTime=effective_time_local)
        # elif action_type == "createAndPosting" :
            # curStatement.handleOriginTrading(amount=amt, tradingType=tradingType, isPomelo=isPomelo, tid=tid, sync=True, curTime=effective_time_local)
        else :
            ref_order_id = tid
            if action_type == "incrementAmount" :
                curStatement.handleChangeTrading(tid=tid, originTid=ref_order_id, amount=amt, fromPomelo=isPomelo)
            elif action_type == "reduceAmount" :
                if status == "canceled" and amt == 0:
                    curStatement.handleRejectedTrading(tid=tid, cancel=True)
                else :
                    curStatement.handleChangeTrading(tid=tid, originTid=ref_order_id, amount=-amt, fromPomelo=isPomelo)
            else :
                assert(0)
                print()

    def checkIns(self, effective_time_local) :
        while self.insIndex != -1 and self.insDataList[self.insIndex]["apply_time_local"].to_pydatetime() < effective_time_local :
            insData = self.insDataList[self.insIndex]
            tid = insData["reference_id"]
            self.curStatement.handleInstallmentTrading(tid, insData)
            self.insIndex += 1
            if self.insIndex >= len(self.insDataList) :
                self.insIndex = -1


    def getDQInfo(self) :
        dqDays = self.cif.getDQDays()
        dqBucket = self.cif.getDQBucket()
        dqDueBucket = self.cif.getDQDueBucket()
        blockCodes = self.cif.getBlockCodeList()

        return (dqDays, dqBucket, dqDueBucket, blockCodes)
    
    def getLimitInfo(self) :
        limit = round_to_even(self.cif.creditLine * 100, 0)
        available = round_to_even(self.cif.availableLimit * 100, 0)
        return (limit, available)
    
    def getLastBillStatement(self) :
        statement = self.curStatement
        while (statement != None) :
            if statement.isBilled == True :
                return statement
            statement = statement.lastStatement
        return None
    
    def findCanInstallmentTrading(self, number) :
        return self.curStatement.findCanInstallmentTrading(number)
    
    def cancelInsMannul(self, insId=None) :
        if insId == None :
            # cancel all
            self.curStatement.cancelInstallment(None)
        else :
            installment = self.curStatement.findInstallmentById(insId)
            self.curStatement.cancelInstallment(installment, onlyPrin=True)
    
    def adjustInsPostDate(self) :
        self.curStatement.adjustInsPostDate()