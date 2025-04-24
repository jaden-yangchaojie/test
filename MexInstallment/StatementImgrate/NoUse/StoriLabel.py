
from enum import Enum, Flag, IntEnum

class StroiFlag(Enum):
    __autoValue__ = 0
    def __new__(cls, description, *combines):  
        obj = object.__new__(cls)  
        cls.__autoValue__ += 1  
        obj._value_ = cls.__autoValue__
        obj.description = description
        obj.combines = combines
        return obj
    
    def __invert__(self) :
        return ~StroiFlagOp(self)
    
    def __and__(self, other) :
        return StroiFlagOp(self) & StroiFlagOp(other)
    
    def __or__(self, other) :
        return StroiFlagOp(self) | StroiFlagOp(other)

# 运算符(&, |, ~)重载
class StroiFlagOp :
    def __init__(self, op):
        self.op = op

    def __invert__(self) :
        if type(self.op) == StroiFlagOp :
            return ~StroiFlagOp(self.op.op)
        elif type(self.op) == list :
            return StroiFlagOp(tuple(map(lambda x: ~StroiFlagOp(x), self.op)))
        elif type(self.op) == tuple :
            return StroiFlagOp(list(map(lambda x: ~StroiFlagOp(x), self.op)))
        else :
            return StroiFlagOp({self.op : False})
            
    def __and__(self, other) :
        if type(self.op) == tuple :
            if type(other) == StroiFlagOp :
                if type(other.op) == tuple:
                    return StroiFlagOp(self.op + other.op)
                else :
                    other = other.op
            return StroiFlagOp(self.op + (other,))
        else :
            return StroiFlagOp((self.op, other))

    def __or__(self, other) :
        if type(self.op) == list :
            if type(other) == StroiFlagOp :
                if type(other.op) == list:
                    return StroiFlagOp(self.op + other.op)
                else :
                    other = other.op
            op = self.op.copy()
            op.append(other)
            return StroiFlagOp(op)
        else :
            return StroiFlagOp([self.op, other])

class StoriContractFlag(StroiFlag): 
    ContractCycle12 = ( "12出账")
    ContractCycle27 = ( "27出账")
    ContractHasExchangeCardFee = ("合约有换卡费")
    ContractHasNoExchangeCardFee = ("合约没有换卡费")
    ContractHasOpenFee = ("合约有开卡费")
    ContractHasNoOpenFee = ("合约没有开卡费")
    ContractLateFeeDirect = ("滞纳金Direct模式")
    ContractLateFeeTire = ("滞纳金Tire模式")
    ContractAPRLessThan100 = ("apr<100")
    ContractAPRMoreThan100 = ("apr>100")

class StoriStatementFlag(StroiFlag): 
    StatementFirst = ("第一期账单")
    StatementHasEndingBalance = ( "endbalance>0")
    StatementHasNegativeEndingBalance = ( "endbalance<0,有溢缴款")
    StatementHasZeroEndingBalance = ( "endbalance=0")
    StatementHasPendingTrading = ( "有pengding没有入账的交易")
    StatementHasNoTrading = ( "没有交易")
    StatementHasLateFee = ( "本期有滞纳金产生")
    StatementHasINT = ( "本期有利息产生")
    # 出账时checkDQ期数
    StatementDQ1 = ( "账单逾期1") 
    StatementDQ2 = ( "账单逾期2")
    StatementDQ3 = ( "账单逾期3")
    StatementDQ4 = ( "账单逾期4")
    StatementDQ5 = ( "账单逾期5")
    StatementDQ6 = ( "账单逾期6")
    StatementDQ7 = ( "账单逾期7+")
    StatementHasActiveCard = ("账期内有激活卡片")

