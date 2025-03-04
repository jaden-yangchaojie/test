from StoriSQL import StoriSQL
import pandas as pd
from StoriUtils import round_to_even, getRunTime, loggingExpect
from datetime import datetime, time, timedelta
from StoriStatement import Statement
from StoriCif import StoriCif
from StoriBill import StoriBill
import json
from StoriUser import StoriUser
from StoriTrade import StoriTrade, TradingType, convertToTradingType, PRINTradingListType, ADBTYPEList
import logging

class StoriCheck:
    def __init__(self, checkIds:list = None, localCalResults:dict = {}, dbData:dict = None, userMap = {}):  
        self.checkIds:list = checkIds # 待检验的accountId
        self.accountError:dict = {} # accountId-error的映射
        self.userError:dict = {} # 用例名-error的映射

        self.userMap:dict = userMap # accountId-用例名的映射
        self.localCalResults:dict = localCalResults # 本地跑的结果，用例名-user映射
        self.dbData:dict = dbData # 数据库的结果，用例名-数据库数据的映射

        self.curUser:StoriUser = None # 临时变量，当前检查的用户
        self.curCheckCycle = None # 零时变量，当前检查的账期

        self.logger = logging.getLogger('check')
        self.logger.setLevel(logging.DEBUG)

        # file_handler = logging.FileHandler(f'{folder}/log.log')
        console_handler = logging.StreamHandler()
        # file_handler.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        # file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        # self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    @getRunTime
    def checkLatest(self, checkNumber = 1) :
        sql = StoriSQL()
        data = sql.getAccountsData(self.checkIds, forRecovery=True)
        for accountId in data :
            try :
                self.reconstructStatement(accountId, data[accountId], checkNumber=checkNumber)
            except Exception as e:
                loggingExpect(self.logger, e)
        print(self.userError)
        print(f"失败:{len(self.accountError)}/总数:{len(self.checkIds)}")
        print("成功率: ", (len(self.checkIds)-len(self.accountError))/len(self.checkIds))

    @getRunTime
    def checkAll(self) :
        if self.dbData == None :
            sql = StoriSQL()
            data = sql.getAccountsData(self.checkIds)
            for accountId in data :
                user:StoriUser = None
                if accountId in self.userMap :
                    name = self.userMap[accountId]
                    if name in self.localCalResults :
                        user = self.localCalResults[name]
                self.runStatement(accountId, data[accountId], user)
        else :
            for key in self.dbData :
                user:StoriUser = self.localCalResults[key]
                accountId = user.accountId
                dbData = self.dbData[key]
                self.runStatement(accountId, dbData, user)
        # formatted_json_str = json.dumps(self.accountError, indent=4, ensure_ascii=False)
        # print(formatted_json_str)
        print(self.userError)
        print(f"失败:{len(self.accountError)}/总数:{len(self.checkIds)}")
        print("成功率: ", (len(self.checkIds)-len(self.accountError))/len(self.checkIds))
        return self.userError
    
    def checkStatement(self, dbData, statement:Statement, realtime = False) :
        bill:StoriBill = statement.bill
        dueDate = bill.dueDate.strftime("%Y%m%d")
        statementDate = bill.statementDate.strftime("%Y%m%d")
        graceDate = bill.graceDate.strftime("%Y%m%d")
        billingCycle = bill.startDate.strftime("%Y%m%d") + "-" + bill.endDate.strftime("%Y%m%d")
        self.curCheckCycle = billingCycle
        minPayment = round_to_even(bill.minimumPayment * 100, 0)
        pmt_amt = round_to_even((bill.totalPayment - statement.unpaidTotal) * 100 , 0)
        grace_dt_unpaid_mini_amt = round_to_even(statement.graceDayUnpaidMinimum * 100, 0)
        due_dt_unpaid_mini_amt = round_to_even(statement.dueDayUnpaidMinimum * 100, 0)
        previousBalance = round_to_even(bill.previousBalance * 100, 0)
        newBalance = round_to_even(bill.newBalance * 100, 0)

        self.checkExpectData(dbData, "billing_cycle", billingCycle)
        self.checkExpectData(dbData, "due_dt", dueDate)
        self.checkExpectData(dbData, "grace_dt", graceDate)
        self.checkExpectData(dbData, "statement_dt", statementDate)
        self.checkExpectData(dbData, "min_pmt", minPayment, 0)
        self.checkExpectData(dbData, "previous_bal", previousBalance, 0)
        self.checkExpectData(dbData, "new_bal", newBalance, 0)
        if realtime == False :
            self.checkExpectData(dbData, "pmt_amt", pmt_amt, 0)
            self.checkExpectData(dbData, "grace_dt_unpaid_mini_amt", grace_dt_unpaid_mini_amt, 0)
            self.checkExpectData(dbData, "due_dt_unpaid_mini_amt", due_dt_unpaid_mini_amt, 0)

        activity_summary = json.loads(dbData["activity_summary"])
        SUM = activity_summary["SUM"]
        CURRENT = activity_summary["CURRENT"]

        unpaidDetail = bill.unallocDetail
        vat = round_to_even(unpaidDetail[TradingType.VAT_FEE] + unpaidDetail[TradingType.VAT_INT])
        interest = unpaidDetail[TradingType.INT]
        fee = unpaidDetail[TradingType.FEE]
        insVat = unpaidDetail[TradingType.INS_VAT_INT]
        insInterest = unpaidDetail[TradingType.INS_INT]
        insPrincipal = unpaidDetail[TradingType.INS_PRIN]
        ins = insVat + insInterest + insPrincipal
        prin = unpaidDetail[TradingType.PRIN]
        payment = unpaidDetail[TradingType.PAYMENT]
        refund = unpaidDetail[TradingType.REFUND]
        adj = unpaidDetail[TradingType.ADJ_NEGATIVE]
        self.checkStatementCurrentData(CURRENT, "VAT", vat)
        self.checkStatementCurrentData(CURRENT, "INTEREST", interest)
        self.checkStatementCurrentData(CURRENT, "FEE", fee)
        self.checkStatementCurrentData(CURRENT, "PRIN", prin)
        self.checkStatementCurrentData(CURRENT, "INSTALLMENT", ins)
        # self.checkStatementCurrentData(CURRENT, "PAYMENT", payment)
        # self.checkStatementCurrentData(CURRENT, "RETURN", refund)
        # self.checkStatementCurrentData(CURRENT, "ADJ", adj)

    def doCheck(self, statementSQLData:list, dqData:dict, realtime = False) :
        statementList:list = self.curUser.statementList
        for index, row in enumerate(statementSQLData):
            statement:Statement = statementList[index]
            self.checkStatement(dbData=row, statement=statement, realtime=realtime)
            
        if dqData :
            cif = self.curUser.cif
            dqDays = cif.getDQDays()
            dqDueBucket = cif.getDQDueBucket()
            status = row["status"]
            if status == "Current" :
                self.checkExpectData(dqData, "due_bucket", dqDueBucket, 0)
                self.checkExpectData(dqData, "dq_days", dqDays, 0)
            elif status == "Recovery" and dqDays != 0:
                self.checkExpectData(dqData, "dq_days", dqDays, 0)

    def runStatement(self, accountId, data, user:StoriUser = None) :
        
        if not "statement" in data :
            return
        statementList = data["statement"]
        if len(statementList) <= 0 :
            return
        
        if user :
            self.curUser = user
            if user.accountId != accountId :
                user.accountId = accountId
                self.doCheck(statementList, None)
            else :
                self.doCheck(statementList, None, realtime=True)
            return
        
        contractInfo = {"params":data["params"]}

        cardId = 1
        cif = StoriCif(contractInfo, cardId=cardId)
        open_date = data["account"]["open_date"].to_pydatetime()

        activityList = data["activity"]
        # if type(activityDF) == pd.DataFrame and not activityDF.empty :
        #     activityDF = activityDF.sort_values(by='effective_time_local')
        
        self.curUser = StoriUser(accountId, cif, open_date)
        self.curUser.accountId = accountId
        self.curUser.activeCard({"cardId":cardId})
        cardId += 1

        statementIndex = 0
        statementCreateTime = statementList[statementIndex]["create_time_local"].to_pydatetime()

        if "installment" in data :
            self.curUser.handleIns(data["installment"])

        if "benefit" in data :
            self.curUser.benefits(data["benefit"])

        for row in activityList:
            # isPomelo = row["channel"] == "POMELO"
            # tid = row["reference_id"]
            activityType = row["type"]
            sub_type = row["sub_type"]
            # action_type = row["action_type"]
            # status = row["status"]
            # amt = round_to_even(row["amt"]/100)
            effective_time_local = row["effective_time_local"].to_pydatetime()
            create_time_local = row["create_time_local"].to_pydatetime()
            # transaction_local_time = row["transaction_local_time"].to_pydatetime()

            while statementCreateTime and statementCreateTime < create_time_local :
                self.curUser.changeTime(datetime.combine(self.curUser.curStatement.bill.statementDate, time(0,1)))
                self.curUser.genBill()
                statementIndex += 1
                if statementIndex < len(statementList) :
                    statementCreateTime = statementList[statementIndex]["create_time_local"].to_pydatetime()
                else :
                    statementCreateTime = None

            self.curUser.changeTime(effective_time_local)

            # tradingData = {"type":activityType, "sub_type":sub_type, "action_type":action_type, "tid":tid, "ref_order_id":tid, "amt":amt, "status":status, "effective_time_local":effective_time_local, "transaction_local_time":transaction_local_time}
            if sub_type == "CARD_REPLACEMENT_FEE" :
                if activityType == "CARD_REPLACEMENT_FEE" :
                    self.curUser.exchangeCard({"reason":"LOST"}, cardId)
                    self.curUser.activeCard({"cardId":cardId})
                    cardId += 1
            
            tradingData = row.copy()
            self.curUser.trading(tradingData)

        while self.curUser.billedNumber < len(statementList) :
            isLast = self.curUser.billedNumber == len(statementList)-1
            self.curUser.genBill(isLast)

        dqData = data["dq"] if "dq" in data else None
        self.doCheck(statementList, dqData)
        
    def addUserError(self, errorData:tuple) :
        cycle = self.curCheckCycle
        errorData = (cycle, ) + errorData

        accountId = self.curUser.accountId
        if not accountId in self.accountError :
            self.accountError[accountId] = []
        self.accountError[accountId].append(errorData)
        
        userName = self.curUser.userName
        if not userName in self.userError :
            self.userError[userName] = []
        self.userError[userName].append(errorData)


    # 检查断言是否一致
    def checkExpectData(self, assertData, key, checkData, precision = 2) :
        if (key == None) :
            return None
        expectData = assertData[key]
        if (expectData == None) :
            return None
        if (type(checkData) == str) :
            if (expectData != checkData) :
                print("assert error:", expectData, checkData)
                self.addUserError((key, checkData, expectData))
        else :
            if (precision == 0) :
                expectData = int(expectData)
            else :
                expectData = float(expectData)
                checkData = round_to_even(checkData, precision)
            if (expectData != checkData) :
                print("assert error:", expectData, checkData)
                self.addUserError((key, checkData, expectData))
        return None
    
    def checkStatementCurrentData(self, current, key, value) :
   
        if value > 0 :
            if not key in current :
                self.addUserError((f"current[{key}]", value, 0))
            else :
                expectData = round_to_even(current[key]/100)
                if expectData != value :
                    self.addUserError((f"current[{key}]", value, expectData))
        else :
            if key in current :
                expectData = round_to_even(current[key]/100)
                if expectData != 0 :
                    self.addUserError((f"current[{key}]", value, expectData))

    def reconstructStatement(self, accountId, data, checkNumber = 1) :
        if not "statement" in data :
            return

        # 创建用户和合约
        contractInfo = {"params":data["params"]}
        cif = StoriCif(contractInfo, cardId=1)
        open_date = data["account"]["open_date"].to_pydatetime()
        self.curUser = StoriUser(accountId, cif, open_date, forRecovery=True)
        self.curUser.accountId = accountId

        statementSQLData = data["statement"]
        if len(statementSQLData) <= 0 :
            return
        
        # 需要核对的账单位置
        checkStatementIndex = max(0, len(statementSQLData)-checkNumber)
        # 创建账单
        startTime = open_date
        checkStartSysTime = startTime
        for i in range(len(statementSQLData)) :
            row = statementSQLData[i]
            curStatement:Statement = self.curUser.addStatement(startTime, row["create_time_local"].to_pydatetime())
            curStatement.statementId = row["statement_id"]
            if i >= checkStatementIndex :
                continue

            bill:StoriBill = curStatement.bill
            billingCycle = row["billing_cycle"]
            due_dt = datetime.strptime(row["due_dt"], '%Y%m%d').date()
            grace_dt = datetime.strptime(row["grace_dt"], '%Y%m%d').date()
            startTime = datetime.strptime(row["statement_dt"], '%Y%m%d')
            statement_dt = startTime.date()
            min_pmt = round_to_even(row["min_pmt"]/100)
            previous_bal = round_to_even(row["previous_bal"]/100)
            new_bal = round_to_even(row["new_bal"]/100)
            pmt_amt = round_to_even(row["pmt_amt"]/100)
            grace_dt_unpaid_mini_amt = round_to_even(row["grace_dt_unpaid_mini_amt"])
            due_dt_unpaid_mini_amt = round_to_even(row["due_dt_unpaid_mini_amt"])
            status = row["status"]

            bill.billingCycle = billingCycle
            bill.dueDate = due_dt
            bill.graceDate = grace_dt
            bill.statementDate = statement_dt
            bill.endDate = statement_dt - timedelta(days=1)
            bill.DQTriggerDay = due_dt + timedelta(days=1)
            bill.minimumPayment = min_pmt
            bill.totalPayment = max(0, round_to_even(previous_bal + new_bal))
            bill.previousBalance = previous_bal
            bill.newBalance = new_bal

            curStatement.graceDayUnpaidMinimum = grace_dt_unpaid_mini_amt
            curStatement.dueDayUnpaidMinimum = due_dt_unpaid_mini_amt
            curStatement.unpaidTotal = max(0, bill.totalPayment - pmt_amt)
            curStatement.unpaidMinimum = max(0, bill.minimumPayment - pmt_amt)
            
            if curStatement.unpaidTotal <=0 :
                assert(status == "PMT_IN_ALL")
            elif pmt_amt == 0 :
                assert(status == "PMT_NO")
            elif curStatement.unpaidMinimum <=0 :
                assert(status == "PMT_COVER_MIN")
            else :
                assert(status == "PMT_BELOW_MIN")

        # 创建一个未出账账单
        self.curUser.addStatement(startTime)
        
        statementList = self.curUser.statementList
        checkStatement:Statement = statementList[checkStatementIndex]
        if checkStatement.lastStatement :
            checkStartSysTime = checkStatement.lastStatement.createTime

        if "benefit" in data :
            benefits = []
            for benefit in data["benefit"] :
                if benefit["benefit_type"] == "INTEREST_COUPON" :
                    if benefit["usage_time"]==None or benefit["usage_time"].to_pydatetime().date()>checkStatement.bill.startDate :
                        benefits.append(benefit)
                else :
                    benefits.append(benefit)
            self.curUser.benefits(benefits)

        # 关联账单交易
        activityList = data["activity"]
        for activityData in activityList:
            effective_time_local:datetime = activityData["effective_time_local"].to_pydatetime()
            create_time_local:datetime = activityData["create_time_local"].to_pydatetime()
            post_time_local:datetime  = activityData["post_time_local"].to_pydatetime() if activityData["post_status"] == "POSTED" and activityData["post_time_local"] != None else None
            activityType = activityData["type"]
            sub_type = activityData["sub_type"]
            request_id = activityData["request_id"]
            tradingType = convertToTradingType(typeStr=activityType, subType=sub_type)
            amt = round_to_even(activityData["amt"]/100)
            pmt_amt = round_to_even(activityData["pmt_amt"]/100)
            if tradingType == None :
                print("activityType")
                assert("trading type error")
            trading = StoriTrade(tradingType, amt, tid=request_id, effective_time=effective_time_local)
            
            if post_time_local :
                trading.posting(amount=amt, posting_time=post_time_local)
            trading.leftAmount = round_to_even(amt - pmt_amt)
            for statement in statementList:
                statement_dt = statement.bill.statementDate
                statementCreateTime = statement.createTime
                if effective_time_local.date() < statement_dt and (statementCreateTime==None or create_time_local < statementCreateTime):
                    statement.unbilledList.append(trading)
                if post_time_local and post_time_local.date() < statement_dt :
                    statement.bill.addTrading(trading)
                    if trading in statement.unbilledList :
                        statement.unbilledList.remove(trading)
                    if statement.bill.number < checkStatement.bill.number :
                        if trading.isPositiveTrading() :
                            statement.unpaidTradingDic[trading.type].append(trading)
                    break
                elif post_time_local and post_time_local.date() == statement_dt and activityType in ["LATE_FEE","VAT_LATE_FEE","INTEREST","VAT_INT"]:
                    if statement.bill.number < checkStatement.bill.number :
                        statement.bill.addTrading(trading)
                        statement.unpaidTradingDic[trading.type].append(trading)
                    break

            if trading.isNegativeTrading() :
                cif.availableLimit = round_to_even(cif.availableLimit + trading.amount)
            else :
                cif.availableLimit = round_to_even(cif.availableLimit - trading.amount)

        # 计算历史账单数据
        for i in range(checkStatementIndex) :
            statement:Statement = statementList[i]
            statement_dt = statement.bill.statementDate
            print(statement.statementId, statement_dt)
            print(statement.unpaidTotal, statement.unpaidMinimum)
            billedList = statement.bill.billedList
            allButPrincipal = 0
            for trading in billedList :
                print(trading.effective_time, trading.posting_time, trading.amount, trading.leftAmount, trading.type)
                if trading.type not in PRINTradingListType:
                    leftAmount = trading.leftAmount
                    if leftAmount > 0 :
                        trading.unpaidInMinimum[statement.bill.number] = leftAmount
                        allButPrincipal += leftAmount

            curMin = statement.unpaidMinimum
            if statement.lastStatement :
                curMin = round_to_even(statement.unpaidMinimum - statement.lastStatement.unpaidMinimum)
            assert(curMin >= 0)

            principalInMinimum = round_to_even(statement.unpaidMinimum - allButPrincipal)
            statement.allocPrinInMinimum(principalInMinimum)
            statement.isBilled = True
        
        print("startdate", checkStatement.bill.startDate)

        paymentList = data["payment"]
        curStatement = checkStatement
        for payment in paymentList :
            create_time_local = payment["create_time_local"].to_pydatetime()
            if checkStatement.lastStatement and create_time_local < checkStatement.lastStatement.createTime : 
                continue
            while curStatement.createTime and create_time_local > curStatement.createTime :
                curStatement = statementList[curStatement.bill.number]
            amt = round_to_even(payment["amt"]/100)
            paymentTrading = curStatement.findTargertTradingById(payment["pmt_id"], posted=True)
            activity_statement_id = payment["activity_statement_id"]
            payment_statement_id = payment["payment_statement_id"]
            activityStatement = self.findStatement(self.curUser, activity_statement_id) # 正向交易所在账单
            if activityStatement == None :
                activityStatement = curStatement
            if payment_statement_id == None :
                paymentStatement = activityStatement
            else :                
                paymentStatement = self.findStatement(self.curUser, payment_statement_id) # 所还款账单
            if paymentStatement == None :
                paymentStatement = curStatement
            toTrading = activityStatement.findTargertTradingById(payment["account_activity_id"], posted=True)
            paymentBillNumber = paymentStatement.bill.number
            print(activityStatement.bill.number, paymentBillNumber, amt)
            if toTrading : # None 账单生产的交易，没有关联
                toTrading.leftAmount = round_to_even(toTrading.leftAmount + amt)
                if paymentBillNumber < checkStatement.bill.number:
                    if payment["subtype"] == "MINI_PMT_MINI" :
                        unpaid = toTrading.unpaidInMinimum.get(paymentBillNumber, 0)
                        toTrading.unpaidInMinimum[paymentBillNumber] = round_to_even(unpaid + amt)
                    if paymentStatement != activityStatement :
                        paymentStatement.unpaidTradingDicOfPreStatement[toTrading.type].append(toTrading)
                else :
                    print(paymentStatement.bill.number)
                assert(toTrading.leftAmount <= toTrading.amount)
            # else :
            #     assert(0)

            if paymentTrading == None : # 溢缴款，向后还款
                while curStatement.lastStatement :
                    curStatement = curStatement.lastStatement
                    paymentTrading = curStatement.findTargertTradingById(payment["pmt_id"], posted=True)
                    if paymentTrading :
                        break
            assert(paymentTrading)
            paymentTrading.leftAmount = round_to_even(paymentTrading.leftAmount + amt)
            assert(paymentTrading.leftAmount <= paymentTrading.amount)
            # print(paymentTrading.amount, paymentTrading.leftAmount)
            # print( amt, fromStatement.statementId, activityStatement.statementId, paymentTrading.amount, toTrading.amount)

            if payment["type"] == "PAYMENT_STATEMENT" and activityStatement.bill.number < checkStatement.bill.number:
                cif.availableLimit = round_to_even(cif.availableLimit - amt)
                toMinimum = payment["subtype"] == "MINI_PMT_MINI"
                statement = checkStatement.lastStatement
                while statement:
                    statement.unpaidTotal = round_to_even(statement.unpaidTotal + amt)
                    if toMinimum and statement.bill.number >= paymentBillNumber:
                        statement.unpaidMinimum = round_to_even(statement.unpaidMinimum + amt)
                    if statement == activityStatement :
                        break
                    statement = statement.lastStatement
        
        # 计算 balance
        lastStatement = checkStatement.lastStatement
        if lastStatement:
            cif.balance = round_to_even(lastStatement.bill.previousBalance + lastStatement.bill.newBalance)
            if cif.balance < 0 : # 溢缴款
                lastStatement.calOverPayment()
            else :
                assert(cif.balance == lastStatement.unpaidTotal)
            
            if lastStatement.unpaidTotal > 0 :
                notADB = 0
                for i in range(checkStatementIndex) :
                    statement = statementList[i]
                    if statement.unpaidMinimum <= 0 :
                        break
                    for tradingType in statement.unpaidTradingDic :
                        if tradingType in ADBTYPEList :
                            continue
                        for intTrading in statement.unpaidTradingDic[tradingType] :
                            if intTrading.leftAmount <=0 :
                                continue
                            notADB = round_to_even(notADB + intTrading.leftAmount)
                cif.adbBalance = max(0, round_to_even(lastStatement.unpaidTotal - notADB))

        # dq恢复
        if "dq" in data :
            dqData = data["dq"]
            dqStatus = dqData["status"]
            if dqStatus == "Recovery" :
                recovery_date = datetime.strptime(dqData["recovery_date"], '%Y%m%d').date()
                if recovery_date < checkStatement.bill.startDate :
                    cif.DQDays = 0
                    cif.DQFirstDueDate = None
                    cif.DQFirstStatement = 0
                    cif.DQCurStatement = lastStatement.bill.number
                else :
                    print("")
            else :
                print("")

        # 出账
        for i in range(checkStatementIndex, len(statementList)) :
            statement = statementList[i]
            for trading in statement.bill.billedList :
                statement.updateBalance(trading)
                if trading.isNegativeTrading() and trading.leftAmount > 0 :
                    statement.handlePayment(trading)
            if i < len(statementList)-1 :
                startTime = datetime.combine(statement.bill.statementDate,  time(00,00))
                statement.changeTime(startTime)
                statement.generateBill()
        
        # 出账验证
        for i in range(checkStatementIndex, len(statementList)-1) :
            statement = statementList[i]
            dbData = statementSQLData[i]
            # self.checkStatement(dbData=dbData, statement=statement)
            self.checkStatement(dbData=dbData, statement=statement, realtime=True)
    
    def findStatement(self, user, statementId, next = False) -> Statement:
        if statementId == None :
            return None
        statementList:list = user.statementList
        if len(statementList) == 1 :
            return statementList[0]
        for index, statement in enumerate(statementList) :
            if statement.statementId == statementId :
                if next == False :
                    return statement
                else :
                    return statementList[index + 1]
        return None
            
