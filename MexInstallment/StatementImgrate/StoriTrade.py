from datetime import datetime, timedelta
from enum import Enum
from StoriUtils import round_to_even

NewInterestCal = True #是否用新的利息计算方式
APPLY_NEW_Installment_RULES = True #新的分期规则

# 交易状态
class TradingStatus(Enum):  
    PENDING = 1
    POSTED = 2
    REJECTED = 3

# 交易类型
class TradingType(Enum):  
    PAYMENT = 1
    REFUND = 2
    ADJ_NEGATIVE = 3
    
    VAT_INT = 10 # vat_int/adj_vat_int
    VAT_FEE = 11 # vat_fee/adj_vat_fee
    INT = 12 # int/adj_int
    FEE = 13 # fee/open_fee/exchange_fee/adj_fee
    PRIN = 14 # purchase/adj_principal/CASH_ADVANCE/BALANCE_INQUIRY

    INS_VAT_INT = 25
    # INS_VAT_FEE = 26
    INS_INT = 27
    # INS_FEE = 28
    INS_PRIN = 29

    # INS_VAT_FEE_MSI = 35
    # INS_FEE_MSI = 38
    INS_PRIN_MSI = 39

NegativeTypeList = [
    TradingType.PAYMENT,
     TradingType.REFUND,
      TradingType.ADJ_NEGATIVE
]

# 一般情况下，不同交易类型的还款顺序，排在前面的先还
PaymentOrderListOld = [
                    TradingType.INS_VAT_INT, 
                    TradingType.INS_INT, 
                    TradingType.INS_PRIN_MSI,
                    TradingType.INS_PRIN,
                    TradingType.VAT_INT,
                    TradingType.VAT_FEE,
                    TradingType.INT,
                    TradingType.FEE,
                    TradingType.PRIN,
                    ]
PaymentOrderListNew = [
                # TradingType.INS_VAT_FEE_MSI,
                    TradingType.INS_VAT_INT, 
                    TradingType.VAT_INT,
                    TradingType.VAT_FEE,

                    TradingType.INS_INT, 
                    TradingType.INT,

                    # TradingType.INS_FEE_MSI
                    TradingType.FEE,

                    TradingType.INS_PRIN_MSI,
                    TradingType.INS_PRIN,
                    TradingType.PRIN,
                    ]

PaymentOrderList = PaymentOrderListNew if APPLY_NEW_Installment_RULES else PaymentOrderListOld

# 逾期一定程度先还本金
PaymentOrderListFirstPrinOld = [
                    TradingType.INS_PRIN,
                    TradingType.PRIN,
                    TradingType.INS_VAT_INT, 
                    TradingType.VAT_INT,
                    TradingType.VAT_FEE,
                    TradingType.INS_INT, 
                    TradingType.INT,
                    TradingType.FEE,
                    ]

PaymentOrderListFirstPrinNew = [
                    TradingType.INS_PRIN_MSI,
                    TradingType.INS_PRIN,
                    TradingType.PRIN,
                    TradingType.INS_VAT_INT,
                    TradingType.VAT_INT,
                    # TradingType.INS_VAT_FEE_MSI,
                    TradingType.VAT_FEE,
                    TradingType.INS_INT, 
                    TradingType.INT,
                    # TradingType.INS_FEE_MSI
                    TradingType.FEE,
                    ]
PaymentOrderListFirstPrin = PaymentOrderListFirstPrinNew if APPLY_NEW_Installment_RULES else PaymentOrderListFirstPrinOld


ADBTYPEListOld = [
                    TradingType.INS_PRIN,
                    TradingType.PRIN]
ADBTYPEListNew = [TradingType.INS_VAT_INT, 
                    # TradingType.INS_VAT_FEE, 
                    # TradingType.INS_FEE,
                    # TradingType.INS_VAT_FEE_MSI,
                    # TradingType.INS_FEE_MSI
                    TradingType.INS_PRIN_MSI,
                    TradingType.INS_PRIN,
                    TradingType.VAT_INT,
                    TradingType.VAT_FEE,
                    TradingType.FEE,
                    TradingType.PRIN,
                    ]


ADBTYPEList = ADBTYPEListNew if NewInterestCal else ADBTYPEListOld