class StoriDQFlag(StroiFlag): 
    # DQtriggerDay时checkDQ期数更新
    DQTrigger1 = ("DQ1期触发")
    DQTrigger2 = ("DQ2期触发")
    DQTrigger3 = ("DQ3期触发")
    DQTrigger4 = ("DQ4期触发")
    DQTrigger5 = ("DQ5期触发")
    DQTrigger6 = ("DQ6期触发")
    DQTrigger7 = ("DQ7+期触发")

    DQ1CanAuth = ("DQ1期可以Pomelo购买授权") #1-14天
    DQ1CanAppTxn = ("DQ1期可以App购买授权") #1-14天
    DQ1CanNotExchangeCard = ("DQ1期不能换卡")
    DQ1CanAuthAfterReverse = ("DQ回撤后可以Pomelo购买授权")
    DQ1CanAppTxnAfterReverse = ("DQ回撤后可以App购买授权")
    DQ0CanExchangeCardAfterReverse = ("DQ回撤到0可以换卡")
    DQBucket1CannotAuth = ( "bucket1 Pomelo交易授权失败") # 14天+
    DQBucket1CannotAppTxn = ( "bucket1 APP交易授权失败") # 14天+
    DQ4CannotReversed = ( "duebucket4不能回退")
    DQ4CannotReversedCausePaymentNotEnouph = ( "duebucket4不能回退因为金额不够")
    
    DQReversedTrigger = ("发生了DQ回撤")
    # # DQTriggerDay之前回撤
    # DQReversedTo0BeforeDQTrigger = ("TriggerDay之前DQ回撤到0")
    # DQReversedTo1BeforeDQTrigger = ("TriggerDay之前DQ回撤到1")
    # DQReversedTo2BeforeDQTrigger = ("TriggerDay之前DQ回撤到2")
    # DQReversedTo3BeforeDQTrigger = ("TriggerDay之前DQ回撤到3")
    # DQReversedTo4BeforeDQTrigger = ("TriggerDay之前DQ回撤到4+")

    # # DQTriggerDay之后回撤
    # DQReversedTo0AfterDQTrigger = ("TriggerDay之后DQ回撤到0")
    # DQReversedTo1AfterDQTrigger = ("TriggerDay之后DQ回撤到1")
    # DQReversedTo2AfterDQTrigger = ("TriggerDay之后DQ回撤到2")
    # DQReversedTo3AfterDQTrigger = ("TriggerDay之后DQ回撤到3")
    # DQReversedTo4AfterDQTrigger = ("TriggerDay之后DQ回撤到4+")

