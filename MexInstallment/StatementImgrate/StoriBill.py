from StoriUtils import round_to_even
from typing import List
from StoriTrade import DayBalance, StoriTrade
from StoriConfigs import readUDI, VAT_RATE
from datetime import timedelta


# 账单明细，保存出账时的数据，出账后数据不再变化
class StoriBill:
    def __init__(self, startDate, cycle, number, cif):
        
        # 合约
        self.cif = cif

        # 账期
        self.number = number
        self.startDate = startDate
        self.endDate = cycle["endDay"] #账期结束时间
        self.dueDate = cycle["dueDay"]
        self.graceDate = cycle["graceDay"]
        self.statementDate = cycle["statementDay"]
        self.DQTriggerDay = cycle["DQTriggerDay"]
        self.billingCycle = startDate.strftime("%Y%m%d") + "-" + self.endDate.strftime("%Y%m%d")

        self.availableLimit = 0

        self.billedList: List[StoriTrade] = [] #需要出账的交易列表
        self.balanceList: List[DayBalance] = [] #balance更新列表(按天更新)
        self.adbList: List[DayBalance] = [] #adb更新列表（出账时候计算）

        self.totalPayment = 0.0 #出账时本期账单总还款额
        self.minimumPayment = 0.0   #出账时最小还款额

        self.historyUnpaidMinimum = 0.0 #历史未还最小还款额
        self.s1 = 0
        self.s2 = 0
        self.s3 = 0
        self.minimumDic = {} #出账时最小还款额的快照

        self.originUnpaidDetail = [] # 账期开始时的未还明细（view展示用）
        self.endUnpaidDetail = [] # 账期结束时的未还明细（view展示用）
        self.paymentList = [] #还款分配列表
        self.DQList = [] #记录DQ bucket变化
        self.unallocDetail = {} # 账期结束时未分配的交易明细
        # self.totalUnallocedDetail = {} # 账期结束时，所有未分配的交易明细
        
        # DQ相关
        self.accountDQ = "NON-DQ" #出账时DQ状态
        self.dqDays = 0 #出账时DQ天数
        self.dqBucket = -1 #出账时DQ bucket（按天数计算）
        self.dueBucket = 0 #出账时DQ Due bucket（按账期计算）
        self.dqBlockCode = 0 
        self.dqBlockReason = ""
        
        # 利息计算相关
        self.interestNotTax = 0
        self.totalInterest = 0
        self.vatInterest = 0
        self.adb = 0
        self.UDI = None

        # 滞纳金
        self.lateFee = 0
        self.vatLateFee = 0


        self.previousBalance = 0
        self.newBalance = 0

    def calInt(self) :

        if self.UDI == None :
            UDI = readUDI()
            self.curUDI = round_to_even(UDI[self.endDate], 6)
            self.lasUDI = round_to_even(UDI[self.startDate - timedelta(days=1)], 6)
            self.factor = round_to_even(self.curUDI/self.lasUDI, 6)
            self.inflation = round_to_even(max(0, self.factor - 1), 6)
            self.apr = round_to_even(self.cif.getAPR()/100, 4)
            self.mpr = round_to_even(self.apr/12, 6)
            self.mpr_taxable = round_to_even(self.mpr - self.inflation, 6)
            self.UDI = UDI

            assert(self.mpr >= 0)

        dateNum = len(self.adbList)
        adbSum  = 0
        for i in range(dateNum) :
            adb = max(0, self.adbList[i].endBalance)
            adbSum = round_to_even(adbSum + adb)
        adb = round_to_even(adbSum / dateNum)

        intTaxable = round_to_even(adb * (self.mpr_taxable / 30) * dateNum)
        intNotTaxable = round_to_even(adb * (self.inflation / 30) * dateNum)
        assert(intTaxable >= 0)
        assert(intNotTaxable >= 0)
        
        self.interestNotTax = intNotTaxable
        self.intTaxable = intTaxable
        self.adb = adb
        self.dateNum = dateNum
        self.adbSum = adbSum
        self.vatInterest = round_to_even(intTaxable * VAT_RATE)
        self.totalInterest = round_to_even(intTaxable + intNotTaxable)

    def getEndBalance(self) :
        if self.balanceList :
            return self.balanceList[-1].endBalance
        return round_to_even(self.previousBalance + self.newBalance)
        
    def recordDQ(self, DQBucket) :
        self.DQList.append(DQBucket)

    def addTrading(self, trading :StoriTrade) :
        self.billedList.append(trading)
        trading.billNumber = self.number
        trading.index = len(self.billedList)-1
        
    def recordPayment(self, negativeTrading :StoriTrade, positiveTrading :StoriTrade, payment, isHistory = True, minimumNumber = 0, isOverPayment = False, isOverDQ = False) :
        payment = round_to_even(payment)
        if (payment == 0) :
            return
        if isOverDQ :
            to = "all"
        elif isHistory :
            if minimumNumber > 0 :
                to = "history-minimum-" + str(minimumNumber)
            else :
                to = "history-other-" + str(positiveTrading.billNumber)
        else :
            to = "current-" + "after" if isOverPayment else "before"

        self.paymentList.append({
                        "amount" : payment,
                        "to" : to,
                        "type" : positiveTrading.type,
                        "form-id" : str(negativeTrading.billNumber) + "-" +str(negativeTrading.index),
                        "to-id" : str(positiveTrading.billNumber) + "-" +str(positiveTrading.index),
                        # "effective_time" : str(effective_time.date()),
                        "left" : round_to_even(negativeTrading.leftAmount)
                    })