PRINTradingTypeListOld = [
    TradingType.PRIN
]

PRINTradingTypeListNew = [
    TradingType.INS_PRIN_MSI,
    TradingType.INS_PRIN,
    TradingType.PRIN
]

PRINTradingListType = PRINTradingTypeListNew if APPLY_NEW_Installment_RULES else PRINTradingTypeListOld

def isInstallmentType(tradingType : TradingType) :
    return tradingType.value >= TradingType.INS_VAT_INT.value and tradingType.value <= TradingType.INS_PRIN_MSI.value

def isNegativeType(tradingType: TradingType) :
    return tradingType in NegativeTypeList

def isADBType(tradingType: TradingType) :
    return tradingType in ADBTYPEList

def positiveUnpaidFilter(trading):  
        return trading.isPositiveTrading() and round_to_even(trading.leftAmount) > 0
def unpaidFilter(trading):  
        return round_to_even(trading.leftAmount) > 0

def tradingListSortByTime(tradingList, isByPosingTime=True) :
    sortedList = list(tradingList)
    n = len(sortedList)  
    for i in range(n):  
        swapped = False  
        for j in range(0, n - i - 1):
            posting_time1 = sortedList[j].posting_time
            posting_time2 = sortedList[j + 1].posting_time
            effective_time1 = sortedList[j].effective_time
            effective_time2 = sortedList[j + 1].effective_time
            if (isByPosingTime) :  
                time1 = posting_time1
                time2 = posting_time2
            else :
                time1 = effective_time1
                time2 = effective_time2
            if time1 == time2 and isByPosingTime :
                time1 = effective_time1
                time2 = effective_time2
            if time1 > time2:  
                sortedList[j], sortedList[j + 1] = sortedList[j + 1], sortedList[j]  
                swapped = True  

        if not swapped:  
            break  
    return sortedList

def convertToTradingType(typeStr: str, subType:str) :
    tradingType = getattr(TradingType, typeStr, None)
    if tradingType == None :
        if typeStr == "PAYMENT" :
            tradingType = TradingType.PAYMENT
        elif typeStr == "RE_REFUND" :
            tradingType = TradingType.REFUND
        elif typeStr in ["ADJUSTMENT","ADJ_INS"] :
            tradingType = TradingType.ADJ_NEGATIVE
        elif typeStr == "INS_INT" :
            tradingType = TradingType.INS_INT
        elif typeStr == "INS_VAT" :
            tradingType = TradingType.INS_VAT_INT
        elif typeStr == "INS_PRIN" :
            tradingType = TradingType.INS_PRIN
        elif typeStr.startswith("VAT") :
            if typeStr.endswith("FEE") :
                tradingType = TradingType.VAT_FEE
            else :
                tradingType = TradingType.VAT_INT
        elif typeStr in ["INTEREST","ADJ_INTEREST"]:
            tradingType = TradingType.INT
        elif typeStr.endswith("FEE") or typeStr == "ADJ_FEE":
            tradingType = TradingType.FEE
        elif typeStr in ["PURCHASE","ADJ_PRINCIPAL","BALANCE_INQUIRY", "CASH_ADVANCE"] :
            tradingType = TradingType.PRIN
        elif typeStr.startswith("ADJ_VAT") :
            if "FEE" in subType :
                tradingType = TradingType.VAT_FEE
            elif (subType == "INTEREST") :
                tradingType = TradingType.VAT_INT
    return tradingType