class StoriPaymentFlag(StroiFlag): 
    PaymentInFullBeforeDueDay = ( "还款日前全额还款")
    PaymentInFullAfterDueDay = ( "还款日后全额还款")
    PaymentInMinimumBeforeDueDay = ( "还款日前最小还款")
    PaymentInMinimumBeforeGraceDay = ( "宽限日前最小还款")
    PaymentInMinimumAfterGraceDay = ( "宽限日后最小还款")
    PaymentNotInFullBeforeDueDay = ( "还款日前没有全额还款")
    PaymentNotInMinimumBeforeGraceDay = ( "宽限日前没有最小还款") # 触发滞纳金
    PaymentNotInMinimumBeforeDueDay = ( "还款日前没有最小还款") # 触发DQ通知
    PaymentOverflowBeforeStatement = ( "出账前有溢缴款") # 还没有生成滞纳金和利息时
    PaymentActiveBeforeDueDay = ("还款日之前有主动还款")
    PaymentReachGraceAmountBeforeDueDay = ( "还款日前还款总额达到了宽限金额")

    # 历史还款分配
    PaymentToHistoryMinimumINS_VAT_INT = ( "还款分配到历史账期分期利息的税")
    PaymentToHistoryMinimumINS_INT = ( "还款分配到历史账期分期利息")
    PaymentToHistoryMinimumINS_PRIN = ( "还款分配到历史账期分期本金")
    PaymentToHistoryMinimumVAT_INT = ( "还款分配到历史账期利息的税")
    PaymentToHistoryMinimumVAT_FEE = ( "还款分配到历史账期费的税")
    PaymentToHistoryMinimumINT = ( "还款分配到历史账期利息")
    PaymentToHistoryMinimumFEE = ( "还款分配到历史账期的费")
    PaymentToHistoryMinimumPRIN = ( "还款分配到历史账期最小还款中的本金")
    PaymentToHistoryMinimumPRINSpecial = ( "还款分配到历史账期最小还款中的本金,本金不在最小还款账期的本金中")
    PaymentToHistoryPRIN = ( "还款分配到历史账期本金")
    PaymentToHistoryINS_PRIN = ("还款分配到历史账期分期本金")
    PaymentToHistoryINS_PRIN_MSI = ("还款分配到历史账期MSI分期本金")
    PaymentToHistoryMinimumINS_PRIN_MSI = ("还款分配到历史账期MSI分期本金")

    # 实时还款分配，向前分配
    PaymentToRealtimeVAT_INT = ( "实时还款分配到利息（调整）的税")
    PaymentToRealtimeVAT_FEE = ( "实时还款分配到费的税")
    PaymentToRealtimeINT = ( "实时还款分配到利息(调整)")
    PaymentToRealtimeFEE = ( "实时还款分配到费")
    PaymentToRealtimePRIN = ( "实时还款分配到本金")
    # 分期在最后一天入账，不存在非溢缴的实时还款分配

    # 溢缴实时还款分配，向后分配
    PaymentOverToRealtimePRIN = ( "溢缴实时还款分配到本金")
    PaymentOverToRealtimeFEE = ( "溢缴实时还款分配到费")
    PaymentOverToRealtimeVAT_FEE = ( "溢缴实时还款分配到费的税")
    PaymentOverToRealtimeINT = ( "溢缴实时还款分配到利息（调整）")
    PaymentOverToRealtimeVAT_INT = ( "溢缴实时还款分配到利息（调整）的税")
    PaymentOverToRealtimeINS_VAT_INT = ( "溢缴实时还款分配到分期利息的税")
    PaymentOverToRealtimeINS_INT = ( "溢缴实时还款分配到分期利息")
    PaymentOverToRealtimeINS_PRIN = ( "溢缴实时还款分配到分期本金")
    PaymentOverToRealtimeINS_PRIN_MSI = ( "溢缴实时还款分配到分期MSI本金")

    # 溢缴分配到本期滞纳金和利息
    PaymentOverToLateFee = ( "溢缴款分配到本期出账的滞纳金")
    PaymentOverToVatLateFee = ( "溢缴款分配到本期出账的滞纳金税")
    PaymentOverToInt = ( "溢缴款分配到本期出账的利息")
    PaymentOverToVatInt = ( "溢缴款分配到本期出账的利息税")

    # bucket 7+ 还款分配
    PaymentToAllPRIN = ( "还款分配到所有账期本金")
    PaymentToAllINS_VAT_INT = ( "还款分配到所有账期分期利息的税")
    PaymentToAllINS_INT = ( "还款分配到所有账期分期利息")
    PaymentToAllINS_PRIN = ( "还款分配到所有账期分期本金")
    PaymentToAllINS_PRIN_MSI = ( "还款分配到所有账期分期MSI本金")
    PaymentToAllVAT_INT = ( "还款分配到所有账期利息的税")
    PaymentToAllVAT_FEE = ( "还款分配到所有账期费的税")
    PaymentToAllINT = ( "还款分配到所有账期利息")
    PaymentToAllFEE = ( "还款分配到所有账期费")

    # 还款状态回撤
    PaymentDQReversed1 = ("一笔交易DQ回撤1期")
    PaymentDQReversed2 = ("一笔交易DQ回撤2期")
    PaymentDQReversed3 = ("一笔交易DQ回撤3期")
    PaymentDQReversed4 = ("一笔交易DQ回撤4期+")
    PaymentReverseInt = ("dueday后入账还款，产生利息撤回")
    PaymentReverseLateFee = ("grace day后入账还款，撤回滞纳金")
    PaymentAllTriggerClosing = ("全额还清，触发销户")


    # bug check
    PaymentReverseIntWhenPMTALL = ("利息撤回时已经全额还款")
    PaymentReverseLateFeeWhenPMTALL = ("滞纳金撤回时已经全额还款")
    PaymentReverseDQ4WhenPMTALL = ("DQ4+撤回时已经全额还款")

