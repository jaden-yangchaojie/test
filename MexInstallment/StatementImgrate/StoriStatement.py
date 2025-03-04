
from datetime import datetime, timedelta, time
# from enum import Enum
from StoriUtils import round_to_even
from StoriConfigs import readCycle, MINIMUM_PAYMENT_THRESHOLD, VAT_RATE
from StoriTrade import APPLY_NEW_Installment_RULES, PRINTradingListType, DayBalance, TradingStatus, TradingType, StoriTrade, PaymentOrderList, PaymentOrderListFirstPrin, isInstallmentType, isNegativeType, positiveUnpaidFilter, unpaidFilter, tradingListSortByTime
from StoriInstallment import Installment
# from logger import logger
from StoriBill import StoriBill
from StoriLabel import StoriLabel, StoriDQFlag, StoriChargingFlag, StoriPaymentFlag, StoriChargingFlag, StoriStatementFlag, StoriTradingFlag, StoriAdjustmentFlag, StoriMinimumFlag, StoriFreeIntCouponFlag, StoriInstallmentFlag
from StoriCif import StoriCif
from typing import List, Dict

APPLY_NEW_Grace_Amount = True
PAYMENT_Grace_Amount = 10

class Statement:  

    def __init__(self, startTime, cif:StoriCif = None, lastStatement = None, statementId = None):
        
        self.statementId = statementId

        self.cif = cif #合约信息
        self.label = StoriLabel(lastLabel=lastStatement.label if lastStatement != None else None, cifLabel=cif.label)

        # 账期相关时间
        contractStatementDay = self.cif.getStatementDay()
        cycleList = readCycle(contractStatementDay)

        if (lastStatement == None) :
            startDate = startTime.date()
            for index, cycle in enumerate(cycleList) :
                initialDay = cycle["initialDay"]
                endDay = cycle["endDay"]
                if (startDate >= initialDay and startDate <= endDay) :
                    self.cycle = cycle
                    self.cycleLine = index
                    break
            assert(self.cycle != None)
            number = 1
            self.label.markFlag(StoriStatementFlag.StatementFirst)
        else :
            self.cycleLine = lastStatement.cycleLine + 1
            self.cycle = cycleList[self.cycleLine]
            startDate = self.cycle["initialDay"]
            number = lastStatement.bill.number + 1
            self.cif.DQCurStatement = lastStatement.bill.number

        self.curTime = startTime
        self.curDate = self.curTime.date()

        self.bill = StoriBill(startDate, self.cycle, number, cif)

        self.unbilledList:List[StoriTrade] = [] # 非本账期入账的交易列表
        self.lastStatement:Statement = lastStatement #上个账单

        self.installmentList: List[Installment] = [] #分期列表

        # 状态
        self.dueDayUnpaidTotal = 0.0 # DQTriggerDay的未还总额 大于0触发利息
        self.dueDayUnpaidMinimum = 0.0 # DQTriggerDay的未还最小金额 大于0触发DQ
        self.graceDayUnpaidMinimum = 0.0 # GraceDay的未还最小金额 大于0触发滞纳金
        self.dqUnpaidMinimum = 0.0 # 触发DQ的未还最小还款，duebucket>4后的逆向不能
        self.intChecked = False
        self.latefeeChecked = False
        if (self.lastStatement != None) :
            for trading in self.lastStatement.unbilledList:
                if trading.status == TradingStatus.POSTED :
                    self.bill.addTrading(trading)
                elif trading.status != TradingStatus.REJECTED and trading.amount != 0 :
                    self.unbilledList.append(trading)
            self.installmentList = lastStatement.installmentList

        #Trade类型
        self.lateFeeTrading = None
        self.vatLateFeeTrading = None
        self.interestTrading = None
        self.vatInterestTrading = None

        self.billing = False #正在出账
        self.isBilled = False #是否已经出账
        self.installmentPosted = False #分期是否已经入账
        self.insAdjusted = False #是否调整过分期入账时间
        self.endDayChargingList = [] #出账时产生的滞纳金和利息还有税的列表
        self.overTrading = None

        self.unpaidTotal = 0.0 # 未还总额（包含上期未还）
        self.unpaidMinimum = 0.0 # 未还最小还款额（包含上期未还）
        self.unpaidTradingDic: Dict[TradingType, List[StoriTrade]] = {} # 本账期未还的交易明细 type : 未还tradingList
        self.unpaidTradingDicOfPreStatement: Dict[TradingType, List[StoriTrade]] = {} # 最小还款关联交易中，不在本账期的交易
        for key in PaymentOrderList :
            self.unpaidTradingDic[key] = []
            self.unpaidTradingDicOfPreStatement[key] = []

        self.bill.originUnpaidDetail = self.getUnpaidDetail()

        # 触发历史还款        
        for trading in self.bill.billedList :
            self.triggerPayment(trading)
            self.updateBalance(trading)
        

    # 是否缺少DQ触发通知
    def lackOfDQTrigger(self, date) -> bool:
        lastStatement = self.lastStatement
        if lastStatement != None :
            if date > lastStatement.bill.DQTriggerDay and (self.cif.DQEnabledDate == None or self.cif.DQEnabledDate < lastStatement.bill.DQTriggerDay) :
                unpaid = self.getHistoryUnpaidMinimum()
                if unpaid > 0 :
                    return True
        return False
    
    #时间更新
    def changeTime(self, curTime) :
        print(curTime)

        if curTime == self.curTime :
            return

        if curTime.date() < self.curDate :
            print()
        
        self.curDate = curTime.date()
        self.curTime = curTime

        if self.lastStatement and self.curDate > self.getLastDueDate() :
            if self.cif.checkCanReverseDQ() :
                unpaid = round_to_even(self.lastStatement.unpaidMinimum)
                self.updateDueDayUnpaidMinimum(unpaid)

        # 更新DQEnabledDate
        if self.lastStatement and self.curDate > self.lastStatement.bill.DQTriggerDay :
            self.cif.DQCurStatement = self.bill.number
            if self.cif.DQEnabledDate == None or self.cif.DQEnabledDate < self.getLastDueDate() :
                self.handleDQCreate(auto=True)
        
        # # 检查分期入账
        # if (self.curDate >= self.bill.endDate and self.installmentPosted == False) :
        #     self.postingInstallment()
        #     self.installmentPosted = True

    def handleDQCreate(self, auto = False) :
        if self.lastStatement == None :
            return
        
        # unpaid = self.lastStatement.dueDayUnpaidMinimum
        unpaid = round_to_even(self.lastStatement.unpaidMinimum)

        canReversDQ = self.cif.checkCanReverseDQ()

        if unpaid <= 0:
            if not canReversDQ :
                self.cif.DQSkipStatementSet.add(self.bill.number)
            return
        
        if auto == True :
            print("auto")
        
        if self.curDate > self.getLastDueDate() :
            
            print("还款日后触发DQ")

            self.cif.DQEnabledDate = self.lastStatement.bill.DQTriggerDay
            self.cif.DQCurStatement = self.bill.number

            if canReversDQ:
                self.updateDQUnpaidMinimum(unpaid)
                if self.cif.checkDQ() == False : # 首次触发DQ通知通知才能生效
                    self.cif.DQFirstDueDate = self.getLastDueDate()
                    self.cif.DQFirstStatement = self.lastStatement.bill.number
                    self.cif.updateDQDays(self.curDate)
            
            # label after trigger
            self.markDueBucket()

    def handleDQUpdate(self) :
        print("DQ天数更新")
        self.cif.updateDQDays(self.curDate)

    def markDueBucket(self) :
        dueBucket = self.cif.getDQDueBucket()
        if (dueBucket >0) :
            flagName = "DQTrigger" + str(dueBucket)
            flag = getattr(StoriDQFlag, flagName, None)  
            self.label.markFlag(flag)

    def reverseDueBucket(self, oldBucket, newBucket) : # DQUpdateTrigger

        # 更新DQ天数
        self.cif.updateDQDays(self.curDate)

        # 更新首次DQTrigger的时间
        if self.cif.checkDQ() == False:
            self.cif.DQEnabledDate = None

        # label
        bucketReversed = oldBucket - newBucket

        flagName = "PaymentDQReversed" + str(int(bucketReversed))
        flag = getattr(StoriPaymentFlag, flagName, None)
        self.label.markFlag(flag)
        self.label.markFlag(StoriDQFlag.DQReversedTrigger)

    def getLastGraceDate(self) :
        if (self.lastStatement == None) :
            return None
        return self.lastStatement.bill.graceDate
    
    def getLastDueDate(self) :
        if (self.lastStatement == None) :
            return None
        return self.lastStatement.bill.dueDate
    
    def getGraceDayUnpaidMinimum(self) :
        if self.lastStatement == None :
            return 0
        return self.lastStatement.graceDayUnpaidMinimum
    
    def updateGraceDayUnpaidMinimum(self, unpaid) :
        self.lastStatement.graceDayUnpaidMinimum = max(0, unpaid)
    
    # def getDueDayUnpaidTotal(self) :
    #     if self.lastStatement == None :
    #         return 0
    #     return self.lastStatement.dueDayUnpaidTotal
    
    def updateDueDayUnpaidTotal(self, unpaid) :
        self.lastStatement.dueDayUnpaidTotal = max(0, unpaid)
    def updateDueDayUnpaidMinimum(self, unpaid) :
        self.lastStatement.dueDayUnpaidMinimum = max(0, unpaid)

    def getDQUnpaidMinimum(self) :
        if self.lastStatement == None :
            return 0
        return self.lastStatement.dqUnpaidMinimum
    
    def updateDQUnpaidMinimum(self, unpaid) :
        self.lastStatement.dqUnpaidMinimum = max(0, unpaid)
    
    # 检查交易时间对应的DQ账期
    def findDQStatementNumber(self, tradingDate) :
        statement = self
        while (statement.lastStatement != None) :
            if tradingDate >= statement.bill.startDate :
                if tradingDate > statement.getLastDueDate() :
                    DQStatementNumber = statement.bill.number
                else :
                    DQStatementNumber = statement.lastStatement.bill.number
                break
            statement = statement.lastStatement
        return DQStatementNumber
    
    # trading不为空，表示90天后，回撤，trading是引起回撤的交易
    def checkReverseDQ(self, trading:StoriTrade = None) :
        
        # 交易入账检查更新DQ状态
        statement = self
        oldDueBucket = self.cif.getDQDueBucket()
        self.cif.DQFirstDueDate = None
        self.cif.DQFirstStatement = 0
        DQFirstDueDate = None
        DQFirstStatement = 0
        while (statement.lastStatement != None) :
            if trading != None :
                unpaid = round_to_even(statement.getDQUnpaidMinimum() - trading.amount)
            else :
                unpaid = round_to_even(statement.lastStatement.unpaidMinimum)
            
            # 更新未还最小还款快照
            statement.updateDQUnpaidMinimum(unpaid)
            # 如果没有最小未还，停止查找
            if unpaid <= 0 :
                break
            # 往前查找历史账期，如果最小未还金额>0，dq天数更新为当前时间-账期dueday
            if (self.cif.DQEnabledDate and self.cif.DQEnabledDate > statement.getLastDueDate()) :
                DQFirstDueDate = statement.getLastDueDate()
                DQFirstStatement = statement.lastStatement.bill.number
            statement = statement.lastStatement
        self.cif.DQFirstDueDate = DQFirstDueDate
        self.cif.DQFirstStatement = DQFirstStatement

        # DQ回撤更新
        newDueBucket = self.cif.getDQDueBucket()
        if (newDueBucket < oldDueBucket) :
            self.reverseDueBucket(oldDueBucket, newDueBucket)

    def checkIfNeedReverseStatus(self, trading:StoriTrade) :
        if (trading.status != TradingStatus.POSTED) :
            return
        if (self.lastStatement == None) :
            return
        
        tradingEffectiveDate = trading.effective_time.date()
        
        # bucket4不能撤回，但是如果还款交易时间在bucket4之前，仍然可以回撤
        if self.cif.checkCanReverseDQ() == False :
            statementNumber = self.findDQStatementNumber(tradingEffectiveDate)
            if self.cif.checkCanReverseDQ(tradingEffectiveDate, statementNumber) :
                oldDueBucket = self.cif.getDQDueBucket()
                self.checkReverseDQ(trading)
                newDueBucket = self.cif.getDQDueBucket()
                if (newDueBucket < oldDueBucket) :
                    if self.totalPaymentBeforeTrading :
                        self.label.markFlag(StoriPaymentFlag.PaymentReverseDQ4WhenPMTALL)
                else :
                    self.label.markFlag(StoriDQFlag.DQ4CannotReversedCausePaymentNotEnouph)
                    print("有交易时间发生在bucket4之前的，但是不满足回撤条件")
            else :
                self.label.markFlag(StoriDQFlag.DQ4CannotReversed)
                print("bucket>=4，DQ 不能回退, DQ天数：", self.cif.DQDays)
        else :
            self.checkReverseDQ()

    def checkClosing(self) :
        if self.cif.checkReachClosingBucket() and self.unpaidTotal <= 0 :
            self.label.markFlag(StoriPaymentFlag.PaymentAllTriggerClosing)
            return True
        return False

    # 记账
    def pendingTrading(self, trading:StoriTrade, effective_time) :
        assert(effective_time != None)
        trading.effective_time = effective_time
        trading.status = TradingStatus.PENDING
        if self.billing == False :
            self.unbilledList.append(trading)
        else :
            self.bill.addTrading(trading)
        self.updateCredit(trading) # 更新额度
    
    # 入账
    def postingTrading(self, trading:StoriTrade, posting_time, amount) :
        if trading.status == TradingStatus.PENDING :
            if (amount < trading.amount) :
                self.label.markFlag(StoriTradingFlag.TradingPostingLessThenAuth)
            elif (amount > trading.amount) :
                self.label.markFlag(StoriTradingFlag.TradingPostingOverAuth)
            trading.posting(amount, posting_time)
            if trading in self.unbilledList and posting_time.date() <= self.bill.endDate:
                self.bill.addTrading(trading)
                self.unbilledList.remove(trading)
            self.updateBalance(trading, checkDate=(self.billing==False)) # 更新余额
            self.triggerPayment(trading) # 逆向交易触发还款分配

            # label更新
            if self.lastStatement != None :
                if self.lastStatement.bill.totalPayment > 0 :
                    if self.label.getMarkedFlag(StoriPaymentFlag.PaymentNotInFullBeforeDueDay) :
                        if self.curDate > self.lastStatement.bill.dueDate and self.lastStatement.unpaidTotal<=0:
                            self.label.markFlag(StoriPaymentFlag.PaymentInFullAfterDueDay)
                if self.lastStatement.bill.minimumPayment > 0 :
                    if self.label.getMarkedFlag(StoriPaymentFlag.PaymentNotInMinimumBeforeGraceDay) :
                        if self.curDate > self.lastStatement.bill.graceDate and self.lastStatement.unpaidMinimum<=0:
                            self.label.markFlag(StoriPaymentFlag.PaymentInMinimumAfterGraceDay)
            return True
        return False

    # 交易入账时检查是否是逆向交易入账，如果是逆向交易，触发还款分配，以及状态更新
    def triggerPayment(self, trading:StoriTrade) :
        if trading.isNegativeTrading() :
            if self.lastStatement and round_to_even(self.lastStatement.unpaidTotal) <= 0 :
                self.totalPaymentBeforeTrading = True
            else :
                self.totalPaymentBeforeTrading = False

            if trading.priorityTid :
                priorityTrading = self.findTargertTradingById(trading.priorityTid, posted=True)
                trading.paymentToPositveTrading(priorityTrading)
            if trading.leftAmount > 0 :
                self.handlePayment(trading) # 目前退款和调整都和payment一样处理
            
            # self.handlePayment(trading) # 目前退款和调整都和payment一样处理
            # if (trading.type == TradingType.REFUND) :
            #     print()
            # if (trading.type == TradingType.PAYMENT) :
            #     self.handlePayment(trading)
            # elif (trading.type == TradingType.REFUND) :
            #     self.handleRefund(trading)
            # elif (trading.type == TradingType.ADJ_NEGATIVE) :
            #     self.handleRefund(trading)
            # 查看是否需要撤销状态（是否要撤销DQ、Int、Latefee)
            self.checkIfNeedReverseStatus(trading)

            # 查看是否可以销户
            self.checkClosing()

    # 获取历史最小还款额未还
    # markLabel表示是否要添加label，只有在出账计算最小未还时，添加标签
    def getHistoryUnpaidMinimum(self, markLabel = False) :
        statement = self.lastStatement
        if (statement == None) :
            return 0
        needAssertHistoryUnpaidMinimum = True
        if needAssertHistoryUnpaidMinimum :
            amount = 0
            while(statement != None) :
                for key in PaymentOrderList :
                    unpaidTradingList = statement.unpaidTradingDic[key] + statement.unpaidTradingDicOfPreStatement[key]
                    for unpaidTrading in unpaidTradingList :
                        unpaid = unpaidTrading.unpaidInMinimum.get(statement.bill.number)
                        if not unpaid or unpaid <= 0:
                            continue
                        amount = round_to_even(amount + unpaid)
                        if markLabel:
                            flagName = "MinimumHasHistory" + str(key.name)
                            flag = getattr(StoriMinimumFlag, flagName, None)  
                            self.label.markFlag(flag)
                statement = statement.lastStatement
            assert(round_to_even(amount) == round_to_even(self.lastStatement.unpaidMinimum))
        amount = self.lastStatement.unpaidMinimum
        return round_to_even(amount)
    
    # 获取历史最小还款额未还明细
    def getUnpaidDetail(self) :
        statement = self
        historyUnpaidMinimumDetail = []
        while(statement != None) :
            unpaidMinimumDic = statement.bill.minimumDic.copy()
            unpaidMinimumDic["Unpaid Total"] = statement.unpaidTotal
            historyUnpaidMinimumDetail.insert(0, unpaidMinimumDic)
            statement = statement.lastStatement
        return historyUnpaidMinimumDetail
    
    # 获取当前账单未分配交易明细
    def getUnallocDetail(self) :
        tradingTypes = [tradingType for tradingType in TradingType]
        detailDic = {}
        for tradingType in tradingTypes :
            detailDic[tradingType] = 0
        for trading in self.bill.billedList :
            if trading.leftAmount > 0 :
                detailDic[trading.type] = round_to_even(detailDic[trading.type] + trading.leftAmount)
        return detailDic

    # 收取滞纳金和利息后，判断是否有溢缴款需要对滞纳金和利息进行归还
    def handleRealTimePaymentAfterCharging(self) :
        if self.overTrading == None :
            return
        if (round_to_even(self.overTrading.leftAmount) <= 0) :
            return
        trading = self.overTrading

        for positiveTrading in self.endDayChargingList :
            payment = trading.paymentToPositveTrading(positiveTrading)
            self.bill.recordPayment(trading, positiveTrading, payment, isHistory=False, isOverPayment=True)
            print("归还产生利息之后的： ", positiveTrading.type, payment)

            # label
            if (positiveTrading.type == TradingType.FEE) :
                self.label.markFlag(StoriPaymentFlag.PaymentOverToLateFee)
            elif (positiveTrading.type == TradingType.VAT_FEE) :
                self.label.markFlag(StoriPaymentFlag.PaymentOverToVatLateFee)
            elif (positiveTrading.type == TradingType.INT) :
                self.label.markFlag(StoriPaymentFlag.PaymentOverToInt)
            elif (positiveTrading.type == TradingType.VAT_INT) :
                self.label.markFlag(StoriPaymentFlag.PaymentOverToVatInt)
    
            if (trading.leftAmount <= 0) :
                break

    def handleRealTimePaymentBeforeCharging(self) :
        
        # 如果历史账单没有还清
        if self.lastStatement and round_to_even(self.lastStatement.unpaidTotal) > 0 :
            return
        
        print("本期账单实时还款")
        preList: List[StoriTrade] = [] # 逆向posting之前的交易列表，按照1.PaymentOrderList、2.effective_time排序
        afterList: List[StoriTrade] = [] # 逆向posting之后的交易列表，按照1.posting_time、2.effective_time排序

        # 账单按照posting_time排序
        tradingListByTime = tradingListSortByTime(filter(unpaidFilter, self.bill.billedList))
        # tradingListByTime = list(filter(unpaidFilter, self.bill.billedList))

        # 如果上期账单有溢缴款，插入溢缴款
        if (self.lastStatement != None and self.lastStatement.overTrading and round_to_even(self.lastStatement.overTrading.leftAmount) > 0) :
            tradingListByTime.insert(0, self.lastStatement.overTrading)

        length  = len(tradingListByTime)
        for i in range(length) :
            trading: StoriTrade = tradingListByTime[i]
            # 如果是正向交易，插入preList
            if (trading.isPositiveTrading()) : 
                if (trading.leftAmount > 0) :
                    index = 0
                    while index < len(preList) :
                        if PaymentOrderList.index(trading.type) < PaymentOrderList.index(preList[index].type):
                            break
                        index += 1
                    preList.insert(index, trading)
                continue
            
            # 如何是逆向交易，开始进行还款
            if (trading.leftAmount <=0) : #逆向交易没有未分配的金额
                continue

            # 先归还posting_time之前的
            for positiveTrading in preList:
                payment = trading.paymentToPositveTrading(positiveTrading)
                self.bill.recordPayment(trading, positiveTrading, payment, isHistory=False)  
                print("归还posting_time之前的： ", positiveTrading.type, payment)         

                # label
                flagName = "PaymentToRealtime" + positiveTrading.type.name
                flag = getattr(StoriPaymentFlag, flagName, None)  
                self.label.markFlag(flag)

                # self.label.hasRealtimePaymentToBefore = True
                if (trading.leftAmount <= 0) :
                    break
            
            # 从preList里面过滤掉已经还完的
            preList = list(filter(unpaidFilter, preList))

            # 剩余不够
            if (trading.leftAmount <= 0) :
                continue
            
            assert(len(preList) == 0)
            
            # 如果还有剩下的溢缴款，开始归还后面的

            print("溢缴款")
            afterList = tradingListByTime[i+1:]
            afterList = list(filter(positiveUnpaidFilter, afterList)) # 过滤生成逆向交易posting_time之后的未付正向交易

            # 归还posting_time之后的
            for positiveTrading in afterList :
                payment = trading.paymentToPositveTrading(positiveTrading)

                self.bill.recordPayment(trading, positiveTrading, payment, isHistory=False, isOverPayment=True)
                print("归还posting_time之后的： ", positiveTrading.type, payment)      
                
                flagName = "PaymentOverToRealtime" + positiveTrading.type.name
                flag = getattr(StoriPaymentFlag, flagName, None)  
                self.label.markFlag(flag)
                if (trading.leftAmount <= 0) :
                    break
            
            # 从afterList里面过滤掉已经还完的
            afterList = list(filter(unpaidFilter, afterList))

            # 如果所有都还完
            if (len(afterList) == 0) :
                print("所有都还清")
                break

    # 历史还款分配优先本金
    def handleHistoryPaymentPRINFirst(self, trading:StoriTrade):
        statementList:List[Statement] = []
        statement = self.lastStatement
        while(statement != None) :
            if statement.unpaidTotal <= 0 :
                break
            statementList.insert(0, statement)
            statement = statement.lastStatement
        firstNumber = statementList[0].bill.number
        for tradingType in PaymentOrderListFirstPrin :
            for statement in statementList :
                for unpaidTrading in statement.unpaidTradingDic[tradingType] :
                    if unpaidTrading.leftAmount <= 0 :
                        continue
                    for number in unpaidTrading.unpaidInMinimum :
                        leftAmount = unpaidTrading.unpaidInMinimum[number]
                        if leftAmount <= 0 :
                            continue
                        if trading.leftAmount <= 0:
                            break
                        # print("before", unpaidTrading.unpaidInMinimum[number])
                        payment = min(leftAmount, trading.leftAmount)
                        # print("payment", payment)
                        self.updateUnpaidData(trading, statementList[number-firstNumber], unpaidTrading, payment, tradingType)
                        # print("after", unpaidTrading.unpaidInMinimum[number])
                        # print()
                    if unpaidTrading.leftAmount > 0 and trading.leftAmount > 0:
                        payment = min(unpaidTrading.leftAmount, trading.leftAmount)
                        self.updateUnpaidData(trading, None, unpaidTrading, payment, tradingType)

                    if trading.leftAmount <= 0 :
                        return

    # 逆向交易入账时触发历史账单还款
    def handleHistoryPayment(self, trading:StoriTrade = None):

        # 查找历史账单
        statement = self.lastStatement

        # 如果没有历史账单，返回
        if (statement == None) :
            return

        # 如果历史账单已经还清，返回
        if round_to_even(statement.unpaidTotal) <= 0 :
            return
        
        # 在已经入账的交易中查找逆向的未分配完的交易进行还款分配
        if trading == None :
            for trading in self.bill.billedList :
                if trading.isNegativeTrading() and round_to_even(trading.leftAmount) > 0 :
                    self.handleHistoryPayment(trading)
            return

        # 交易不在当前账期，下个账期再处理
        if (trading and trading.posting_time.date() > self.bill.endDate) :
            return
        
        print("---处理历史账单还款---")
        print("入账金额：", trading.leftAmount, "入账时间", trading.posting_time)
        
        # 如果DQ超出，更换还款方式
        if self.cif.checkDQOverLimit() :
            self.handleHistoryPaymentPRINFirst(trading)
            return
        
        # 查找所有未还清的历史账单
        statementList: List[Statement] = []
        while(statement != None) :
            if (statement.unpaidTotal > 0) :
                statementList.insert(0, statement)
            statement = statement.lastStatement

        print("分配到历史账单未还最小还款：")
        # 先还最小还款额部分
        for statement in statementList :
            if statement.unpaidMinimum <= 0 :
                continue
            for tradingType in PaymentOrderList :
                unpaidTradingList = statement.unpaidTradingDic[tradingType] + statement.unpaidTradingDicOfPreStatement[tradingType]
                for unpaidTrading in unpaidTradingList :
                    amount = trading.leftAmount
                    if amount <= 0 :
                        return
                    unpaid = unpaidTrading.unpaidInMinimum.get(statement.bill.number)
                    if unpaid==None or unpaid <= 0 :
                        continue
                    payment = min(statement.unpaidTotal, unpaid, amount)
                    self.updateUnpaidData(trading, statement, unpaidTrading, payment, tradingType)
                if trading.leftAmount <= 0 :
                    return

        print("分配到历史账单非最小还款部分：")        
        # 再还剩余本金部分
        for statement in statementList :
            if (statement.unpaidTotal <= 0) :
                continue
            for tradingType in PRINTradingListType :
                unpaidTradingList = statement.unpaidTradingDic[tradingType]
                for unpaidTrading in unpaidTradingList :
                    unpaid = unpaidTrading.leftAmount
                    if unpaid <= 0 :
                        continue
                    payment = min(unpaid, trading.leftAmount)
                    self.updateUnpaidData(trading, None, unpaidTrading, payment, tradingType)                
                    if (trading.leftAmount == 0) :
                        return
    
    # 从statement到当前账单self更新每个账单对象的unpaidTotal和unpaidMinimum，以及trading的leftAmount
    # trading: 逆向交易
    # minimumStatement: 最小还款账单
    # positiveTrading : 被还款交易所在账单
    # payament : 还款金额
    # tradingType : 被还款交易类型
    def updateUnpaidData(self, negativeTrading:StoriTrade, minimumStatement, positiveTrading:StoriTrade, payment, tradingType:TradingType) :
        statement = self
        minimumNumber = minimumStatement.bill.number if minimumStatement != None else 0
        while statement.bill.number != positiveTrading.billNumber :
            statement = statement.lastStatement
            if (minimumNumber and round_to_even(statement.unpaidMinimum) != 0 and statement.bill.number >= minimumStatement.bill.number) :
                statement.unpaidMinimum = round_to_even(statement.unpaidMinimum - payment)
            statement.unpaidTotal = max(0, round_to_even(statement.unpaidTotal - payment))
            assert( round_to_even(statement.unpaidMinimum) >= 0)
        negativeTrading.leftAmount = round_to_even(negativeTrading.leftAmount - payment)
        negativeTrading.paymentDic[tradingType] = round_to_even(negativeTrading.paymentDic[tradingType] + payment)
        assert(negativeTrading.leftAmount >= 0)

        positiveTrading.leftAmount = round_to_even(positiveTrading.leftAmount - payment)
        if minimumNumber > 0 :
            positiveTrading.unpaidInMinimum[minimumNumber] = round_to_even(positiveTrading.unpaidInMinimum[minimumNumber]-payment)
            assert(positiveTrading.unpaidInMinimum[minimumNumber]>=0)
        assert(positiveTrading.leftAmount >= 0)

        print("账期：", minimumStatement.bill.statementDate if minimumStatement else statement.bill.statementDate , "金额：", payment)

        isOverDQ = self.cif.checkDQOverLimit()
        self.bill.recordPayment(negativeTrading, positiveTrading, payment, minimumNumber=minimumNumber, isOverDQ=isOverDQ)

        # label
        if isOverDQ :
            flagName = "PaymentToAll"
        else :
            if minimumNumber :
                flagName = "PaymentToHistoryMinimum"
            else :
                flagName = "PaymentToHistory"
        flagName += tradingType.name
        flag = getattr(StoriPaymentFlag, flagName, None)  
        self.label.markFlag(flag)

    def handlePayment(self, trading:StoriTrade) :
        print("处理还款")
        self.handleHistoryPayment(trading)
        # self.handleRealTimePaymentBeforeCharging()

    # def handleRefund(self, trading) :
    #     print("处理退款")
    #     self.handleHistoryPayment(trading)

    def findTargertTradingById(self, tid, findChangeTid = False, posted = False) -> StoriTrade: 
        if posted :
            tradingList = self.bill.billedList
        else :
            tradingList = self.unbilledList
        # tradingList = reversed(self.unbilledList)
        for trade in tradingList:
            if trade.tid == tid :
                return trade
            if findChangeTid and trade.changeTid == tid :
                return trade
        if (tid == "${__UUID}") :
            print(tid)
        else :
            print(tid)
        return None
    
    def postingInstallment(self) :
        for installment in self.installmentList.copy() :
            
            curIns : List[StoriTrade] = installment.getCurInstallmentTrading()
            if (curIns == None) :
                continue
            for trading in curIns :
                # 因为trading入账会扣额度，但是分期额度已经占用过了，因此额度先增加额度
                self.cif.availableLimit = round_to_even(self.cif.availableLimit + trading.amount)
                if trading.effective_time == None :
                    effective_time = datetime.combine(self.bill.endDate,  time(23,59))
                else :
                    effective_time = trading.effective_time
                self.processTrading(trading, effective_time)
            installment.posting()
            if self.cif.checkCancelInstallment() :
                self.cancelInstallment(installment)
        print("分期入账")

    def adjustInsPostDate(self) :
        self.insAdjusted = True
        if self.curDate + timedelta(days=1) == self.bill.statementDate :
            if self.installmentPosted == False:
                self.postingInstallment()
                self.installmentPosted = True

    def cancelInstallment(self, installment:Installment, onlyPrin=False) :
        print("取消剩余分期")

        if installment == None :
            for installment in self.installmentList :
                self.cancelInstallment(installment, onlyPrin)
            return

        leftTradings : List[StoriTrade] = installment.getLeftTradings()

        for index, trading in enumerate(leftTradings) :
            # 额度恢复
            effective_time = self.curTime
            self.cif.availableLimit = round_to_even(self.cif.availableLimit + trading.amount)
            if index == 0 and self.insAdjusted == False :
                effective_time = datetime.combine(self.bill.startDate + timedelta(days=1), time())

            if trading.type in [TradingType.INS_PRIN, TradingType.INS_PRIN_MSI]:
                trading.type = TradingType.PRIN
                self.processTrading(trading, effective_time)
            elif onlyPrin == False :
                self.processTrading(trading, effective_time)

        installment.cancel()
        self.installmentList.remove(installment)

        self.label.markFlag(StoriInstallmentFlag.InstallmentCancel)

    def findInstallmentById(self, insId) :
        for installment in self.installmentList :
            if installment.insId == insId :
                return installment
        return None
    
    def findCanInstallmentTrading(self, number) :
        index = 0
        for trading in list(reversed(self.bill.billedList)) :
            if trading.type != TradingType.PRIN :
                continue
            if not trading.canIns :
                continue
            if index == number :
                return trading
            else :
                index += 1

    def handleInstallmentTrading(self, tid, data:dict) :
        
        trading = self.findTargertTradingById(tid, posted=True)
        if trading == None :
            return

        if not self.cif.checkCanInstallment():
            self.label.markFlag(StoriInstallmentFlag.InstallmentDQReject)
            print("DQ不能分期")
            return
        principal = int(data["principal"])
        if principal < 100 :
            self.label.markFlag(StoriInstallmentFlag.InstallmentLowerAmount)
            print("金额小于100不能分期")
            return

        periods = int(data["periods"])
        insId = data.get("installmentId")
        msi = data.get("msi")
        installment = Installment(periods, principal, trading.tid, insId=insId, msi = msi)

        total = round_to_even(installment.totalAmount/100)
        if (round_to_even(self.cif.availableLimit + principal/100) < total) :
            self.label.markFlag(StoriInstallmentFlag.InstallmentOverLimit)
            print("额度超限不能分期")
            return
        
        self.installmentList.append(installment)
        
        # 调整交易
        adjustmentTrading = StoriTrade(TradingType.ADJ_NEGATIVE, installment.principal / 100, effective_time=self.curTime)
        adjustmentTrading.priorityTid = tid
        
        # 交易入账
        self.processTrading(adjustmentTrading, self.curTime)

        # 额度更新
        self.cif.availableLimit = round_to_even(self.cif.availableLimit - total)

        trading.canIns = False

        self.label.markFlag(StoriInstallmentFlag.InstallmentCreate)

        if msi :
            print()
        else :
            flagName = "InstallmentPeriod" + str(periods)
            flag = getattr(StoriInstallmentFlag, flagName, None)  
            self.label.markFlag(flag)
        
    
    def handleMarketingCancelBenefit(self, benifit_no = None) :
        print("撤销领取权益")
        benifit = self.cif.freeIntBenefit(benifit_no)
        if (benifit) :
            benifit["status"] = "CANCELED"
            self.label.markFlag(StoriFreeIntCouponFlag.FreeIntCouponCancelled)
    
    def handleMarketingExpiredBenefit(self, benifit_no = None) :
        print("权益失效")
        benifit = self.cif.freeIntBenefit(benifit_no)
        if benifit :
            benifit["status"] = "EXPIRED"
            self.label.markFlag(StoriFreeIntCouponFlag.FreeIntCouponExpired)

    def handleMarketingAddBenefit(self, marketingBenefit) :
        benifit = {}

        usageRules = marketingBenefit["instanceRules"]["usageRules"]
        effectiveStartTime = usageRules["effectiveStartTime"]
        effectiveEndTime = usageRules["effectiveEndTime"]
        format = '%Y-%m-%dT%H:%M:%S'
        benifit["effectiveStartTime"] = datetime.strptime(effectiveStartTime, format)
        benifit["effectiveEndTime"] = datetime.strptime(effectiveEndTime, format)
        benifit["status"] = "UNUSE"
        # benifit["expiredTriggered"] = False

        benefitType = marketingBenefit["instance"]["benefitType"]
        benifit["benefitType"] = benefitType
        if "benefit_no" in marketingBenefit :
            benifit["benefit_no"] = marketingBenefit["benefit_no"]
        self.cif.benefits.append(benifit)

        if benefitType == "INTEREST_COUPON" :
            self.label.markFlag(StoriFreeIntCouponFlag.FreeIntCouponBenifit)

        print("营销权利：", benefitType)

    # 开卡
    def handleOpenCard(self) :
        print("开卡")

        adjustment = self.cif.getOpenFee()
        adjustment = adjustment / 100.0
        openFee =  adjustment/ (1+ VAT_RATE)

        if (adjustment != 0) :
            self.handleOriginTrading(adjustment, tradingType=TradingType.ADJ_NEGATIVE, isPomelo=False)
            self.handleOriginTrading(openFee, tradingType=TradingType.FEE, isPomelo=False)

    def handleActiveCard(self, cardId) :
        print("激活卡")
        self.cif.activeCard(cardId)
        self.label.markFlag(StoriStatementFlag.StatementHasActiveCard)

    # 换卡
    def handleChangeCard(self, data, cardId) :
        print("换卡")
        reason = data["reason"]
        chargeReasons = ["DAMAGE", "PIN_BLOCK", "LOST", "STOLEN", "NON_DELIVERY"]
        # notChargeReasons = ["STOLEN_IN_DELIVERY", "FRAUD_CONFIRMED", "CARD_EXPIRATION"]
        cardReplacementFee = self.cif.getCardReplacementFee()
        exchangeFee = cardReplacementFee / 100.0
        if self.cif.checkExchangeCard() :
            if self.label.getMarkedFlag(StoriDQFlag.DQReversedTrigger) :
                self.label.markFlag(StoriDQFlag.DQ0CanExchangeCardAfterReverse)
            if (cardReplacementFee != 0 and reason in chargeReasons) :
                self.handleOriginTrading(exchangeFee, tradingType=TradingType.FEE, isPomelo=False)
                self.label.markFlag(StoriChargingFlag.ChargingExchangeFee)
            else :
                self.label.markFlag(StoriChargingFlag.ChargingNoExchangeFee)
            self.cif.exchangeCard(cardId)
        else :
            print("DQ block 不能换卡")
            self.label.markFlag(StoriDQFlag.DQ1CanNotExchangeCard)

    # 交易检查
    def checkTradingEnabled(self, tradingType, isPomelo) :
        if not isNegativeType(tradingType) :
            if not self.cif.checkTrading() :
                print("DQ in bucket 1，不能发生交易")
                if (isPomelo) :
                    self.label.markFlag(StoriDQFlag.DQBucket1CannotAuth)
                else :
                    self.label.markFlag(StoriDQFlag.DQBucket1CannotAppTxn)
                return False
            elif self.cif.getDQDueBucket() == 1 :
                if (isPomelo) :
                    if self.label.getMarkedFlag(StoriDQFlag.DQReversedTrigger) :
                        self.label.markFlag(StoriDQFlag.DQ1CanAuthAfterReverse)
                    else :
                        self.label.markFlag(StoriDQFlag.DQ1CanAuth)
                else :
                    if self.label.getMarkedFlag(StoriDQFlag.DQReversedTrigger) :
                        self.label.markFlag(StoriDQFlag.DQ1CanAppTxnAfterReverse)
                    else :
                        self.label.markFlag(StoriDQFlag.DQ1CanAppTxn)
        return True
    
    # 处理交易
    def processTrading(self, trading:StoriTrade, tradingTime, sync = True) :

        amount = trading.amount

        # 检查额度
        if self.cif.availableLimit < amount :
            if trading.type == TradingType.PRIN :
                print("额度不够")
                self.label.markFlag(StoriTradingFlag.TradingAuthFailedForOverLimit)
                return
        
        # 交易记账
        self.pendingTrading(trading, tradingTime)
        if sync : # 如果是同步交易，立刻入账
            self.postingTrading(trading, tradingTime, amount)
            
            if (trading.type == TradingType.PAYMENT) :
                self.label.markFlag(StoriTradingFlag.TradingHasAppPayment)

        print("add trade :", trading.type, amount, "同步" if sync else "异步")

    def handleOriginTrading(self, amount, tradingType = TradingType.PRIN, isPomelo = True,  tid = None, sync = True, curTime = None, installments = None) :       
        # 检查交易是否可以进行
        if self.checkTradingEnabled(tradingType, isPomelo) == False :
            return False

        if curTime == None :
            curTime = self.curTime

        # 创建交易
        originTrading = StoriTrade(tradingType=tradingType, amount=amount, tid=tid, installments=installments)

        # 处理交易
        self.processTrading(originTrading, curTime, sync)

        # 如果是费，自动生成税
        if tradingType == TradingType.FEE :
            vatTrading = StoriTrade(TradingType.VAT_FEE, amount * VAT_RATE, effective_time=curTime)
            self.processTrading(vatTrading, curTime)

        # label
        if isPomelo :
            if tradingType == TradingType.PRIN :
                self.label.markFlag(StoriTradingFlag.TradingHasPomeloPurchaseAuth)
            elif tradingType == TradingType.REFUND :
                self.label.markFlag(StoriTradingFlag.TradingHasPomeloRefundAuth)
            elif tradingType == TradingType.PAYMENT :
                self.label.markFlag(StoriTradingFlag.TradingHasPomeloPaymentAuth)
        else :
            if (tradingType == TradingType.PRIN) :
                self.label.markFlag(StoriTradingFlag.TradingHasAppPurchaseAuth)
            elif tradingType == TradingType.PAYMENT :
                self.label.markFlag(StoriTradingFlag.TradingHasAppPayment)
        return True
    
    def handlePostingTrading(self, tid, trading:StoriTrade = None, amount = 0, isPomelo = True, curTime = None, installments:dict = None) :
        if trading == None :
            trading = self.findTargertTradingById(tid)
        if trading == None :
            return
        
        if curTime == None :
            curTime = self.curTime
        
        posted = self.postingTrading(trading, curTime, amount)

        if installments and installments == trading.installments:
            try :
                quantity = int(installments.get("quantity"))
            except :
                quantity = 0
            credit_type = installments.get("credit_type")
            if quantity >= 2 and credit_type == "WITHOUT_INTEREST" :
                data = {"principal": round_to_even(trading.amount * 100, 0) , "periods":quantity, "msi":True}
                self.handleInstallmentTrading(trading.tid, data=data)
        
        # label
        if posted :
            if isPomelo :
                if trading.type == TradingType.PRIN :
                    self.label.markFlag(StoriTradingFlag.TradingHasPostedPomeloPurchase)
                elif trading.type == TradingType.REFUND :
                    self.label.markFlag(StoriTradingFlag.TradingHasPostedPomeloRefund)
                elif trading.type == TradingType.PAYMENT :
                    self.label.markFlag(StoriTradingFlag.TradingHasPostedPomeloPayment)
            else :
                if (trading.type == TradingType.PRIN) :
                    self.label.markFlag(StoriTradingFlag.TradingHasPostedAppPurchase)

            if trading.isNegativeTrading() :
                self.label.markFlag(StoriTradingFlag.TradingHasPostedNegative)
            else :
                self.label.markFlag(StoriTradingFlag.TradingHasPostedPositive)

            if trading.isEffectBeforeCycle(self.bill.startDate) :
                if trading.isNegativeTrading() :
                    self.label.markFlag(StoriTradingFlag.TradingPostingHistoryNegative)
                else :
                    self.label.markFlag(StoriTradingFlag.TradingPostingHistoryPositive)
    
    def updateBalance(self, trading:StoriTrade, checkDate = True) :
        if (checkDate and trading.posting_time.date() > self.bill.endDate) :
            return
        if trading.isNegativeTrading() :
            self.cif.balance = round_to_even(self.cif.balance - trading.amount)
        else :
            self.cif.balance = round_to_even(self.cif.balance + trading.amount)
    
    def updateCredit(self, trading:StoriTrade) :
        if trading.isNegativeTrading() :
            self.cif.availableLimit = round_to_even(self.cif.availableLimit + trading.amount)
        else :
            self.cif.availableLimit = round_to_even(self.cif.availableLimit - trading.amount)
            if self.cif.availableLimit < 0 :
                self.label.markFlag(StoriTradingFlag.TradingOverLimit)

    def handleRejectedTrading(self, tid, trading:StoriTrade = None, amount = 0, cancel = False) :
        if trading == None :
            trading = self.findTargertTradingById(tid, findChangeTid=True)
        if trading == None :
            return
        if cancel :
            amount = trading.amount
        reversed = trading.reverse(amount)
        if reversed :
            self.cif.availableLimit = round_to_even(self.cif.availableLimit + amount)

            # label
            if (trading.type == TradingType.PAYMENT) :
                self.label.markFlag(StoriTradingFlag.TradingHasPaymentReversal)
            elif (trading.type == TradingType.REFUND) :
                self.label.markFlag(StoriTradingFlag.TradingHasRefundReversal)
            elif (trading.type == TradingType.PRIN) :
                if (len(trading.changedList)==2) :
                    self.label.markFlag(StoriTradingFlag.TradingHasPurchaseReversal)
                elif (len(trading.changedList) > 2) :
                    if (trading.changedList[-2] > 0) :
                        self.label.markFlag(StoriTradingFlag.TradingHasIncreaseReversal)
                    else :
                        self.label.markFlag(StoriTradingFlag.TradingHasDecreaseReversal)
        elif trading.status == TradingStatus.POSTED :
            self.label.markFlag(StoriTradingFlag.TradingReversalPostedFailed)
        elif trading.status == TradingStatus.REJECTED :
            self.label.markFlag(StoriTradingFlag.TradingReversalRejectedFailed)

        if trading.isEffectBeforeCycle(self.bill.startDate) :
            self.label.markFlag(StoriTradingFlag.TradingReversalHistoryPending)

    def handleAdjustmentTrading(self, amount, type, subType) :
        if (type in ["ADJUSTMENT"]) :
            tradingType = TradingType.ADJ_NEGATIVE
            self.label.markFlag(StoriAdjustmentFlag.AdjustmentNegative)
        elif type == "ADJ_PRINCIPAL" :
            tradingType = TradingType.PRIN
            self.label.markFlag(StoriAdjustmentFlag.AdjustmentPRIN)
        elif type == "ADJ_FEE" :
            tradingType = TradingType.FEE
            self.label.markFlag(StoriAdjustmentFlag.AdjustmentFEE)
        elif type == "ADJ_VAT" :
            if (subType in ["LATE_FEE", "OPEN_FEE", "CARD_REPLACEMENT_FEE", "DISPUTE_FEE"]) :
                tradingType = TradingType.VAT_FEE
                self.label.markFlag(StoriAdjustmentFlag.AdjustmentVAT_FEE)
            elif (subType == "INTEREST") :
                tradingType = TradingType.VAT_INT
                self.label.markFlag(StoriAdjustmentFlag.AdjustmentVAT_INT)
        elif type == "ADJ_INTEREST" :
            tradingType = TradingType.INT
            self.label.markFlag(StoriAdjustmentFlag.AdjustmentINT)
        else :
            assert("0")

        # 创建交易
        originTrading = StoriTrade(tradingType=tradingType, amount=amount)

        # 处理交易
        self.processTrading(originTrading, self.curTime)

        if tradingType == TradingType.FEE and subType != "LATE_FEE" :
            originTrading = StoriTrade(tradingType=TradingType.VAT_FEE, amount=amount * VAT_RATE)
            self.processTrading(originTrading, self.curTime)


    def handleChangeTrading(self, tid, originTid, trading:StoriTrade = None, amount = 0, fromPomelo = True) :
        if trading == None :
            trading = self.findTargertTradingById(originTid)
        if trading == None :
            return
        changed = trading.change(amount, tid)
        if changed :
            self.cif.availableLimit = round_to_even(self.cif.availableLimit - amount)
            # label 
            if (fromPomelo) :
                if (amount > 0) :
                    self.label.markFlag(StoriTradingFlag.TradingHasPomeloIncrease)
                elif (amount < 0) :
                    self.label.markFlag(StoriTradingFlag.TradingHasPomeloDecrease)
            else :
                self.label.markFlag(StoriTradingFlag.TradingHasUserIncrease)
        elif trading.status == TradingStatus.POSTED :
            if (amount > 0) :
                self.label.markFlag(StoriTradingFlag.TradingIncreasePostedFailed)
            else :
                self.label.markFlag(StoriTradingFlag.TradingDecreasePostedFailed)
        elif trading.status == TradingStatus.REJECTED :
            if (amount > 0) :
                self.label.markFlag(StoriTradingFlag.TradingIncreaseRejectedFailed)
            else :
                self.label.markFlag(StoriTradingFlag.TradingDecreaseRejectedFailed)

    def checkNeedCalLateFee(self):
        if self.lastStatement == None :
            return False
        
        payment = 0
        for trading in self.bill.billedList :
            if not trading.isNegativeTrading() :
                continue
            date = trading.effective_time.date()
            if (date <= self.getLastGraceDate()) :
                payment += trading.amount
        
        unpaid = round_to_even(self.lastStatement.bill.minimumPayment - payment)
        self.updateGraceDayUnpaidMinimum(unpaid)
        if (unpaid > 0) :
            self.label.markFlag(StoriPaymentFlag.PaymentNotInMinimumBeforeGraceDay)
        else :
            self.label.markFlag(StoriPaymentFlag.PaymentInMinimumBeforeGraceDay)

        if self.cif.checkNotChargeIntAndLateFee() :
            return False
        
        if unpaid > 0 :
            return True
        return False
    
    def checkNeedCalInterest(self):
        if self.lastStatement == None :
            return False

        payment = 0
        hasPayment = False # 是否有主动还款
        for trading in self.bill.billedList :
            if not trading.isNegativeTrading() :
                continue
            date = trading.effective_time.date()
            if (date <= self.getLastDueDate()) :
                if trading.type == TradingType.PAYMENT and trading.amount > 0:
                    hasPayment = True
                payment += trading.amount
        
        if hasPayment :
            self.label.markFlag(StoriPaymentFlag.PaymentActiveBeforeDueDay)

        unpaid = max(0, round_to_even(self.lastStatement.bill.totalPayment - payment))
        self.updateDueDayUnpaidTotal(unpaid)
        if (unpaid > 0) :
            self.label.markFlag(StoriPaymentFlag.PaymentNotInFullBeforeDueDay)
        else :
            self.label.markFlag(StoriPaymentFlag.PaymentInFullBeforeDueDay)

        if unpaid <= PAYMENT_Grace_Amount :
            self.label.markFlag(StoriPaymentFlag.PaymentReachGraceAmountBeforeDueDay)

        # due day前最小还款
        unpaidMinimum = max(0, round_to_even(self.lastStatement.bill.minimumPayment - payment))
        self.updateDueDayUnpaidMinimum(unpaidMinimum)

        if unpaidMinimum > 0 :
            self.label.markFlag(StoriPaymentFlag.PaymentNotInMinimumBeforeDueDay)
        else :
            self.label.markFlag(StoriPaymentFlag.PaymentInMinimumBeforeDueDay)

        if self.cif.checkNotChargeIntAndLateFee() :
            return False
        if unpaid <= 0 :
            return False
        
        if self.checkPaymentGrace(unpaid, unpaidMinimum, hasPayment) :
            return False
        if unpaid > 0 :
            return True
        return False
    
    # payment grace
    def checkPaymentGrace(self, unpaid, unpaidMinimum, hasPayment) :
        if APPLY_NEW_Grace_Amount :
            if unpaid > PAYMENT_Grace_Amount :
                return False
            if not hasPayment :
                return False
            if unpaidMinimum > 0 :
                return False
            if unpaid > 0 :
                self.label.markFlag(StoriChargingFlag.IntHasGraced)
            return True
        else :
            return False
        
    def generateBill(self) :
        print("---出账---")
        
        self.cif.DQEnabledDate = self.curDate
        self.cif.updateDQDays(self.curDate)

        assert(self.curDate- timedelta(days=1)==self.bill.endDate)

        if self.billing == True :
            assert(0)

        self.billing = True
        
        # self.genBillList()

        # 本期账单还款分配
        # 计算ADB依赖逆向交易还款分配的情况，因此需要在计算ADB之前进行分配
        self.handleRealTimePaymentBeforeCharging()

        # 计算溢缴款
        # 需要带入下一期账单中计算还款分配和ADB，保存在overTrading中
        # 溢缴款对利息和滞纳金的还款分配算在下一个账期，因此需要在滞纳金和利息计算之前获取balance值进行计算
        self.calOverPayment()

        # 计算滞纳金和税，加入本期账单列表
        # 需要带入下一账单中计算ADB， 保存在endDayChargingList中
        if self.checkNeedCalLateFee() :
            self.calLateFee()
        
        # 生成ADBList
        # 利息依赖abd的结果，需要在利息计算之前
        self.genADBList()

        # 计算利息和税，加入本期账单列表
        # 需要带入下一账单中计算ADB， 保存在endDayChargingList中
        if self.checkNeedCalInterest() :
            self.calInterest()            
        
        # 生成balanceList()
        # 扣除了本期的滞纳金和利息，需要在利息和滞纳金之后生成
        self.genBalanceList()

        # 生成滞纳金和利息后，如果还有溢缴款，需要对滞纳金和利息和相应的税做还款
        # 利息和滞纳金的交易在本期账单中体现，是否还款会影响到本期账单的还款总额和最小还款额
        self.handleRealTimePaymentAfterCharging()

        print("已出账单：", self.bill.startDate, "--", self.bill.endDate)

        # 计算还款总额
        self.calTotalPayment()

        # 计算最小还款额
        self.calMinimumPayment()

        # 账单状态修改为已出账
        self.isBilled = True

        # 更新未分配交易明细
        self.bill.unallocDetail = self.getUnallocDetail()

        # 断言doublecheck一下余额
        if (self.lastStatement != None) :
            balance = round_to_even(self.cif.balance)           
            assert(balance == self.bill.getEndBalance())
            if balance > 0 :
                assert(balance == self.bill.totalPayment)

        # label
        # self.label.markFlag(StoriStatementFlag.StatementHasBilled)
        self.label.autoMarkUnions()


    # 计算本期账单溢缴款
    def calOverPayment(self) :
        print("计算溢缴款：")
        overAmount = 0
        # endBalance = self.cif.balanceList[-1].endBalance
        endBalance = self.cif.balance
        if (endBalance < 0) :
            overAmount = -endBalance
            print(overAmount)

        if round_to_even(overAmount) <= 0 :
            self.overTrading = None
            return
        
        # time = datetime(self.statementDate.year, self.statementDate.month, self.statementDate.day)
        overTrading = StoriTrade(tradingType= TradingType.PAYMENT, status = TradingStatus.POSTED, effective_time = self.curTime, amount=overAmount)
        self.overTrading = overTrading 

        self.label.markFlag(StoriPaymentFlag.PaymentOverflowBeforeStatement)

    # 计算本期账单滞纳金
    def calLateFee(self) :
        print("计算滞纳金： ")
        lateFeeMaxAmount = self.cif.getLateFeeMaxAmount()/100.0
        isTire = self.cif.getLateFeeMethod() == "tier"
        unpaidMinimum = round_to_even(self.getGraceDayUnpaidMinimum())
        lateFeeAmount = 0
        if isTire :
            if (unpaidMinimum >= 9.99 and unpaidMinimum<=34.99) :
                lateFeeAmount = unpaidMinimum
            elif unpaidMinimum > 34.99 :
                lateFeeAmount = lateFeeMaxAmount
        else :
            if unpaidMinimum > 50 :
                lateFeeAmount = lateFeeMaxAmount

        time = datetime(self.curDate.year, self.curDate.month, self.curDate.day)
        
        self.lateFeeTrading = StoriTrade(TradingType.FEE, lateFeeAmount)
        self.vatLateFeeTrading = StoriTrade(TradingType.VAT_FEE, lateFeeAmount * VAT_RATE)
        self.endDayChargingList.append(self.lateFeeTrading)
        self.endDayChargingList.append(self.vatLateFeeTrading)
        
        # 滞纳金和税入账
        self.processTrading(self.lateFeeTrading, time)
        self.processTrading(self.vatLateFeeTrading, time)

        print("滞纳金： ", self.lateFeeTrading.amount)
        print("滞纳金税： ", self.vatLateFeeTrading.amount)

        self.bill.lateFee = lateFeeAmount
        self.bill.vatLateFee = self.vatLateFeeTrading.amount

        # label
        if lateFeeAmount > 0:
            self.label.markFlag(StoriStatementFlag.StatementHasLateFee)
            if lateFeeAmount == unpaidMinimum :
                self.label.markFlag(StoriChargingFlag.ChargingMinimumLateFee)
            else :
                self.label.markFlag(StoriChargingFlag.ChargingContractLateFee)

    def genBalanceList(self) :
        
        print("计算balance：")

        # 初始化第一天的balance，为上期最后一天的endbalance或者0
        originBalance = self.lastStatement.bill.getEndBalance() if self.lastStatement != None else 0.0
        self.bill.previousBalance = round_to_even(originBalance)
        
        # 按照posting_time日期给交易分类
        tradingDic = {}
        tradingDic[self.bill.startDate] = []
        tradingDic[self.bill.endDate] = []
        for trading in self.bill.billedList :
            date = trading.posting_time.date()
            if (date < self.bill.startDate) :
                tradingDic[self.bill.startDate].append(trading)
                continue
            if date in tradingDic :
                tradingDic[date].append(trading)
            else :
                tradingDic[date] = [trading]

        # 滞纳金/利息和相应的税，归属到最后一天
        # 入账时间在endDate+1，需要额外添加
        tradingDic[self.bill.endDate].extend(self.endDayChargingList)

        # 计算每天的balance
        balanceList = DayBalance.genBalanceList(self.bill.startDate, self.bill.endDate, originBalance, tradingDic)
        self.bill.balanceList = balanceList
        self.bill.newBalance = round_to_even(balanceList[-1].endBalance - self.bill.previousBalance)

    # def genBillList(self) : 
    #     for trading in self.unbilledList :
    #         if (trading.status == TradingStatus.PENDING) :
    #             self.label.markFlag(StoriStatementFlag.StatementHasPendingTrading)

    #     # 第一期，去除开卡3笔交易
    #     self.label.markFlag(StoriStatementFlag.StatementHasNoTrading)

    def genADBList(self, endDate=None) :
        print("计算ADB： ")
        
        tradingDic = {} # 保持每天的ADB信息

        lastStatement = self.lastStatement

        # 初始化originBalance，0 or 上一期adb最后一天的endBalance
        # originBalance = lastStatement.bill.adbList[-1].endBalance if lastStatement != None else 0
        originBalance = self.cif.adbBalance

        assert(originBalance >= 0)

        # 带入上期的溢缴款/滞纳金/利息，归属到第一天
        if (lastStatement != None) :
            if (lastStatement.overTrading != None) :
                tradingDic[self.bill.startDate] = [lastStatement.overTrading]
            else :
                tradingDic[self.bill.startDate] = []
            tradingDic[self.bill.startDate].extend(lastStatement.endDayChargingList)

        # 按照effective_time日期给交易分类，小于第一天的也归属到第一天
        for trading in self.bill.billedList :
            date = trading.effective_time.date()
            if (date < self.bill.startDate) :
                tradingDic[self.bill.startDate].append(trading)
            else :
                if date in tradingDic :
                    tradingDic[date].append(trading)
                else :
                    tradingDic[date] = [trading]
            
        if endDate == None :
            endDate = self.bill.endDate
        # 计算每天的ADB
        self.bill.adbList = DayBalance.genBalanceList(self.bill.startDate, endDate, originBalance, tradingDic, isADB=True)
        self.cif.adbBalance = self.bill.adbList[-1].endBalance

        # 如果没有计算利息，没有label
        if self.checkNeedCalInterest() == False :
            return
        
        # label
        if (originBalance > 0) :
            self.label.markFlag(StoriChargingFlag.IntADBHasOrigin)
        else :
            self.label.markFlag(StoriChargingFlag.IntADBHasNoOrigin)
        
        for adb in self.bill.adbList :
            for detail in adb.adbDetailList :
                name = detail[0]
                amount = detail[1]
                flagName = "IntADBHas" + name
                if (amount > 0) :
                    flagName = "IntADBHas" + name
                else :
                    flagName = "IntADBHasPaymentTo" + name
                flag = getattr(StoriChargingFlag, flagName, None)
                self.label.markFlag(flag)

    def calInterest(self) :

        print("计算利息： ")

        bill:StoriBill = self.bill

        bill.calInt()

        curTime = datetime(self.curDate.year, self.curDate.month, self.curDate.day)

        free = False
        for benifit in self.cif.benefits :
            if benifit["status"] != "UNUSE" :
                continue
            if benifit["benefitType"] != "INTEREST_COUPON" :
                continue
            effectiveStartTime = benifit["effectiveStartTime"]
            effectiveEndTime = benifit["effectiveEndTime"]
            time1 = datetime.combine(bill.startDate + timedelta(days=3), time(0, 0, 0))
            time2 = datetime.combine(bill.endDate - timedelta(days=3), time(0, 0, 0))
            if (effectiveStartTime > time1) :
                self.label.markFlag(StoriFreeIntCouponFlag.FreeIntCouponStartTimeExceed)
                continue
            if (effectiveEndTime < time2) :
                self.label.markFlag(StoriFreeIntCouponFlag.FreeIntCouponEndTimeExceed)
                continue
            # if (benifit["expiredTriggered"] == True and effectiveEndTime < self.curTime) :
            #     continue
            free = True
            benifit["status"] = "USED"
            self.label.markFlag(StoriFreeIntCouponFlag.FreeIntCouponUsed)
            break                

        print("利息：", bill.totalInterest)
        print("利息税：", bill.vatInterest)
        print("adb：", bill.adb)

        if (free) :
            print("免除本期利息")
            bill.vatInterest = 0
            bill.totalInterest = 0
        else :
            # 利息入账
            self.interestTrading = StoriTrade(TradingType.INT, amount=bill.totalInterest, effective_time=curTime)
            self.endDayChargingList.append(self.interestTrading)
            self.processTrading(self.interestTrading, curTime)

            # 税入账
            self.vatInterestTrading = StoriTrade(TradingType.VAT_INT, amount=bill.vatInterest, effective_time = curTime)
            self.endDayChargingList.append(self.vatInterestTrading)
            self.processTrading(self.vatInterestTrading, curTime)

            self.label.markFlag(StoriStatementFlag.StatementHasINT)

    def calTotalPayment(self) :
        # 本期账单列表中未还的额度+历史账单中未还的额度

        # add this cycle
        amount = 0.00 
        if (self.lastStatement != None) :
            amount = self.lastStatement.bill.getEndBalance()

        for trading in self.bill.billedList :
            if (trading.isNegativeTrading()) :
                change = -trading.amount
            else :
                change = trading.amount
            amount += change
            print(trading.amount, trading.leftAmount , " ", trading.status,  " ", trading.type, " ", trading.posting_time)

        self.unpaidTotal = round_to_even(max(0,amount))
        self.bill.totalPayment = round_to_even(max(0,amount))

        print("还款总额：")
        print(self.unpaidTotal)

        self.dueDayUnpaidTotal = self.unpaidTotal

    def calMinimumPayment(self) :
        print("计算最小还款额：")

        bill = self.bill

        if self.cif.checkDQ() :
            bill.accountDQ = "DQ"
            bill.dqDays = self.cif.getDQDays()
            bill.dqBucket = self.cif.getDQBucket()
            bill.dueBucket = self.cif.getDQDueBucket()
            bill.dqBlockCode = self.cif.getBlockCode()
            bill.dqBlockReason = self.cif.getBlockReason()

        installmentInMinimumS2 = 0 #最小还款额中分期部分
        allButPrincipal = 0 #最小还款额所有非本金部分

        for key in PaymentOrderList :
            bill.minimumDic[key] = 0.0

        for trading in self.bill.billedList :
            if trading.isNegativeTrading() :
                continue
            leftAmount = round_to_even(trading.leftAmount)
            if leftAmount <=0 :
                continue
            tradingType:TradingType = trading.type
            self.unpaidTradingDic[tradingType].append(trading)
            if tradingType not in PRINTradingListType:
                amount = bill.minimumDic[tradingType]
                bill.minimumDic[tradingType] = round_to_even(amount + leftAmount)
                allButPrincipal += leftAmount
                if not APPLY_NEW_Installment_RULES and isInstallmentType(tradingType):
                    installmentInMinimumS2 += leftAmount
                trading.unpaidInMinimum[self.bill.number] = leftAmount
                
                flagName = "MinimumHas" + str(tradingType.name)
                flag = getattr(StoriMinimumFlag, flagName, None)  
                self.label.markFlag(flag)

        # 历史未还最小还款额
        historyUnpaidMinimum = self.getHistoryUnpaidMinimum(markLabel=True)
        
        print("历史未还最小：", historyUnpaidMinimum)
        allButPrincipal += historyUnpaidMinimum
        bill.historyUnpaidMinimum = historyUnpaidMinimum

        endBalance = round_to_even(self.bill.getEndBalance())

        creditLine = self.cif.creditLine
        allButPrincipalAndFee = allButPrincipal - bill.minimumDic[TradingType.FEE]
        temp1 = round((endBalance - allButPrincipalAndFee) * (0.015), 8)
        s1 = round_to_even(round_to_even(temp1) + allButPrincipalAndFee)
        s3 = round_to_even(round_to_even((endBalance - allButPrincipal) * 0.016) + allButPrincipal)
        s2 = round_to_even(creditLine * 0.0125 + historyUnpaidMinimum + installmentInMinimumS2)

        # if (s1 >= 0 and s3 >=0) :
        #     assert(s1<=s3)
        assert(abs(s1) <= abs(endBalance))
        assert(abs(s3) <= abs(endBalance))
        
        if (endBalance < MINIMUM_PAYMENT_THRESHOLD) : # 如果账单总额小于threshold，最小还款是账单总额
            minimumPayment = max(0, min(endBalance, MINIMUM_PAYMENT_THRESHOLD))
            self.label.markFlag(StoriMinimumFlag.MinimumEqualBalanceLessThenThreshold)
        else :
            if (s2 <= endBalance and s2 > MINIMUM_PAYMENT_THRESHOLD and s2>=s1 and s2>=s3) :
                minimumPayment = s2 # 如果s2小于等于账单总额，且最大时，最小还款额是s2
                if s2 != endBalance :
                    self.label.markFlag(StoriMinimumFlag.MinimumEqualS2)
            else : # 只有s2可能大于账单总额，s1和s3不可能大于账单总额
                if (s1 > MINIMUM_PAYMENT_THRESHOLD and s1 >= s3) :
                    minimumPayment = s1 # 如果s1最大，最小还款额是s1
                    if s1 != endBalance :
                        # 实际上s1不可能大于s3, 公式推导一下即可得出这个结论
                        self.label.markFlag(StoriMinimumFlag.MinimumEqualS1)
                elif (s3 > MINIMUM_PAYMENT_THRESHOLD) :
                    minimumPayment = s3 # 如果s3最大，最小还款额是s3
                    if s3 != endBalance :
                        self.label.markFlag(StoriMinimumFlag.MinimumEqualS3)
                else :
                    minimumPayment = MINIMUM_PAYMENT_THRESHOLD
                    self.label.markFlag(StoriMinimumFlag.MinimumEqualThreshold)
                
                if (s2 > endBalance) :
                    self.label.markFlag(StoriMinimumFlag.MinimumS2LargerThanBalance)

        print("s1: ", s1, "  s2: ", s2,  "  s3: ", s3)

        principalInMinimum = round_to_even(minimumPayment - allButPrincipal)
        # 将最小还款额中prin部分再次分配一下, 可能是本期的交易，也可能是以前的交易
        self.allocPrinInMinimum(principalInMinimum)
        # if (principalInMinimum < 0) :
        #     assert(principalInMinimum >=0)

        if principalInMinimum > 0 :
            self.label.markFlag(StoriMinimumFlag.MinimumHasPRIN)

        self.unpaidMinimum = minimumPayment
        bill.minimumPayment = minimumPayment
        bill.s1 = s1
        bill.s2 = s2
        bill.s3 = s3
        bill.availableLimit = self.cif.availableLimit
        bill.endUnpaidDetail = self.getUnpaidDetail()

        self.graceDayUnpaidMinimum = minimumPayment
        self.dueDayUnpaidMinimum = minimumPayment
        self.dqUnpaidMinimum = minimumPayment

        # if self.cif.checkDQOverLimit() :
        #     assert(bill.minimumPayment == bill.totalPayment)

        print("最小还款额： ", minimumPayment)

        # label
        if (self.cif.balance > 0) :
            self.label.markFlag(StoriStatementFlag.StatementHasEndingBalance)
        elif (self.cif.balance < 0) :
            self.label.markFlag(StoriStatementFlag.StatementHasNegativeEndingBalance)
        else :
            self.label.markFlag(StoriStatementFlag.StatementHasZeroEndingBalance)

        if (historyUnpaidMinimum > 0) :
            bucket = self.cif.getDQDueBucket()
            if (bucket >0) :
                flagName = "StatementDQ" + str(bucket)
                flag = getattr(StoriStatementFlag, flagName, None)  
                self.label.markFlag(flag)
                self.label.markFlag(StoriMinimumFlag.MinimumAccountHasDQ)
            else :
                assert(0)
        
        # if self.lastStatement and self.lastStatement.bill.dueBucket > 0 and self.bill.dueBucket < self.lastStatement.bill.dueBucket :
        #     flagName = "DQReversed" + str(int( self.lastStatement.bill.dueBucket - self.bill.dueBucket))
        #     flag = getattr(StoriDQFlag, flagName, None)  
        #     self.label.markFlag(flag)

        if round_to_even(allButPrincipal) == 0 :
            self.label.markFlag(StoriMinimumFlag.MinimumHasOnlyPRIN)

        if round_to_even(minimumPayment - bill.totalPayment) == 0 :
            self.label.markFlag(StoriMinimumFlag.MinimumEqualBalance)

    def allocPrinInMinimum(self, principalInMinimum) :
        leftPrinAmount = principalInMinimum
        # 先本期
        for tradingType in PRINTradingListType :
            prinTradingList = self.unpaidTradingDic[tradingType]
            for prinTrading in prinTradingList :
                if prinTrading.leftAmount <= 0 :
                    continue
                allocatedAmount = min(prinTrading.leftAmount, leftPrinAmount)
                prinTrading.unpaidInMinimum[self.bill.number] = allocatedAmount
                assert(allocatedAmount<=prinTrading.leftAmount)
                leftPrinAmount = round_to_even(leftPrinAmount - allocatedAmount)
                self.bill.minimumDic[tradingType] = round_to_even(self.bill.minimumDic[tradingType] + allocatedAmount)
                if leftPrinAmount <= 0 :
                    return
        
        # 历史本金
        statement = self.lastStatement
        statementList: List[Statement] = []
        while(statement != None) :
            if (statement.unpaidTotal > 0 and statement.unpaidTotal > statement.unpaidMinimum) :
                statementList.insert(0, statement)
            statement = statement.lastStatement
        
        for statement in statementList :
            for tradingType in PRINTradingListType :
                prinTradingList = statement.unpaidTradingDic[tradingType]
                for prinTrading in prinTradingList :
                    canAllocatedNotInMinimum = prinTrading.leftAmount
                    for number in prinTrading.unpaidInMinimum :
                        canAllocatedNotInMinimum = round_to_even(canAllocatedNotInMinimum-prinTrading.unpaidInMinimum[number])
                    assert(canAllocatedNotInMinimum>=0)
                    if canAllocatedNotInMinimum > 0 :
                        allocatedAmount = min(canAllocatedNotInMinimum, leftPrinAmount)
                        self.bill.minimumDic[tradingType] = round_to_even(self.bill.minimumDic[tradingType] + allocatedAmount)
                        self.unpaidTradingDicOfPreStatement[tradingType].append(prinTrading)
                        prinTrading.unpaidInMinimum[self.bill.number] = allocatedAmount
                        leftPrinAmount = round_to_even(leftPrinAmount - allocatedAmount)
                        if leftPrinAmount <= 0 :
                            return
                        
        if leftPrinAmount > 0 :
            assert(0)