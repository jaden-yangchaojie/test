from StoriLabel import StoriLabel, StoriContractFlag
from StoriUtils import round_to_even
from StoriDQ import DQBucketAccordingDays, DQReasonAccordingDays

APPLY_NEW_DQ_RULES = True
APPLY_NEW_Charging_RULES = True

DQ_UPDATE_MAX_DAYS = 360 if APPLY_NEW_DQ_RULES else 180
DQ_UPDATE_MAX_DUEBUCKET = 7

class StoriCif :
    def __init__(self, contractInfo, cardId) :

        # 合约
        self.contractInfo = contractInfo
        self.label = StoriLabel()
        
        self.statementDay = int(self.getUserInfo("statementDay"))
        self.initialCreditLine = int(self.getUserInfo("initialCreditLine"))
        self.apr = float(self.getUserInfo("apr"))
        self.lateFeeMethod = self.getUserInfo("lateFeeMethod")
        self.lateFeeMaxAmount = int(self.getUserInfo("lateFeeMaxAmount"))
        self.cardReplacementFee = int(self.getUserInfo("cardReplacementFee"))
        self.openFee = int(self.getUserInfo("openFee"))

        # 用户状态
        self.DQFirstDueDate = None # 第一个DQ的duedate（DQ天数：当前天数-DQFirstDueDate）
        self.DQFirstStatement = 0 # 第一个DQ的账期（DQ期数：当前期数DQCurStatement-DQFirstStatement）
        self.DQSkipStatementSet = set() # duebucket4之后，bucket只增加不回退，但是中间有还清最小还款的账单，会跳过不增加duebucket
        # self.DQStatementSet = set()
        self.DQDays = 0 # DQ 天数
        self.DQEnabledDate = None # 发送触发DQ通知的date
        self.DQCurStatement = 1 # 当前计算逾期的账期数（dueday之前，期数=上个账期。dueday之后，期数=当前账期）
        self.balance = 0.0 #账户余额
        self.adbBalance = 0.0 #abd
        self.creditLine = round_to_even(self.initialCreditLine/100) #总额度
        self.availableLimit = self.creditLine #可用额度
        
        self.benefits = []

        self.unactivedCardId = cardId # 待激活的卡片ID
        self.activedCardId = None # 激活状态的卡片ID

        # label
        if self.statementDay == 12 :
            self.label.markFlag(StoriContractFlag.ContractCycle12)
        elif self.statementDay == 27 :
            self.label.markFlag(StoriContractFlag.ContractCycle27)
        else :
            assert(0)
        
        if self.openFee > 0 :
            self.label.markFlag(StoriContractFlag.ContractHasOpenFee)
        else :
            self.label.markFlag(StoriContractFlag.ContractHasNoOpenFee)

        if self.cardReplacementFee > 0 :
            self.label.markFlag(StoriContractFlag.ContractHasExchangeCardFee)
        else :
            self.label.markFlag(StoriContractFlag.ContractHasNoExchangeCardFee)

        if self.lateFeeMethod == "tier" :
            self.label.markFlag(StoriContractFlag.ContractLateFeeTire)
        else :
            self.label.markFlag(StoriContractFlag.ContractLateFeeDirect)

        if self.apr < 100 :
            self.label.markFlag(StoriContractFlag.ContractAPRLessThan100)
        else :
            self.label.markFlag(StoriContractFlag.ContractAPRMoreThan100)


    def getUserInfo(self, key) :
        value = self.contractInfo["params"][key]
        return value

    def getOpenFee(self) :
        return self.openFee
    
    def getCardReplacementFee(self) :
        return self.cardReplacementFee
    
    def getLateFeeMaxAmount(self) :
        return self.lateFeeMaxAmount
    
    def getLateFeeMethod(self) :
        return self.lateFeeMethod
    
    def getAPR(self) :
        return self.apr

    def getStatementDay(self) :
        return self.statementDay

    def getInitialCreditLine(self) :
        return self.initialCreditLine

    def updateDQDays(self, curDate) :
        dqDays = 0
        if self.DQFirstDueDate :
            dqDays = max(0, (curDate - self.DQFirstDueDate).days)

        if dqDays > DQ_UPDATE_MAX_DAYS :
            print(f"DQ天数超过{DQ_UPDATE_MAX_DAYS}天不再更新")        
        
        dqDays = min(dqDays, DQ_UPDATE_MAX_DAYS)
        self.DQDays = dqDays

        if (self.DQDays > 0) :
            print("DQ天数：", self.DQDays)
        else :
            print("DQ天数：0")

    def getDQDays(self) :
        return self.DQDays
    
    def getDQBucket(self, DQDays = -1) :
        if DQDays == -1 :
            DQDays = self.DQDays
            
        bucket = DQBucketAccordingDays(DQDays)
        return bucket
    
    def getDQDueBucket(self, DQStatementNumber = 0) :
        if self.DQDays <= 0 :
            return 0
        if self.DQFirstStatement <= 0 :
            return 0
        if DQStatementNumber <= 0 :
            DQStatementNumber = self.DQCurStatement
        dueBucket = max(0, DQStatementNumber - self.DQFirstStatement)
        dueBucket = min(dueBucket, DQ_UPDATE_MAX_DUEBUCKET)
        if dueBucket > 4 :
            dueBucket = min(dueBucket-len(self.DQSkipStatementSet), DQ_UPDATE_MAX_DUEBUCKET)
        assert(dueBucket >= 0)
        return dueBucket
    
    def getBlockCodeList(self) :
        dqDueBucket = self.getDQDueBucket()
        blockCodes = []
        if dqDueBucket > 0 :
            assert(self.getDQBucket() > -1)
            assert(self.getDQDays() > 0)
            blockCodes.append(self.getBlockCode())
            dueBlockCode = self.getDueBlockCode()
            if dqDueBucket < 4 :
                blockCodes.append(dueBlockCode)
            else :
                blockCodes.append("E002")
                blockCodes.append(dueBlockCode)
        return blockCodes
    
    def getBlockCode(self) :
        bucket = DQBucketAccordingDays(self.DQDays)
        code = "D" + str(int(bucket+1)).zfill(3)
        return code
    
    def getDueBlockCode(self) :
        code = "ND" + str(self.getDQDueBucket()).zfill(3)
        return code
    
    def getDueBlockReason(self) :
        code = "DQ bucket " + str(self.getDQDueBucket())
        return code
    
    def getBlockReason(self) :
        reason = DQReasonAccordingDays(self.DQDays)
        return reason
    
    # controls
    def checkReachClosingBucket(self) :
        if self.getDQDueBucket() >=4 :
            return True
        return False

    def checkNotChargeIntAndLateFee(self) :
        if APPLY_NEW_Charging_RULES :
            bucket = 7
        else :
            bucket = 4
        
        if APPLY_NEW_DQ_RULES :
            if self.getDQDueBucket() >= bucket :
                return True
            elif self.getDQDueBucket() >= 4 :
                print("dif case found")
        else :
            if self.getDQBucket() >= bucket :
                return True
        return False
    
    def checkDQ(self) :
        if self.getDQDueBucket() > 0 :
        # if self.DQDays > 0 :
            return True
        return False
    
    def checkCanReverseDQ(self, tradingDate = None, DQStatementNumber = -1) : # 影响DQ回退
        if APPLY_NEW_DQ_RULES :
            if self.getDQDueBucket(DQStatementNumber) < 4 :
                return True
        else :
            days = self.DQDays
            if tradingDate :
                days = (tradingDate - self.DQFirstDueDate).days
            if self.getDQBucket(days) < 4 :
                return True
        return False
    
    def checkExchangeCard(self) :
        if self.getDQDueBucket() > 0 :
            return False
        if self.getDQBucket() >= 0 :
            return False
        return True
    
    def checkTrading(self) :
        if self.getDQBucket() <= 0 :
            return True
        return False
    
    def checkCanInstallment(self) :
        if self.getDQDueBucket() > 0 :
            return False
        if self.getDQBucket() >= 0 :
            return False
        return True
    
    def checkCancelInstallment(self) :
        duebucket = self.getDQDueBucket()
        if duebucket >= 2 :
            return True
        return False
    
    def checkDQOverLimit(self) : # 影响还款方式
        if APPLY_NEW_DQ_RULES :
            if self.getDQDueBucket() >=7 :
                return True
        else :
            if self.getDQBucket() >=5 :
                return True
        return False
    
    def activeCard(self, cardID) :

        self.activedCardId = cardID

    def exchangeCard(self, cardID) :

        self.unactivedCardId = cardID

    def freeIntBenefit(self, benifit_no = None) :
        for benifit in self.benefits :
            if benifit_no != None :
                if benifit_no == benifit["benefit_no"] :
                    return benifit
            else :
                if (benifit["benefitType"] == "INTEREST_COUPON") :
                    return benifit
        return None