class StoriTradingFlag(StroiFlag): 
    TradingHasAppPurchaseAuth = ( "有APP购买交易授权")
    TradingHasPomeloPurchaseAuth =  ( "有Pomelo购买交易授权")
    TradingHasPomeloPaymentAuth = ("有Pomelo还款交易授权")
    TradingHasPomeloRefundAuth =  ( "有Pomelo退款交易授权")
    TradingHasPostedAppPurchase = ( "有入账的APP购买交易")
    TradingHasPostedPomeloPurchase =  ( "有入账的Pomelo购买交易")
    TradingHasPostedPomeloPayment = ( "有Pomelo还款交易")
    TradingHasPostedPomeloRefund =  ( "有入账的Pomelo退款交易")
    TradingHasAppPayment = ("有APP还款交易")
    TradingHasPostedPositive = ("有入账的正向交易")
    TradingHasPostedNegative = ("有入账的逆向交易")
    TradingHasPomeloIncrease =  ( "有Pomelo调增交易")
    TradingHasPomeloDecrease =  ( "有Pomelo调减交易")
    TradingHasUserIncrease =  ( "有商户调增交易")
    TradingHasRefundReversal =  ( "有退款Reversal交易")
    TradingHasPaymentReversal =  ( "有还款Reversal交易")
    TradingHasPurchaseReversal =  ( "有购买Reversal交易")
    TradingHasIncreaseReversal =  ( "有调增Reversal交易")

    TradingHasDecreaseReversal =  ( "有调减Reversal交易")
    TradingReversalPostedFailed = ( "Reversal已经入账的交易失败")
    TradingReversalRejectedFailed = ( "Reversal已经rejected的交易失败")
    TradingIncreasePostedFailed = ( "调增已经入账的交易失败")
    TradingDecreasePostedFailed = ( "调减已经入账的交易失败")
    TradingIncreaseRejectedFailed = ( "调增已经rejected的交易失败")
    TradingDecreaseRejectedFailed = ( "调减已经rejected的交易失败")
    TradingAuthFailedForOverLimit = ( "额度不足授权失败")
    TradingPostingHistoryPositive = ( "跨账期入账正向交易")
    TradingPostingHistoryNegative = ( "跨账期入账逆向交易")
    TradingReversalHistoryPending = ( "跨账期reversal交易")
    TradingPostingOverAuth = ( "交易入账金额>授权金额")
    TradingPostingLessThenAuth = ( "交易入账金额<授权金额")
    TradingOverLimit = ("额度超限占用")

class StoriMinimumFlag(StroiFlag): 
    MinimumAccountHasDQ = ( "账户有逾期")
    MinimumEqualBalanceLessThenThreshold = ( "账单金额<阈值，最小还款额=账单金额")
    MinimumEqualThreshold = ( "账单金额>阈值，s<阈值，最小还款额=阈值")
    MinimumEqualS1 = ( "账单金额>阈值，最小还款额=s1")
    MinimumEqualS2 = ( "账单金额>阈值，最小还款额=s2")
    MinimumEqualS3 = ( "账单金额>阈值，最小还款额=s3")
    MinimumS2LargerThanBalance = ( "s2>账单金额>阈值")
    MinimumHasINS_VAT_INT = ( "最小还款有本期的利息的税")
    MinimumHasINS_INT = ( "最小还款有本期的分期利息")
    MinimumHasINS_PRIN = ( "最小还款有本期的分期本金")
    MinimumHasINS_PRIN_MSI = ( "最小还款有本期MSI的分期本金")
    MinimumHasVAT_INT = ( "最小还款有本期的利息的税")
    MinimumHasVAT_FEE = ( "最小还款有本期的费的税")
    MinimumHasINT = ( "最小还款有本期的利息")
    MinimumHasFEE = ( "最小还款有本期的费")
    MinimumHasPRIN = ( "最小还款有本期的本金")
    MinimumHasHistoryINS_VAT_INT = ( "最小还款有历史的利息的税")
    MinimumHasHistoryINS_INT = ( "最小还款有历史的分期利息")
    MinimumHasHistoryINS_PRIN_MSI = ("最小还款有历史的分期MSI本金")
    MinimumHasHistoryINS_PRIN = ( "最小还款有历史的分期本金")
    MinimumHasHistoryVAT_INT = ( "最小还款有历史的利息的税")
    MinimumHasHistoryVAT_FEE = ( "最小还款有历史的费的税")
    MinimumHasHistoryINT = ( "最小还款有历史的利息")
    MinimumHasHistoryFEE = ( "最小还款有历史的费")
    MinimumHasHistoryPRIN = ( "最小还款有历史的本金")
    MinimumHasOnlyPRIN = ('最小还款中只有本金') #等价于账单中只有本金
    MinimumEqualBalance = ( "最小还款额=账单金额")

