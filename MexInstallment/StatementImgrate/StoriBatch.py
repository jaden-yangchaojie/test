from StoriScenario import StatementScenario
import json
import os
import pandas as pd
# from IPython.display import clear_output, display
from typing import List
# from styleframe import StyleFrame, Styler
# from StoriView import StoriView
from StoriPipeLine import StoriPipeLine

class StoriBatch :
    def __init__(self, dir="Scenario", fileNames = [], op = None, filterScenarios = None):

        self.batchFileData = {}
        scenarios = self.getScenariosFrom(dir, fileNames, filterScenarios)
        self.scenarios: List[StatementScenario] = scenarios
        if op == "base" : # 解析base场景
            self.initBase()
        elif op == "pipeline" : # 整理场景
            self.data = self.initPipeLine()
        else :
            self.data = self.initScenarios()

    def initScenarios(self) :
        userDic = {}
        for scenario in self.scenarios:
            scenario.readScenario()
            userDic[scenario.name] = scenario.user
        return userDic

    def initBase(self) :
        for scenario in self.scenarios:
            scenario.exportBaseScenario()

    def initPipeLine(self) :
        userDic = {}
        userVars = {}
        toPipeLineList = []
        for scenario in self.scenarios:
            userVars[scenario.name]= scenario.variables.copy()
            requestList = scenario.getRequestList()
            toPipeLineList.extend(requestList)
            userDic[scenario.name] = scenario.user
        # pipeline
        pipeLine = StoriPipeLine()
        pipeLine.run(toPipeLineList, userDic, userVars)
        return userDic

    # 从场景文件中读取场景
    def getScenariosFrom(self, dir = "Scenario", fileNames = [], filterScenarios = None) -> list:
        # 读取文件
        files = []
        path = dir + "/" if len(dir) > 0 else ""
        if len(fileNames) > 0 :
            for fileName in fileNames :
                files.append(path + fileName + '.json')
        else :
            files = list(map(lambda x:path + x,  filter(lambda x:x.endswith(".json") , os.listdir(path))))

        scenarios = []
        for file in files :
            with open(file, 'r') as f:
                fileData = json.load(f)
                self.batchFileData[file] = fileData
            dataList = fileData["data"]
            for data in dataList :
                scenarioInstance = StatementScenario(data)
                if filterScenarios and not scenarioInstance.name in filterScenarios :
                    continue
                scenarios.append(scenarioInstance)
        return scenarios

    # 获取某个场景
    def getScenario(self, name) -> StatementScenario:
        for scenario in self.scenarios :
            if (scenario.name == name) :
                return scenario
        return None

    # 打印场景中的所有用例名称
    def printScenariosName(self) :
        names = []
        for scenario in self.scenarios:
            names.append(scenario.name)
        print(names)

    # 获取场景中所有用例的名称
    def getScenariosName(self) :
        names = []
        for scenario in self.scenarios:
            names.append(scenario.name)
        return names

    # 更新断言
    def updateAndExportScenarios(self, error = False):
        for scenario in self.scenarios:

            # 更新assert数据
            scenario.unpdateScenario()

            # 更新view数据
            # scenario.updateViews()

        for  file, fileData in self.batchFileData.items() :
            directory, filename = os.path.split(file)
            outputDir = directory + "/updated/"
            output = outputDir + filename

            if not os.path.exists(outputDir) :
                os.makedirs(outputDir)
            with open(output, 'w', encoding='utf-8') as f:
                print(output)
                json.dump(fileData, f, ensure_ascii=False)

    # 查找符合条件的用例
    def getScenariosFitTheLabel(self, *labelArgs) :
        scenarioNameList = []
        for scenario in self.scenarios:
            view = scenario.getView()
            meetList = view.getCasesMeetLabel(*labelArgs)
            if len(meetList)>0 :
                for number in meetList :
                    scenarioNameList.append(scenario.name + "_第" + str(number)+"期账单")
        return scenarioNameList

    def sheetNameOfScenario(self, scenarioName:str) :
        if scenarioName.startswith("第一期"):
            return "一期"
        elif scenarioName.startswith("第二期"):
            return "二期"
        elif scenarioName.startswith("第三期"):
            return "三期"
        elif "期账单" in scenarioName :
            return "N期"
        elif scenarioName.startswith("UAT") or scenarioName.startswith("EXTRA_UAT"):
            return "UAT"
        elif "免息券" in scenarioName :
            return "免息券"
        else :
            return "其他"

    # def exportAllScenarioLabels(self) :
    #     writer = pd.ExcelWriter('export/AllScenarioLabels.xlsx')
    #     startrowDic = {}
    #     for scenario in self.scenarios:
    #         df = pd.DataFrame({"":[scenario.name]}, index=[""])
    #         sf = StyleFrame(df)
    #         sheetName = self.sheetNameOfScenario(scenario.name)
    #         startrow = 0
    #         if sheetName in startrowDic :
    #             startrow = startrowDic[sheetName]
    #         else :
    #             startrowDic[sheetName] = 0
    #         sf.to_excel(writer, sheet_name=sheetName, startrow=startrow, index=True)
    #         dfs = self.getLabelsOfScenario(scenario.name)
    #         for df in dfs :
    #             sf = StyleFrame(df)
    #             sf.to_excel(writer, sheet_name=sheetName, startrow = startrow + 2, index=True, best_fit=list(df.columns))
    #             startrow += len(df) + 2
    #             startrowDic[sheetName] = startrow
    #         startrowDic[sheetName] += 5
    #
    #     notCovered = self.getNotCovered()
    #     notCoveredData = map(lambda x:{"name":x.name, "description":x.description}, notCovered)
    #     df = pd.DataFrame(notCoveredData)
    #     sf = StyleFrame(df)
    #     sf.to_excel(writer, sheet_name="没有覆盖到的标签", startrow=0, index=True,best_fit=list(df.columns))
    #     writer.close()

    def getLabelsOfScenario(self, name) :
        scenario = self.getScenario(name)
        view = scenario.getView()
        trueDescrips = view.getTrueDescrips()
        cifTrueDescriptions = view.getCifTrueDescrips()

        cifDF = pd.DataFrame(cifTrueDescriptions).transpose()
        # cifDF.index = [name]

        columns = []
        for i in range(len(trueDescrips)) :
            number = "第" + str(i + 1) + "期"
            columns.append(number)
        df = pd.DataFrame(trueDescrips, index=columns).transpose()
        return [cifDF, df]

    # 展示场景标签
    # def displayLabelsOfScenario(self, name) :
    #     dfs = self.getLabelsOfScenario(name)
    #     for df in dfs :
    #         display(df)

    # 获取所有用例的标签
    # def getLabelsDF(self) :
    #     df = pd.DataFrame()
    #     for scenario in self.scenarios:
    #         view:StoriView = scenario.getView()
    #         if not view :
    #             continue
    #         labels = view.getAllLabels()
    #         labelDF = pd.DataFrame(labels)
    #         stat = labelDF.apply(lambda col: (col == True).any())
    #         cifDF = view.getCifLabelDF()
    #         stat = pd.concat([stat, cifDF])
    #         stat.name = scenario.name
    #         df = df._append(stat)
    #     return df

    # 获取没有覆盖的标签
    def getNotCovered(self) :
        df = self.getLabelsDF()
        notCovered = df.columns[~df.apply(lambda col: (col == True).any())]
        return notCovered

    # 获取覆盖用例最小集
    def getMiniCoveredCased(self) :
        coverInfo = self.getLabelsDF()
        maxNames = []
        dropLabels = []
        covers = coverInfo
        coverCountList = []
        for i in range(30) :
            # drop已经覆盖的标签
            covers = covers.drop(dropLabels, axis=1)
            # 获取用例对应的标签数量
            coverCountsRow = covers.sum(axis=1)
            # 获取覆盖标签数量最大的用例名
            maxIndex = coverCountsRow.idxmax()
            coverNumber = coverCountsRow[maxIndex]
            if coverNumber == 0 :
                break
            coverCountList.append(coverNumber)
            maxNames.append(maxIndex)
            # 获取改用例覆盖的标签
            maxCoverInfo = covers.loc[maxIndex]
            dropLabels = list(maxCoverInfo[maxCoverInfo == True].index)
        print(maxNames)
        print(coverCountList)
        print(sum(coverCountList))

    # 获取标签的被覆盖情况
    def getLabelCoveredInfo(self) :
        df = self.getLabelsDF()
        coverCounts = df.sum(axis=0)
        coverCounts = coverCounts[coverCounts!=0]
        return coverCounts

    # # 获取用例的覆盖情况
    # def getCasesCoveredInfo(self, dropLabels = None) :
    #     df = self.getLabelsDF()
    #     if dropLabels :
    #         df = df.drop(dropLabels, axis=1)
    #     # df = df.drop(index='')
    #     coverCounts = df.sum(axis=1)
    #     return coverCounts
    #
    # # 展示没有覆盖的标签
    # def displayNotCovered(self) :
    #     notCovered = self.getNotCovered()
    #     notCoveredData = map(lambda x:{"name":x.name, "description":x.description}, notCovered)
    #     df = pd.DataFrame(notCoveredData)
    #     df.columns.names= ["没有覆盖到的标签"]
    #     display(df)
    #
    # def getAllLabeledDataForUser(self) :
    #     dataList = []
    #     indexList = []
    #     for scenario in self.scenarios:
    #         view = scenario.getView()
    #         labels = view.getAllLabels()
    #         # cifLabelDict = scenario.curStatement.cif.label.getLabelDict()
    #         for labelDict in labels :
    #             # labelDict.update(cifLabelDict)
    #             dataList.append(labelDict)
    #         for i in range(len(labels)) :
    #             indexList.append((scenario.name, "账期" + str(i+1)))
    #     multi_index = pd.MultiIndex.from_tuples(indexList)
    #     df = pd.DataFrame(dataList, index=multi_index)
    #     multi_columns = map(lambda x:(x,x.description), df.columns)
    #     df.columns = pd.MultiIndex.from_tuples(multi_columns)
    #     return df
    #
    # def getAllLabeledDataForStatement(self) :
    #     dataList = []
    #     indexList = []
    #     for scenario in self.scenarios:
    #         view = scenario.getView()
    #         labels = view.getAllLabels()
    #         # cifLabelDict = scenario.curStatement.cif.label.getLabelDict()
    #         for labelDict in labels :
    #             # labelDict.update(cifLabelDict)
    #             dataList.append(labelDict)
    #         for i in range(len(labels)) :
    #             indexList.append((scenario.name, "账期" + str(i+1)))
    #     multi_index = pd.MultiIndex.from_tuples(indexList)
    #     df = pd.DataFrame(dataList, index=multi_index)
    #     multi_columns = map(lambda x:(x,x.description), df.columns)
    #     df.columns = pd.MultiIndex.from_tuples(multi_columns)
    #     return df

    # 检查冗余
    def checkDuplicates(self) :
        df = self.getAllLabeledDataForStatement()
        print("账期总数：", df.shape[0])
        group = df.groupby(list(df.columns))
        print("标签不同的账期数：", len(group))

        # size = group.size()
        # # values = size.values
        # # print(values)
        # # names = list(map(lambda x:x[1], size.index.names))
        # # print(names)

        # for index in size.index:  
        #     duplicatedNum = size.loc[index]
        #     if duplicatedNum > 5:
        #         print("重复次数：",duplicatedNum)
        #         names = size.index.names
        #         # filtered_list = [item for pair in zip(index, names) if pair[0] > threshold]  
        #         filtered_list = [name for value, name in zip(index, names) if value==True]
        #         trueLabels = list(map(lambda x:x[1], filtered_list))
        #         # conditions = tuple(map(lambda x:x[0], filtered_list))
        #         print(trueLabels)
        #         # print(filtered_list)
        #         # print(conditions)
        #         # fitCases = batch.getScenariosFitTheLabel(conditions)
        #         # print(len(fitCases))
        #         # print(fitCases)
        #         # condition = tuple(filtered_list)
        #         # print(index)

        df1 = self.getLabelsDF()
        print("用例总数：", df1.shape[0])
        group1 = df1.groupby(list(df1.columns))
        print("标签不同的用例数：", len(group1))

        # duplicates = df.duplicated()
        # df_last_duplicates = df.drop_duplicates(keep='last')
        # print(df_last_duplicates.shape)

    # def compareScenario(self, scenarioA, scenarioB) :
    #     labelA = self.getLabelsOfScenario(scenarioA)
    #     labelB = self.getLabelsOfScenario(scenarioB)
    #     print()

    # def exportScenario(self, name) :
    #     outputDir = 'export/cases/'
    #     if not os.path.exists(outputDir) :
    #         os.makedirs(outputDir)
    #     fileName = f'{outputDir}{name}.xlsx'
    #     writer = pd.ExcelWriter(fileName)
    #     # startrowDic = {}
    #     scenario = self.getScenario(name)
    #     if scenario == None :
    #         print("没有这个场景")
    #         return
    #     if not scenario.curStatement or (scenario.curStatement.bill.number == 1 and scenario.curStatement.isBilled == False):
    #         print(scenario.name, "没有已出账单")
    #         return
    #
    #     view = scenario.getView()
    #     # number = scenario.curStatement.bill.number
    #
    #     funcDict = {
    #         "statement cycle" : view.getCycle,
    #         "trading list" : view.getTradingList,
    #         # "unpaid detail" : view.getUnpaidDetail,
    #          "payment allocation" :  view.getPaymentList,
    #         "balance list" : view.getBalanceList,
    #         "adb list" : view.getADBList,
    #         "late fee" : view.getLateFeeDetail,
    #         "interest" :view.getIntDetail,
    #         "minimum payment" :view.getMinimumPayment,
    #         "DQ Info" : view.getDQInfo,
    #         "bill" : view.getBill,
    #     }
    #
    #     for statement in view.statementList :
    #         if not statement.isBilled :
    #             break
    #         number = statement.bill.number
    #         startrow = 0
    #         sheetName = "statement " + str(number)
    #         for name,f in funcDict.items() :
    #
    #             df = f(number)
    #             if type(df) != pd.DataFrame :
    #                 continue
    #
    #             nameDf = pd.DataFrame({name:[""]})
    #             sf = StyleFrame(nameDf)
    #             sf.to_excel(writer, sheet_name=sheetName, startrow= startrow, index=False, best_fit=list(nameDf.columns))
    #
    #             startrow += 1
    #
    #             sf = StyleFrame(df)
    #             sf.to_excel(writer, sheet_name=sheetName, startrow=startrow, index=True, best_fit=list(df.columns))
    #             startrow += len(df) + 2
    #     writer.close()
