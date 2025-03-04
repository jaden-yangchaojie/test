from StoriUtils import round_to_even, calculate_monthly_payment
from StoriConfigs import VAT_RATE, InstallmentAprDic
from StoriTrade import StoriTrade, TradingStatus, TradingType

class Installment:
    def __init__(self, periods, principal, tid=0, insId = 0, msi = False):
        self.data = {}
        self.tid = tid
        self.insId = insId
        self.periods = periods
        self.principal = principal
        self.apr = 0 if msi else InstallmentAprDic[self.periods]
        self.mpr = round_to_even(self.apr/12, 6)
        self.formattedMpr = str(round_to_even(self.mpr * 100, 2)).rstrip('0').rstrip('.')+"%"
        self.monthlyAmount = calculate_monthly_payment(self.principal, self.mpr, self.periods, msi=msi)
        
        self.totalAmount = 0
        self.totalInterest = 0
        self.totalVat = 0

        self.vatList = []
        self.intList = []
        self.principalList = []
        
        self.curPeriods = 0
        self.tradingList = []

        self.cancelled = False

        self.msi = msi

        print("分期试算")
        print("期数：",periods)
        print("本金(*100):",principal)
        leftPricipal = principal
        for i in range(periods) :
            if (i == periods -1) :
                curPrincipal = round_to_even(leftPricipal, 0)
                curInt = round_to_even(self.monthlyAmount - curPrincipal, 0)
            else :
                curInt = round_to_even(leftPricipal * self.mpr, 0)
                curPrincipal = round_to_even(self.monthlyAmount - curInt, 0)
            curVat = round_to_even(curInt * VAT_RATE, 0)
            self.principalList.append(curPrincipal)
            self.intList.append(curInt)
            self.vatList.append(curVat)
            
            self.totalInterest += curInt
            self.totalVat += curVat
            self.totalAmount += curPrincipal + curInt + curVat
            leftPricipal = leftPricipal - curPrincipal
            print(curPrincipal, curInt, curVat)

        print(self.totalAmount, self.totalInterest, self.totalVat)

    def getCurInstallmentTrading(self) :
        if self.curPeriods >= self.periods :
            return None
        if self.cancelled :
            return None
        self.getTradingList()
        curInstallmentTrading = self.tradingList[self.curPeriods]
        return curInstallmentTrading
    
    def getTradingList(self) :
        if (len(self.tradingList) == 0) :
            for i in range(self.periods) :
                if self.msi :
                    principalTrade = StoriTrade(TradingType.INS_PRIN_MSI, self.principalList[i]/100)
                    self.tradingList.append([principalTrade])
                else :
                    principalTrade = StoriTrade(TradingType.INS_PRIN, self.principalList[i]/100)
                    vatTrade = StoriTrade(TradingType.INS_VAT_INT, self.vatList[i]/100)
                    intTrade = StoriTrade(TradingType.INS_INT, self.intList[i]/100)
                    self.tradingList.append([principalTrade, vatTrade, intTrade])
        return self.tradingList

    def getLeftTradings(self) -> list:
        if self.cancelled == True :
            return 0
        leftTradings = []
        self.getTradingList()
        for i in range(self.periods) :
            if (i < self.curPeriods) :
                continue
            tradingList = self.tradingList[i]
            leftTradings.extend(tradingList)
        return leftTradings
    
    def cancel(self) :
        self.cancelled = True
    
    def posting(self) :
        self.curPeriods += 1

    def consultPeroid(principal, period) :
        ins = Installment(period, principal)
        return ins

    def consult(principal) :
        periodList = [3, 6, 9, 12]
        insList = []
        for period in periodList :
            ins = Installment.consultPeroid(principal, period)
            data = {}
            # data["currencyCode"] = "MXN"
            # data["referenceType"] = "order"
            data["periods"] = ins.periods
            # data["couponId"] = ""
            data["principal"] = ins.principal
            # data["totalVat"] = ins.totalVat
            # data["originTotalVat"] = ins.totalVat
            # data["originTotalAmount"] = ins.totalAmount
            # data["monthlyAmount"] = ins.monthlyAmount
            # data["originMonthlyAmount"] = ins.monthlyAmount
            # data["totalInterest"] = ins.totalInterest
            # data["originTotalInterest"] = ins.totalInterest
            # data["apr"] = ins.apr
            # data["originApr"] = ins.apr
            # data["mpr"] = ins.mpr
            # data["originMpr"] = ins.mpr
            # data["formattedMpr"] = ins.formattedMpr
            # data["formattedOriginMpr"] = ins.formattedMpr
            # data["totalAmount"] = ins.totalAmount
            ins.data = data
            insList.append(ins)
        return insList
            