class StoriChargingFlag(StroiFlag): 
    ChargingExchangeFee = ("换卡收取了换卡费")
    ChargingNoExchangeFee = ( "换卡没有收取换卡费")
    ChargingDisputeFee = ( "收取争议费")
    ChargingContractLateFee = ("收取合约滞纳金")
    ChargingMinimumLateFee = ("收取最小还款额滞纳金")
    IntADBHasOrigin = ( "初始adb>0")
    IntADBHasNoOrigin = ( "初始adb=0")
    IntADBHasINS_VAT_INT = ( "adb计算中有分期利息税交易")
    IntADBHasINS_INT = ( "adb计算中有分期利息交易")
    IntADBHasINS_PRIN = ( "adb计算中有分期本金交易")
    IntADBHasINS_PRIN_MSI = ("adb计算中有分期MSI本金交易")
    IntADBHasVAT_FEE = ( "adb计算中有费用的税交易")
    IntADBHasVAT_INT = ( "adb计算中有利息的税交易")
    IntADBHasFEE = ( "adb计算中有费用交易")
    IntADBHasPRIN = ( "adb计算中有本金")
    IntADBHasPaymentToINS_VAT_INT = ( "adb中有还款到分期利息税")
    IntADBHasPaymentToINS_INT = ( "adb中有还款到分期利息")
    IntADBHasPaymentToINS_PRIN = ( "adb中有还款到分期本金")
    IntADBHasPaymentToINS_PRIN_MSI = ( "adb中有还款到分期MSI本金")
    IntADBHasPaymentToFEE = ( "adb中有还款到费用")
    IntADBHasPaymentToVAT_FEE = ( "adb中有还款到费用的税")
    IntADBHasPaymentToVAT_INT = ( "adb中有还款到利息的税")
    IntADBHasPaymentToPRIN = ( "adb中有还款到本金")
    IntGraceUnpaidLessThenGraceAmount = ("Dueday未还总额小于GraceAmount")
    IntHasGraced = ("利息被豁免")

class StoriAdjustmentFlag(StroiFlag): 
    AdjustmentPRIN = ( "有本金的税调整")
    AdjustmentFEE = ( "有费用调整")
    AdjustmentINT = ( "有利息调整")
    AdjustmentINS = ( "有分期调整")
    AdjustmentDispute = ( "有争议调整")
    AdjustmentVAT_FEE = ( "有费用的税调整")
    AdjustmentVAT_INT = ( "有利息的税调整")
    AdjustmentNegative = ( "有逆向的调整")

class StoriInstallmentFlag(StroiFlag): 
    InstallmentCreate = ("创建了分期")
    InstallmentDQReject = ("逾期不能办理分期")
    InstallmentCancel = ("逾期终止分期")
    InstallmentOverLimit = ("超限不能分期")
    InstallmentLowerAmount = ("金额太小不能分期")
    InstallmentTradingReversal = ("交易reversal不能分期")
    InstallmentTradingPending = ("交易pending不能分期")
    InstallmentBlockA001 = ("blockA001, 不能分期")
    InstallmentPeriod3 = ("分期3期")
    InstallmentPeriod6 = ("分期6期")
    InstallmentPeriod9 = ("分期9期")
    InstallmentPeriod12 = ("分期12期")
    InstallmentUSDTrading = ("美元币种分期交易")

class StoriFreeIntCouponFlag(StroiFlag): 
    FreeIntCouponBenifit = ( "有免息券活动")
    FreeIntCouponUsed = ( "使用了免息券")
    FreeIntCouponExpired = ( "免息券expired")
    FreeIntCouponCancelled = ( "免息券cancelled")
    FreeIntCouponStartTimeExceed = ( "免息券开始时间超出")
    FreeIntCouponEndTimeExceed = ( "免息券结束时间超出")

# flag取反，原子flag为false的情况
# ~ 表示not
class StoriInvertFlag(StroiFlag): 
    StatementNotFirst = ("不是第一期账单", ~StoriStatementFlag.StatementFirst)
    StatementHasNoINT = ( "账单没有利息", ~StoriStatementFlag.StatementHasINT)
    StatementHasNoLateFee = ( "账单没有滞纳金", ~StoriStatementFlag.StatementHasLateFee)
    StatementHasNoDQ = ("账单没有DQ", ~StoriMinimumFlag.MinimumAccountHasDQ)
    DQNoReversedTrigger = ("没有发生DQ回撤", ~StoriDQFlag.DQReversedTrigger)
    StatementHasOtherPRIN = ("账单除最小还款外，还有其他本金", ~StoriMinimumFlag.MinimumEqualBalance)