#第三期用例1.2 11110211000000381300
# 11110011000050887075
# 11110011000050825752
# 调整 11110111000000323360
# 分期 11110011000051233808
# 11110011000051865013
# 账单列表分期入账 11110011000052463016
# storiCheck = StoriCheck(checkDic.keys()) 
# storiCheck = StoriCheck(["99910111000000073716"]) 

def checkLastPipeline(folder, localCalResults={}) :
    folder = f"export/autotest/{folder}"
    filename = f"{folder}/pipeline_lastExcute.json"
    with open(filename, 'r') as file:
        data = json.load(file)
        resultId = data["resultId"]
    # filename = f"{folder}/erorr_{resultId}.json"
    # with open(filename, 'r', encoding='utf-8') as file:
    #     errorDic = json.load(file)

    filename = f"{folder}/env_{resultId}.json"
    checkList = []

    with open(filename, 'r', encoding='utf-8') as file:
        envDic:dict = json.load(file)
        userMap = {}
        for user in envDic :
            # if user in errorDic :
            #     continue
            env = envDic[user]
            if "${accountId}" in env:
                accountId = env["${accountId}"]
                if type(accountId) != str or len(accountId) != 20 :
                    continue
                checkList.append(accountId)
                userMap[accountId] = user

    if len(checkList) > 0 :
        storiCheck = StoriCheck(checkList, localCalResults, userMap=userMap)
        storiCheck.check()

