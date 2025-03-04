# import pandas as pd
# # from IPython.display import clear_output, display, HTML
# from StoriTrade import isADBType
# from StoriLabel import StoriLabel
# # from styleframe import StyleFrame, Styler, utils
# from typing import List
# from StoriUser import StoriUser
# from StoriStatement import Statement
#
# def is_all_zero(series):
#     return (series == 0).all()
#
# def highlight_adb(s):
#     return ['background-color: lightblue' if isADBType(s.type) else '' for v in s]
#
# def highlight_date(s):
#     return ['background-color: lightblue' for _ in s]
#
#
# class StoriView :
#     def __init__(self, user:StoriUser):
#         self.user:StoriUser = user
#         # self.statement:Statement = statement
#         self.statementList = user.statementList
#         # statementList = []
#         # stam = statement
#         # while (stam != None) :
#         #     statementList.insert(0, stam)
#         #     stam = stam.lastStatement
#         # self.statementList : List[Statement] = statementList
#         pd.set_option('display.max_columns', None)  # 显示所有列
#         pd.set_option('display.max_colwidth', None) #
#         pd.set_option('display.max_rows', None)  #
#
#         self.labels = None
#         self.trueDescrips = None
#         self.cifTrueDescrips = None
#
#     def displayTitle(self, title) :
#         html_content = f'<br><b><p style="color:gray;">{title}</p></b>'
#         display(HTML(html_content))
#
#     def displayStatementDetail(self, cycle) :
#         # 打印账期1
#         self.displayTitle("账期")
#         statementCycle = self.getCycle(cycle)
#         display(statementCycle)
#
#         self.displayTitle("交易列表")
#
#         # 交易列表
#         tradingList = self.getTradingList(cycle)
#         display(tradingList)
#
#         self.displayTitle("每日余额")
#
#         # 打印balance
#         balanceList = self.getBalanceList(cycle)
#         display(balanceList)
#
#         self.displayTitle("每日adb余额")
#
#         # 打印adb
#         adbList = self.getADBList(cycle)
#         display(adbList)
#
#         self.displayTitle("账单")
#
#         # 账单数据
#         bill = self.getBill(cycle)
#         display(bill)
#
#         self.displayTitle("未还明细")
#
#         unpaidDetail = self.getUnpaidDetail(cycle)
#         display(unpaidDetail)
#
#         paymentList = self.getPaymentList(cycle)
#         if type(paymentList) == pd.DataFrame :
#             self.displayTitle("还款分配明细")
#             styledPaymentList = paymentList.style.apply(highlight_adb, axis=1)
#             display(styledPaymentList)
#         # with pd.ExcelWriter('output.xlsx') as writer:
#             # paymentList.to_excel(writer, sheet_name='Sheet1', startrow=0, startcol=0)
#         #     tradingList.to_excel(writer, sheet_name='Sheet1', startrow=statementCycle.shape[0] + 1, startcol=0)
#
#         intDetail = self.getIntDetail(cycle)
#         if type(intDetail) == pd.DataFrame :
#             self.displayTitle("利息计算")
#             display(intDetail)
#
#     def getDescription(self) -> str:
#         totalNumber = len(self.statementList)
#         description = ""
#         # self.getTrueDescrips()
#
#         for statement in self.statementList :
#             billDesp = f"-----第{statement.bill.number}期-----\n"
#             if (statement.isBilled) :
#                 endBalance = statement.bill.getEndBalance()
#                 availableLimit = statement.cif.availableLimit
#                 accountDQ = statement.bill.accountDQ
#                 interest = statement.bill.totalInterest
#                 lateFee = statement.bill.lateFee
#                 overPayment = statement.overTrading.amount if statement.overTrading else 0
#
#                 billDesp += f"账户余额：{endBalance}, 可用额度：{availableLimit}\n"
#                 billDesp += f"DQ状态：{accountDQ}\n"
#                 if (interest > 0) :
#                     billDesp += f"利息：金额{interest}, DueDay后未还总额:{statement.dueDayUnpaidTotal}\n"
#                 if (lateFee > 0) :
#                     billDesp += f"滞纳金：金额{lateFee}, DueDay后未还总额:{statement.graceDayUnpaidMinimum}\n"
#                 if (overPayment > 0) :
#                     billDesp += f"溢缴款：金额{overPayment}\n"
#                 description += billDesp
#             else :
#                 billDesp += "未出账\n"
#                 description += billDesp
#             # trueDescript:dict = self.trueDescrips[statement.bill.number -1]
#             # trueDescriptList = []
#             # for value in trueDescript.values() :
#             #     trueDescriptList.extend(value)
#             # description += f"标签：\n{trueDescriptList}"
#
#         description = f"共{totalNumber}期\n{description}"
#         return description
#
#     def getStatement(self, number) -> Statement:
#         if (number < 1 or number > len(self.statementList)) :
#             print("账期不存在")
#             return None
#         return self.statementList[number-1]
#
#     def getViewStatements(self, number = 0):
#         if (number == 0) :
#             statementList = self.statementList
#         else :
#             statement = self.getStatement(number)
#             if (statement == None) :
#                 return []
#             statementList = [statement]
#         return statementList
#
#     # 获取每个账期的标签
#     def getAllLabels(self) -> list:
#         if (self.labels == None) :
#             statementList = self.getViewStatements(0)
#             labels = []
#             for statement in statementList :
#                 label = statement.label
#                 labelDict = label.getLabelDict()
#                 labels.append(labelDict)
#             self.labels = labels
#         return self.labels
#
#     def getCifLabelDF(self) -> dict:
#         label = self.user.cif.label
#         labelDict = label.getLabelDict()
#         return pd.Series(labelDict)
#
#     def getTrueDescrips(self) :
#         if self.trueDescrips == None :
#             statementList = self.getViewStatements(0)
#             descriptions = []
#             for statement in statementList :
#                 label = statement.label
#                 descriptions.append(label.getAtomTrueDescriptions())
#             self.trueDescrips = descriptions
#         return self.trueDescrips
#
#     def getCifTrueDescrips(self) :
#         if self.cifTrueDescrips == None :
#             label = self.user.cif.label
#             cifTrueDescrips = label.getAtomTrueDescriptions()
#             self.cifTrueDescrips = cifTrueDescrips
#         return self.cifTrueDescrips
#
#     def getCasesMeetLabel(self, *expectedLabelList) :
#         statementList = self.getViewStatements(0)
#         meetList = []
#         for statement in statementList :
#             cal = statement.label.calCombines(expectedLabelList)
#             if cal :
#                 meetList.append(str(statement.bill.number))
#         return meetList
#
#     # 获取账期
#     def getCycle(self, number) :
#         statement = self.getStatement(number)
#         if (statement == None) :
#             return
#         bills = [statement.bill]
#         if number > 1 :
#             lastStatement = self.getStatement(number-1)
#             if lastStatement != None :
#                 bills.insert(0, lastStatement.bill)
#
#         cycles = []
#         indexes = []
#         for bill in bills :
#             cycleDict = {
#                 'startDate': bill.startDate,
#                 'endDate': bill.endDate,
#                 'statementDate': bill.statementDate,
#                 'dueDate' : bill.dueDate,
#                 'DQTriggerDay' : bill.DQTriggerDay,
#                 'graceDate' : bill.graceDate,
#             }
#             cycles.append(cycleDict)
#             if bill == statement.bill :
#                 indexes.append("本期")
#             else :
#                 indexes.append("上期")
#         df = pd.DataFrame(cycles)
#         # df.columns.names= ["cycle"]
#         df.index = indexes
#         # styled_df = df.style.apply(highlight_date, subset=['dueDate'])
#
#         sf = StyleFrame(df)
#         # sf.apply_column_style(styler_obj=Styler(bg_color='yellow', bold=True), cols_to_style=['dueDate'])
#
#         return df
#
#     # 获取交易列表
#     def getTradingList(self, number) :
#         statement = self.getStatement(number)
#         if (statement == None) :
#             return
#         bill = statement.bill
#         tradingList = []
#         for trading in bill.billedList :
#             # tradingDic = {}
#             tradingDic = { "type": trading.type,
#                            "amount":trading.amount,
#                              "effective_time":trading.effective_time.date(),
#                                "posting_time":trading.posting_time.date()}
#
#             tradingList.append(tradingDic)
#         df = pd.DataFrame(tradingList)
#         # df.columns.names= ["交易列表"]
#         return df
#
#     # 获取balance
#     def getBalanceList(self, number, isADB = False) :
#         statement = self.getStatement(number)
#         if (statement == None) :
#             return
#
#         bill = statement.bill
#         balanceList = bill.balanceList
#         if (isADB) :
#             balanceList = bill.adbList
#         dateDesc = {bill.startDate:"Start Day", bill.endDate:"End Day"}
#         if statement.lastStatement != None : # and isADB == False :
#             lastBill = statement.lastStatement.bill
#             dateDesc[lastBill.dueDate] = "Due Day"
#             dateDesc[lastBill.graceDate] = "Grace Day"
#             dateDesc[lastBill.DQTriggerDay] = "DQ Trigger Day"
#         dfList = []
#         for balance in balanceList :
#             date = balance.date
#             originBalance = balance.originBalance
#             endBalance = balance.endBalance
#             # if len(balance.tradingList) == 0 and (date in datesList) == False  :
#             #     continue
#             if (isADB) :
#                 amountList = list(map(lambda x:x[0] + ":" +  str(x[1]), balance.adbDetailList))
#             else :
#                 amountList = list(map(lambda x:x.amount if x.isPositiveTrading() else -x.amount, balance.tradingList))
#             dfList.append({
#                         'Desc': dateDesc[date] if date in dateDesc else "",
#                         'Date': date,
#                         'Initial Balance': originBalance,
#                         'Ending Balance': endBalance,
#                         'Positive' : balance.positive,
#                         'Negative' : -balance.negative,
#                         'tradingList' : amountList
#             })
#         df = pd.DataFrame(dfList)
#         # df.columns.names= ["adb" if isADB else "balance"]
#         return df
#
#     # 获取adb列表
#     def getADBList(self, number) :
#         return self.getBalanceList(number, isADB=True)
#
#     # 获取账单
#     def getBill(self, number) :
#         statement = self.getStatement(number)
#         if (statement == None) :
#             return
#         if (not statement.isBilled) :
#             return
#         bill = statement.bill
#         billDict = {
#             "balance" : bill.getEndBalance(),
#             "credit line" : bill.cif.creditLine,
#             "available credit" : bill.availableLimit,
#             "total payment" : [bill.totalPayment],
#             "minimum payment" : bill.minimumPayment,
#             "int" : bill.totalInterest,
#             "vat_int" : bill.vatInterest,
#             "latefee" : bill.lateFee,
#             "vat_latefee" : bill.vatLateFee,
#         }
#         df = pd.DataFrame(billDict)
#         # df.columns.names= ["账单"]
#         return df
#
#     # 获取还款分配
#     def getPaymentList(self, number) :
#         statement = self.getStatement(number)
#         if (statement == None) :
#             return
#         bill = statement.bill
#         if len(bill.paymentList) == 0 :
#             return
#         df = pd.DataFrame(bill.paymentList)
#         # df = pd.DataFrame(bill.paymentList).sort_values('effective_time')
#         # df.columns.names= ["还款分配明细"]
#         return df
#
#     def getDQInfo(self, number) :
#         if (number < 2) :
#             return
#         statement = self.getStatement(number)
#         if (statement == None) :
#             return
#         if statement.bill.accountDQ == "NON-DQ" :
#             return
#
#         detailDic = {}
#         unpaid = statement.bill.historyUnpaidMinimum
#         minimumPayment = statement.bill.minimumPayment
#         detailDic["minimum Payment for last statement"] = minimumPayment
#         detailDic["unpaid minimum Payment for previous statement"] = unpaid
#         detailDic["DQ Status"] = statement.bill.accountDQ
#         detailDic["DQ Days till statement day"] = statement.bill.dqDays
#         detailDic["DQ bucket"] = statement.bill.dqBucket
#         detailDic["DQ Block code"] = statement.bill.dqBlockCode
#         detailDic["DQ due bucket"] = statement.bill.dueBucket
#         # detailDic["DQ Block reason"] = statement.bill.dqBlockReason
#
#         dataList = detailDic.values()
#         index = detailDic.keys()
#
#         df = pd.DataFrame(dataList, index=index)
#         return df
#
#     def getMinimumPayment(self, number) :
#         if (number < 1) :
#             return
#         statement = self.getStatement(number)
#         if (statement == None) :
#             return
#
#         detailDic = {k: v for k, v in statement.bill.minimumDic.items() if v != 0}
#
#         unpaid = statement.bill.historyUnpaidMinimum
#         minimumPayment = statement.bill.minimumPayment
#         detailDic["ending balance"] = statement.bill.getEndBalance()
#         detailDic["minimumPayment for previous cycle"] = minimumPayment
#         detailDic["total negative transactions during cycle"] = minimumPayment - unpaid
#         detailDic["history Unpaid Minimum"] = unpaid
#         detailDic["s1"] = statement.bill.s1
#         detailDic["s2"] = statement.bill.s2
#         detailDic["s3"] = statement.bill.s3
#         detailDic["minimumPayment"] = statement.bill.minimumPayment
#
#         dataList = detailDic.values()
#         index = detailDic.keys()
#
#         df = pd.DataFrame(dataList, index=index)
#
#         return df
#
#
#     def getLateFeeDetail(self, number) :
#         if (number < 2) :
#             return
#         statement = self.getStatement(number)
#         if (statement == None) :
#             return
#         if statement.bill.lateFee <= 0 :
#             return
#
#         detailDic = {}
#         unpaid = statement.graceDayUnpaidMinimum
#         minimumPayment = statement.lastStatement.bill.minimumPayment
#         method = statement.cif.getLateFeeMethod()
#         detailDic["Late Fee Type"] = method
#         detailDic["Late Fee Amount"] = statement.cif.getLateFeeMaxAmount()
#         detailDic["minimum payment for last statement"] = minimumPayment
#         detailDic["total negative transactions before grace day"] = minimumPayment - unpaid
#         detailDic["unpaid minimum payment for previous statement"] = unpaid
#         detailDic[f"latefee for {method}"] = statement.bill.lateFee
#         detailDic["vat latefee"] = statement.bill.vatLateFee
#
#         dataList = detailDic.values()
#         index = detailDic.keys()
#
#         df = pd.DataFrame(dataList, index=index)
#         return df
#
#     def getIntDetail(self, number) :
#         if (number < 2) :
#             return
#         statement = self.getStatement(number)
#         if (statement == None) :
#             return
#         if statement.bill.totalInterest <= 0 :
#             return
#
#         detailDic = {}
#         unpaid = statement.dueDayUnpaidTotal
#         totalPayment = statement.lastStatement.bill.totalPayment
#         endDate = statement.bill.endDate
#         lastEndDate = statement.lastStatement.bill.endDate
#         detailDic["total negative transactions before due day"] = totalPayment - unpaid
#         detailDic["full payment for previous statement"] = totalPayment
#         detailDic["Credit Line"] = statement.cif.creditLine
#         detailDic["APR"] = statement.bill.apr
#         detailDic["MPR"] = statement.bill.mpr
#         detailDic["First Day of the cycle"] = statement.bill.startDate
#         detailDic["End Day of the cycle"] = endDate
#         detailDic["Days in the cycle"] = statement.bill.dateNum
#         detailDic["Average Daily Balance"] = statement.bill.adb
#         detailDic[f"last day UDI of cycle-{endDate}"] = statement.bill.curUDI
#         detailDic[f"last day UDI of last cycle-{lastEndDate}"] = statement.bill.lasUDI
#         detailDic["factor"] = statement.bill.factor
#         detailDic["inflation taxable"] = statement.bill.mpr_taxable
#         detailDic["inflation non taxable"] = statement.bill.inflation
#         detailDic["int taxable"] = statement.bill.intTaxable
#         detailDic["int not taxable"] = statement.bill.interestNotTax
#         detailDic["total int"] = statement.bill.totalInterest
#         detailDic["vat of int"] = statement.bill.vatInterest
#
#         dataList = detailDic.values()
#         index = detailDic.keys()
#
#         df = pd.DataFrame(dataList, index=index)
#         return df
#
#
#     # 获取未还明细
#     def getUnpaidDetail(self, number) :
#         if (number < 1) :
#             return
#         statement = self.getStatement(number)
#         if (statement == None) :
#             return
#         detailList = statement.bill.originUnpaidDetail
#         df = pd.DataFrame(detailList)
#         df = df.loc[:, ~df.apply(is_all_zero)]
#         columns = df.columns
#         column_names = list(df.columns)
#         if len(column_names) == 0 :
#             return
#         tuple_list = list(map(lambda x: (x,"origin"), column_names))
#         multi_index = pd.MultiIndex.from_tuples(tuple_list)
#         df.columns = multi_index
#
#         detailList = statement.bill.endUnpaidDetail
#         leftDf = pd.DataFrame(detailList)
#         leftDf = leftDf[columns]
#         tuple_list = list(map(lambda x: (x,"left"), column_names))
#         leftDf.columns = pd.MultiIndex.from_tuples(tuple_list)
#
#         df = pd.concat([df, leftDf], axis=1)
#         number = len(column_names)
#         new_order_positions = []
#         for i in range(number*2) :
#             if (i & 1) :
#                 index = ((i - 1) >> 1) + number
#             else :
#                 index = i >> 1
#             new_order_positions.append(index)
#         df = df.iloc[:, new_order_positions]
#         # df.columns.names= ["未还明细",""]
#
#         row_names = []
#         for i in range(len(detailList)-1) :
#             row_names.append("history-" + str(i+1))
#         row_names.append("current")
#         df.index = row_names
#         return df
#
# def dataFrameOfFlagDesciption(flag) :
#     data = {}
#     for name, member in flag.__members__.items():
#         data[name] = member.description
#     df = pd.DataFrame(data, index=[0])
#     df.index = [flag.__name__]
#     return df
#
# # def autoWidthDF(df) :
# #     df.style.set_table_styles([{
# #         'selector': '',
# #         'props': [('width', 'auto')]
# #     }])
#
# def displayLabels(exported = False) :
#     flags = StoriLabel.getLabelFlags()
#     dfs = {}
#     dfsExported = {}
#     for key, value in flags.items() :
#         if type(value) == list :
#             dflist = []
#             for flag in value :
#                 df = dataFrameOfFlagDesciption(flag)
#                 display(df)
#                 dflist.append(df)
#                 dfsExported[flag.__name__] = df.transpose()
#             dfs[key] = dflist
#         else :
#             df = dataFrameOfFlagDesciption(value)
#             dfs[key] = df
#             display(df)
#             dfsExported[value.__name__] = df.transpose()
#
#     if exported == False :
#         return
#
#     with pd.ExcelWriter('export/LabelDescription.xlsx') as writer:
#         exported = dfs
#         # exported = dfsExported
#         for key, value in exported.items() :
#             if type(value) == list :
#                 startrow = 0
#                 for df in value :
#                     sf = StyleFrame(df)
#                     sf.to_excel(writer, sheet_name=key, startrow=startrow, index=True, best_fit=list(df.columns))
#                     startrow += len(df) + 2
#             else :
#                 sf = StyleFrame(value)
#                 sf.to_excel(writer, sheet_name=key, index=True, best_fit=list(value.columns))