# flag组合，2个或这多个原子flag组合，and/or
# & 表示and。所有成员为TRUE，结果为TRUE。空值返回TRUE
# | 表示or。主要有一个为TRUE，结果为TRUE。控制返回FALSE
# ~ 表示not
class StoriCombineFlag(StroiFlag): 
    ContractHasExchangeFeeButNotCharge = ("合约有换卡费，但是免除了", StoriChargingFlag.ChargingNoExchangeFee & StoriContractFlag.ContractHasExchangeCardFee)
    ContractHasNoExchangeFeeSoNotCharge = ("合约没有换卡费，所以没有收取", StoriChargingFlag.ChargingExchangeFee & StoriContractFlag.ContractHasNoExchangeCardFee)
    LateFeeDirectChargeZero = ( "Direct模式没有滞纳金", StoriContractFlag.ContractLateFeeDirect & StoriInvertFlag.StatementHasNoLateFee)
    LateFeeDirectChargeContract = ( "Direct模式有滞纳金", StoriContractFlag.ContractLateFeeDirect & StoriChargingFlag.ChargingContractLateFee)
    LateFeeTireChargeZero = ( "Tire模式没有滞纳金", StoriContractFlag.ContractLateFeeTire & StoriInvertFlag.StatementHasNoLateFee)
    LateFeeTireChargeContract = ( "Tire模式收取合约滞纳金", StoriContractFlag.ContractLateFeeTire & StoriChargingFlag.ChargingContractLateFee)
    LateFeeTireChargeMinimum = ( "Tire模式收取最小还款额滞纳金", StoriContractFlag.ContractLateFeeTire & StoriChargingFlag.ChargingMinimumLateFee)
    StatementNotFirstAndHasNoInt = ("非第一期账单，没有利息", StoriInvertFlag.StatementNotFirst & ~StoriStatementFlag.StatementHasINT)
    StatementNotFirstAndHasNoLateFee = ("非第一期账单，没有滞纳金", StoriInvertFlag.StatementNotFirst & ~StoriStatementFlag.StatementHasLateFee)
    StatementNotFirstAndHasNoDQ = ("非第一期账单，没有DQ", StoriInvertFlag.StatementNotFirst & ~StoriMinimumFlag.MinimumAccountHasDQ)
    StatementHasINTAndLateFee = ( "账单有利息，有滞纳金", StoriStatementFlag.StatementHasINT & StoriStatementFlag.StatementHasLateFee)
    StatementHasINTButNoLateFee = (  "账单有利息，没有滞纳金", StoriStatementFlag.StatementHasINT & StoriInvertFlag.StatementHasNoLateFee)
    StatementHasNoINTButLateFee = ( "账单没有利息，有滞纳金", StoriInvertFlag.StatementHasNoINT & StoriStatementFlag.StatementHasLateFee)
    StatementHasNoINTAndNoLateFee = ( "账单没有利息，没有滞纳金", StoriInvertFlag.StatementHasNoINT & StoriInvertFlag.StatementHasNoLateFee)
    StatementHasNoUnpaid = ( "账单没有欠款", StoriStatementFlag.StatementHasNegativeEndingBalance | StoriStatementFlag.StatementHasZeroEndingBalance)
    StatementUseCounponToFreeInt = ( "使用免息券免除了利息", StoriInvertFlag.StatementHasNoINT & StoriFreeIntCouponFlag.FreeIntCouponUsed & StoriPaymentFlag.PaymentNotInFullBeforeDueDay)
    StatementHasBilled = ( "账单已经出账", StoriStatementFlag.StatementHasEndingBalance | StoriStatementFlag.StatementHasNegativeEndingBalance | StoriStatementFlag.StatementHasZeroEndingBalance)
    StatementHasDQAndNoReversal = ( "账单DQ且账期内没有DQ回撤", StoriMinimumFlag.MinimumAccountHasDQ & StoriInvertFlag.DQNoReversedTrigger)
    StatementDQ4PaymentNotInFull = ( "账单逾期4期以上没有全额还款", StoriStatementFlag.StatementDQ4 & StoriPaymentFlag.PaymentNotInFullBeforeDueDay)
    StatementDQ4PaymentNotInMinimum = ( "账单逾期4期以上没有最小还款", StoriStatementFlag.StatementDQ4 & StoriPaymentFlag.PaymentNotInMinimumBeforeGraceDay)
    StatementDQMoreThenOne = ( "账单逾期超过1期", StoriMinimumFlag.MinimumAccountHasDQ & ~StoriStatementFlag.StatementDQ1)

    PaymentInFull = ("历史账单全额还款", StoriPaymentFlag.PaymentInFullBeforeDueDay | StoriPaymentFlag.PaymentInFullAfterDueDay )
    PaymentOverToLateFeeBeforeVatLateFee = ("溢缴款还款先还LateFee，再还VatLateFee", StoriPaymentFlag.PaymentOverToLateFee & (~StoriPaymentFlag.PaymentOverToVatLateFee | ~StoriMinimumFlag.MinimumHasFEE & StoriMinimumFlag.MinimumHasVAT_FEE))
    PaymentOverToIntBeforeVatInt = ("溢缴款还款先还LateFee，再还VatLateFee", StoriPaymentFlag.PaymentOverToVatLateFee & (~StoriPaymentFlag.PaymentOverToInt | ~StoriMinimumFlag.MinimumHasVAT_FEE & StoriMinimumFlag.MinimumHasINT))
    PaymentOverToVatLateFeeBeforeInt = ("溢缴款还款先还INT，再还VAT_INT", StoriPaymentFlag.PaymentOverToInt & (~StoriPaymentFlag.PaymentOverToVatInt | ~StoriMinimumFlag.MinimumHasINT & StoriMinimumFlag.MinimumHasVAT_INT))
    DQJumpReversed = ("DQ跨级回撤", StoriPaymentFlag.PaymentDQReversed2 | StoriPaymentFlag.PaymentDQReversed3 | StoriPaymentFlag.PaymentDQReversed4)
    TradingHasFEE = ("有费用交易",  StoriStatementFlag.StatementFirst & StoriContractFlag.ContractHasOpenFee | StoriChargingFlag.ChargingExchangeFee | StoriAdjustmentFlag.AdjustmentFEE | StoriStatementFlag.StatementHasLateFee)
    TradingHasINT = ("有利息交易", StoriAdjustmentFlag.AdjustmentINT | StoriStatementFlag.StatementHasINT)
    StatementHasExchangeCard = ("账期内有换卡", StoriChargingFlag.ChargingNoExchangeFee | StoriChargingFlag.ChargingExchangeFee)
    IntNoGracedForNotCoverMinimumBeforeDueDay = ("利息没有被豁免，因为dueday前没有最小还款", ~StoriPaymentFlag.PaymentInMinimumBeforeDueDay & StoriStatementFlag.StatementHasINT & ~StoriChargingFlag.IntHasGraced & StoriPaymentFlag.PaymentReachGraceAmountBeforeDueDay & StoriPaymentFlag.PaymentActiveBeforeDueDay)
    IntNoGracedForNotPaymentBeforeDueDay = ("利息没有被豁免，因为dueday前没有主动还款", StoriPaymentFlag.PaymentInMinimumBeforeDueDay & StoriStatementFlag.StatementHasINT & ~StoriChargingFlag.IntHasGraced & StoriPaymentFlag.PaymentReachGraceAmountBeforeDueDay & ~StoriPaymentFlag.PaymentActiveBeforeDueDay)

    # TradingHasVAT = ("有税", TradingHasFEE | TradingHasINT)