# 交易类
class StoriTrade:  
    def __init__(self, tradingType, amount, tid = 0, effective_time = None,  status = TradingStatus.PENDING, installments = None):
        self.tid = tid # 交易id
        if (effective_time != None) :
            assert(type(effective_time)==datetime)
        self.effective_time = effective_time # 交易时间
        self.type = tradingType # 交易类型
        self.canIns = tradingType == TradingType.PRIN
        self.amount = round_to_even(amount) # 交易金额
        self.status = status #交易状态
        self.leftAmount = self.amount #正向交易leftAmount = 0表示已还 逆向交易leftAmount = 0 表示已分配
        if (status == TradingStatus.POSTED) : # 交易入账时间
            self.posting_time = effective_time
        else :
            self.posting_time = None

        if isNegativeType(tradingType) :
            self.paymentDic = {} #逆向交易分配表
            for key in PaymentOrderList :
                self.paymentDic[key] = 0.0
        self.changedList = [self.amount] # 金额调整路线
        self.changeTid = 0

        self.priorityTid = None # 优先还款交易

        self.installments = installments

        self.billNumber = 0 # 交易关联的账期
        
        self.unpaidInMinimum = {} # 在最小还款中的未还的部分{账期数：未还金额}

        self.index = -1 # 账单中位置
    
    def isPositiveTrading(self) :
        if not self.isNegativeTrading() :
            assert(self.amount >= 0)
            assert(self.leftAmount >= 0)
            return True
        return False

    def isNegativeTrading(self) :
        # print(self.type, self.amount, self.leftAmount)
        if isNegativeType(self.type) :
            assert(self.amount >= 0)
            assert(self.leftAmount >= 0)
            return True
        return False
    
    def change(self, amount, tid) :
        if (self.status == TradingStatus.PENDING) :
            adjustAmount = round_to_even(amount)
            self.amount = round_to_even(self.amount + adjustAmount)
            self.changedList.append(adjustAmount)
            assert(self.amount >= 0)
            self.leftAmount = self.amount
            self.changeTid = tid
            return True
        return False
    
    def reverse(self, amount) :
        if self.status != TradingStatus.PENDING :
            return False
        reverseAmount = -self.changedList[-1]
        if amount != abs(reverseAmount) :
            assert(0)
        self.amount = round_to_even(self.amount + reverseAmount)
        self.leftAmount = self.amount
        if (self.amount == 0) :
            self.status = TradingStatus.REJECTED
        self.changedList.append(reverseAmount)
        return True

    def posting(self, amount, posting_time) :
        assert(posting_time != None)
        assert(type(posting_time)==datetime)
        self.posting_time = posting_time
        self.status = TradingStatus.POSTED
        self.amount = round_to_even(amount)
        self.leftAmount = self.amount

    def isEffectBeforeCycle(self, startDate) :
        effective_date = self.effective_time.date()
        if (effective_date < startDate) :
            return True
        return False
    
    def paymentToPositveTrading(self, positiveTrading) :
        assert(positiveTrading!=None)
        assert(positiveTrading.leftAmount >= 0)
        payment = min(self.leftAmount, positiveTrading.leftAmount)
        positiveTrading.leftAmount = round_to_even(positiveTrading.leftAmount - payment)
        self.leftAmount = round_to_even(self.leftAmount - payment)
        self.paymentDic[positiveTrading.type] = round_to_even(self.paymentDic[positiveTrading.type] + payment)
        return payment

class DayBalance :
    def __init__(self, originBalance, tradingList, date, isADB = False) :
        self.originBalance = originBalance
        self.tradingList = tradingList
        adbDetailList = []

        self.positive = 0
        self.negative = 0
        for trading in tradingList :
            if trading.isPositiveTrading():
                if isADBType(trading.type) or isADB == False:
                    amount = trading.amount
                    self.positive += amount
                    if (amount > 0) :
                        adbDetailList.append((trading.type.name, amount))
            else :
                if isADB == False :
                    self.negative += trading.amount
                    continue
                paymentDic = trading.paymentDic
                for key in paymentDic.keys() :
                    if isADBType(key):
                        amount = round_to_even(paymentDic[key])
                        self.negative += amount
                        if (amount > 0) :
                            adbDetailList.append((key.name, -amount))
                    
        self.adbDetailList = adbDetailList
        self.date = date
        self.endBalance = round_to_even(self.originBalance + self.positive - self.negative)
        print("balance :", date, self.originBalance, round_to_even(self.positive), round_to_even(-self.negative), self.endBalance)

    def genBalanceList(startDate, endDate, originBalance, tradingDic, isADB = False) :
        balanceList = []
        # 计算每天的balance
        curDate = startDate
        while (curDate <= endDate) :
            list = tradingDic[curDate] if curDate in tradingDic else []
            balance = DayBalance(originBalance, list, curDate, isADB)
            balanceList.append(balance)
            curDate = curDate + timedelta(days=1)
            originBalance = balance.endBalance
        return balanceList