# flag联合模式，由StoriCombineFlag组成，或者多个账期组成
class StoriUnionFlag(StroiFlag): 
    StatementNoHistoryBill = ( "历史账单全部还完", StoriInvertFlag.StatementNotFirst, StoriCombineFlag.StatementHasNoUnpaid)
    StatementHasOneUnpaidMinimum = ( "只有一期历史未还最小还款", StoriInvertFlag.StatementNotFirst, StoriStatementFlag.StatementDQ1)
    StatementHasMulitUnpaidMinimum = ( "有多期历史最小还款未还", StoriInvertFlag.StatementNotFirst, StoriCombineFlag.StatementDQMoreThenOne)
    StatementLastHasIntCurHasNo = ( "上期账单有利息，本期没有", StoriInvertFlag.StatementHasNoINT, StoriStatementFlag.StatementHasINT)
    StatementSpecailTest = ( "上期账单有滞纳金或利息，本期账单没有交易和滞纳金，有利息", StoriCombineFlag.StatementHasINTButNoLateFee & StoriStatementFlag.StatementHasNoTrading , StoriStatementFlag.StatementHasINT | StoriStatementFlag.StatementHasLateFee)

# 需要手动mark的原子flag
AtomEnums = [
            StoriStatementFlag,
            StoriDQFlag, 
                StoriPaymentFlag, 
                StoriChargingFlag,
                StoriTradingFlag,  
                StoriMinimumFlag,
                StoriAdjustmentFlag,
                StoriFreeIntCouponFlag,
                StoriInstallmentFlag]

# 自动生成的组合flag
AutoEnums = [StoriInvertFlag,
            StoriCombineFlag, 
                StoriUnionFlag]

    
class StoriLabel:
    def __init__(self, lastLabel = None, cifLabel = None):

        if cifLabel == None :
            self.flagDic = {StoriContractFlag : [False] * len(StoriContractFlag.__members__)}
            self.autoFlagDic = {}
        else :
            # 为每个flag分配内存空间
            flagDic = {}
            for flag in AtomEnums :
                flagDic[flag] = [False] * len(flag.__members__)
            self.flagDic = flagDic

            # 为每个autoflag分配内存空间
            flagDic = {}
            for flag in AutoEnums :
                flagDic[flag] =  [False] * len(flag.__members__)
            self.autoFlagDic = flagDic

            self.lastLabel = lastLabel
            self.cifLabel = cifLabel

    # 查看flag标记是否为True
    def getMarkedFlag(self, flag) -> bool:
        flagType = type(flag)
        for flagDic in [self.flagDic, self.autoFlagDic] :
            if (flagType in flagDic) :
                flags = flagDic[flagType]
                return flags[flag.value-1]            
        assert(0)
        return False
    
    # 将flag标记为True
    def markFlag(self, flag) :
        flagType = type(flag)
        if (flagType in self.flagDic) :
            flags = self.flagDic[flagType]
            flags[flag.value-1] = True
        elif (flagType in self.autoFlagDic) :
            flags = self.autoFlagDic[flagType]
            flags[flag.value-1] = True
        else :
            assert(0)
    
    # 将flag标记为False
    def unmarkFlag(self, flag) :
        flagType = type(flag)
        if (flagType in self.flagDic) :
            flags = self.flagDic[flagType]
            flags[flag.value-1] = False

    # 自动标记组合flag
    def autoMarkUnions(self) :
        for flag in self.autoFlagDic :
            for name, member in flag.__members__.items():
                combines:list = member.combines
                if len(combines) == 0 :
                    continue
                cal = self.calCombines(combines)
                if cal:    
                    self.markFlag(member)
    
    # 计算组合标记
    def calCombines(self, combines) -> bool:
        if len(combines) == 0 :
            return False
        label = self
        cal = True

        for comb in combines :
            # if type(comb) == tuple and len(comb) == 2 and type(comb[1]) == int :
            #     num = comb[1]
            #     for i in range(num) :
            #         if (label == None) :
            #             return False
            #         cal = cal and label.calUnionFlag(comb[0])
            #         label = label.lastLabel
            #     continue
            if (label == None) :
                return False
            cal = cal and label.calUnionFlag(comb)
            label = label.lastLabel
        return cal
    
    # 计算组合标记的递归函数
    def calUnionFlag(self, unionflag) -> bool:
        if type(unionflag) == StroiFlagOp :
            op = unionflag.op
            flag = self.calUnionFlag(op)
        elif (type(unionflag) == list) :
            flag = any(map(lambda x: self.calUnionFlag(x), unionflag))
        elif (type(unionflag) == tuple) :
            flag = all(map(lambda x: self.calUnionFlag(x), unionflag))
        else :
            if type(unionflag) == dict :
                flagObj = list(unionflag.keys())[0]
                b = unionflag[flagObj]
                value = flagObj.value
                flagType = type(flagObj)
                unionflag = flagObj
            else :
                flagType = type(unionflag)
                value = unionflag.value
                b = True
            if (len(unionflag.combines) == 0) :
                if flagType == StoriContractFlag :
                    flag = self.cifLabel.flagDic[flagType][value-1]
                else :
                    flag = self.flagDic[flagType][value-1]
            else :
                flag = self.getMarkedFlag(unionflag)
            if b == False :
                flag = not flag
        return flag
    
    # 获取所有的标记
    # dict{"name":"flag"}
    def getLabelDict(self) -> dict:
        labelDic = {}
        for flagDic in [self.flagDic, self.autoFlagDic] : 
            for flag, flagList in flagDic.items():
                for name, member in flag.__members__.items():
                    labelDic[member] = flagList[member.value-1]
        return labelDic
    
    # 获取命中的标签
    def getAtomTrueDescriptions(self) -> list:
        flagDic = self.flagDic
        descriptions = {}
        for flag, flagList in flagDic.items():
            trueList = []
            for name, member in flag.__members__.items():
                if flagList[member.value-1] == True :
                    trueList.append(member.description)
            if len(trueList) > 0 :
                descriptions[flag.__name__] = trueList
            else :
                descriptions[flag.__name__] = ""
        return descriptions
    
    def getLabelFlags() -> dict:
        atomEnum = AtomEnums.copy()
        atomEnum.insert(0, StoriContractFlag)
        combineEnum = [StoriInvertFlag ,StoriCombineFlag, StoriUnionFlag]
        flags = {"Atom Label":atomEnum, "Combine Label":combineEnum}
        return flags
        