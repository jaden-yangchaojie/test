
import json
import re
from StoriUtils import round_to_even, getUTCDateTime, getISO8601UTCTimeStr
from StoriStatement import Statement
from datetime import datetime, time
from StoriTrade import TradingType
from StoriInstallment import Installment
# from StoriView import StoriView
from StoriBill import StoriBill
# import os
from StoriCif import StoriCif
import uuid
import StoriPath
from StoriUser import StoriUser

POMELO_TRADING_SID_LIST = ("d8044c43-31fe-429a-9abd-2e7853871806",
                     "6e933136-e398-02c0-13e5-5806f0f1289a",
                     "4eafa7e1-f2a2-4187-bd3e-951a83ab9c1f",
                     "9b8b87bb-b4eb-e46c-1e08-c7acc46a1e99",
                     "e81c01b2-6398-4b11-a830-b6fb330bccbc"
                    )
APP_TRADING_SID_LIST = ("bee5cead-8ee2-0a8d-c649-6a3b89ee394c",
                     "dddf1a91-a4d6-ab65-00c1-37dcd379a6e3",
                     "889b4ace-6876-4edd-970a-bbf51db53fd9",
                    )
CHANGE_DATE_SID = "9d374320-74ae-4433-bcd4-c69165f86691"
SIGN_SID = "e657e600-a5db-4ff2-ac32-49e198e4c482"
CHANGE_CARD_SID = "af13568a-ca9d-18fa-8f3b-6dd61bfe927b"
GEN_BILL_SID = "74eec8a1-b74e-4a17-a919-2ef74cf65e14"
CHECK_LATEST_BILL_SID = "f7255a5c-c697-4455-aa13-1a2b68cf79da"
CHECK_BILL_PROCESS_SID = "e0be200b-b598-4eb7-9b28-e1e9862333bb"
ACTIVE_CARD_SID = "61721c54-2d04-fc49-d720-66d76e3353a9"
OTHER_SID_LIST = ("462f4677-a6c9-4453-95ac-d057c2da5d96",
                           "61721c54-2d04-fc49-d720-66d76e3353a9",
                             "9862d874-bd3e-4b3b-8b7d-583776263709",
                             "19435b3f-2863-48d1-b2c5-40aff2dfd626",
                             "a72c15b3-3f31-442e-9971-d0f271034d26",
                             "2c68a001-f148-432c-8d72-29ea0f7e5296",
                             "10b1a835-11ae-4059-a800-8f4e02a3bdaf",
                             "c0e6a4e7-3625-4881-b742-5327a078fb23",
                             "c12f36c0-a996-4452-97a7-448870cbc783",
                             "dd1d38b5-c045-cc5b-b7f9-9af3a5d9a84a",
                             "86ccaff2-1076-c527-5d73-c3a73e1e2ed6",
                             "ea50d022-e3b0-4ed7-be40-b0ad6b2376a9",
                             "dd6d635e-d8c7-361b-c6f6-ceffe16d14e9",
                             "d2e57bf3-6546-49d0-bd79-ea84fc62c3ae",
                             "1553ddd1-755c-5320-225f-166118c4ad2b",
                             "c11fb186-f84b-4689-96d1-8dca0b0ebae2",
                             "1d2903b6-6a34-4ada-907d-ca1b2704eac6")

PRE_SERVICE_CHECK_GID = 'd2721619-2ee0-47d4-a59a-1ac730972800'
STATEMENT_VIEW_UPDATE_NOTIFICATION_GID = 'c31e2904-d7ca-4cd6-982f-167327dff5eb'
DQ_NOTIFICATION_GID = "ccac6a64-8904-49de-b859-815a7eda3b0a"
CHANGE_DATE_GID = "1eefc592-4db0-4098-9aff-87ba14bd174e"
STATEMENT_GID = "46099e82-ba61-4cda-bf6d-a924d89e9337"
STATEMENT_CHECK_GID = "a40852ea-f16b-4067-a8fa-c75a29ec1f44"
DQ_DAYS_UPDATE_GID = '7b6180c9-4cc1-4826-9d96-d1293a4b96e5'
XXL_JOB_TRIGGER_GID = '86ccaff2-1076-c527-5d73-c3a73e1e2ed6'
POMELO_SIGN_MOCK_GID = '1572c537-0215-42fd-bf3c-1462cf72d96d'
POMELO_CREATE_CARD_MOCK_GID = 'b6008e52-7bf3-4b5e-af17-8bd678231e0f'
POMELO_GET_CARD_MOCK_GID = 'ebae7dce-4707-466b-9324-13237846d573'

BASE_SID_LIST = {
    DQ_NOTIFICATION_GID : "账单通知DQ",
    DQ_DAYS_UPDATE_GID : "DQ天数更新",
    STATEMENT_CHECK_GID : "出账校验",
    CHANGE_DATE_GID : "修改时间",
    XXL_JOB_TRIGGER_GID : "XXLJOB",
    POMELO_SIGN_MOCK_GID : "pomelo-sign-mock",
    POMELO_CREATE_CARD_MOCK_GID :"pomelo-create-card-mock",
    POMELO_GET_CARD_MOCK_GID : "pomelo-get-card-mock"
}

# gNeedCheck = True

gErrorCases = []
gNeedCheckedCases = []

def checkEnable(scenario) :
    return scenario["enable"]

def unableScenario(scenario) :
    scenario["enable"] = False

def getBodyJson(scenario) :
    body = scenario["body"]
    if body["kv"] == True:
        jsonObject = body["kvs"]
        jsonObject = list(filter(lambda x: x["valid"]==True and x["enable"]==True and "name" in x and "value" in x, jsonObject))
    elif "format" in body and body["format"] == 'JSON-SCHEMA' :
        jsonSchema = body["jsonSchema"]
        properties:list = jsonSchema["properties"]
        required:dict = jsonSchema["required"]
        jsonObject = {k: v["mock"]["mock"] for k, v in filter(lambda item: item[0] in required, properties.items())}
    elif body["json"] == True :
        if "raw" in body and body["raw"]:
            try :
                jsonObject = json.loads(body["raw"])
            except :
                jsonObject = body["raw"]
        else :
            jsonObject = {}
    else :
        jsonObject = {}
  
    if len(jsonObject) == 0 :
        jsonObject = {}
    return jsonObject

def getAPIScenarioKV(scenario, type) :
    kvList = scenario[type]
    ret = {}
    for kv in kvList :
        if kv["valid"] == True and kv["enable"] == True:
            name = kv["name"]
            value = kv["value"] if "value" in kv else ""
            if len(name) > 0 :
                ret[name] = value
    return ret

def getHeaders(scenario) :
    return getAPIScenarioKV(scenario, "headers")

def getArguments(scenario) :
    return getAPIScenarioKV(scenario, "arguments")

def getMethod(scenario) :
    method = scenario["method"]
    assert(method == "POST" or method == "GET" or method == "PUT")
    return method

def updateBodyJson(scenario, jsonObject) :
    body = scenario["body"]
    if body["kv"] == True:
        body["kvs"] = jsonObject
    else :
        body["raw"] = json.dumps(jsonObject)
    return jsonObject

def getVarsFromExtractData(extractData) :
    vars = {}
    dataList = extractData["json"]
    for data in dataList :
        key = data["expression"]
        value = data["value"]
        if (len(value) == 0) :
            value = "${" + data["variable"] + "}"
        vars[key] = value
    return vars

def getVarsFromScriptData(preData) :
    vars = {}
    if preData == None or ("script" in preData) == False:
        return vars
    preDataScript = preData["script"]

    matches = re.findall("//.*\n", preDataScript)
    for line in matches:
        line = line[: -1]
        preDataScript = preDataScript.replace(line, "")

    reg = "vars.put(.*);"
    matches = re.findall(reg, preDataScript)
    for line in matches:

        params = line.split(",")
        left = "${" + params[0][2:-1] + "}"
        right = params[1].lstrip(" ").lstrip("(").lstrip("\"").rstrip(" ").rstrip(";").rstrip(")").rstrip("\"")
        vars[left] = right 
            
        reg = right + "\s*" + "=" + "\s*\"\${.*}"
        match = re.search(reg, preDataScript)
        if (match != None) :
            param1 = preDataScript[match.start(): match.end()]
            reg = "\${.*}"
            match = re.search(reg, param1)
            param1 = param1[match.start(): match.end()]
            vars[left] = param1
    return vars

def checkVariables(data, variables) :
    if (type(data) is str) :
        if (data.startswith("${") and data in variables) :
            data = variables[data]
    elif (type(data) is dict) :
        for key, value in data.items() :
            data[key] = checkVariables(value, variables)
    return data

def variablesFromScenario(scenario) :
    if ("variables" in scenario) :
        curVariables = {}
        for data in scenario["variables"] :
            if ("value" in data) :
                value = data["value"]
            else :
                continue
            if ("name" in data) :
                name = "${" + data["name"] + "}"
                curVariables[name] = value
        return curVariables
    return {}

# 前置/后置/断言
def getOperationData(data, operationType) :
    hashTree = data["hashTree"]
    opList = []
    for op in hashTree :
        if (operationType == op["type"]) :
            opList.append(op)
    return opList

# 获取断言结果数据
def getExpectData(data, key) :
    results = data["jsonPath"]
    for result in results :
        expression = result["expression"]
        if (expression != key) :
            continue
        if (checkEnable(result) == False) :
            return None
        ret = result["expect"]
        return ret
    return None

# 删除断言结果
def delExpectData(data, key, path = "jsonPath") :
    results = data[path]
    for index, result in enumerate(results):  
        expression = result["expression"]
        if (expression == key) :
            del results[index]
            break
        
# 断言数据
def getAssertData(data) :
    assertData = getOperationData(data, "Assertions")
    if len(assertData) > 0 :
        return assertData[0]
    return None

# 获取前置脚本
def getPreScriptList(data) :
    preData = getOperationData(data, "JSR223PreProcessor")
    return preData

# 后置操作
def getExtractList(data) :
    extractData = getOperationData(data, "Extract")
    return extractData

# 获取后置脚本
def getExtractScriptList(data) :
    extractData = getOperationData(data, "JSR223PostProcessor")
    return extractData

# 获取resourceId
def getResourceId(data) :
    if "resourceId" in data :
        resourceId = data["resourceId"]
    else :
        resourceId = data["projectId"]
    return resourceId

class DefalutScenario:
    def __init__(self, scenarioData): 
        self.systime : datetime = None
 
        self.data = scenarioData

        self.readed = False
        
        if ("name" in scenarioData) :
            name = scenarioData["name"]
            self.name = name
            # print(name)

        if ("modulePath" in scenarioData) :
            modulePath = scenarioData["modulePath"]
            self.modulePath = modulePath.split("/")[-1]
        
        if "scenarioDefinition" in scenarioData :
            scenarioDefinition = scenarioData["scenarioDefinition"]
            scenarioJson = json.loads(scenarioDefinition)
        else :
            scenarioJson = scenarioData
        self.scenarioJson = scenarioJson

        self.variables = variablesFromScenario(scenarioJson)
        # if len(self.variables) > 0 :
        #     print()
        # print(self.variables)
        # scenarioJson
        # dict_keys(['headers', 'variables', 'mockEnvironment', 'active', 'environmentMap', 'type', 'isMockEnvironment', 'environmentEnable', 'referenced', 'enable', 'name', 'enableCookieShare', 'hashTree', 'id', 'projectId', 'clazzName', 'onSampleError'])
    
        # self.hashTreeList = scenarioJson["hashTree"]

        self.ended = False

        self.lateInsertDic = {}
        self.lateDelDic = {}
        self.autoDisabledIds = {}
        self.replaceScenarioMap = {}
        self.mockInsertMap = {}
        self.ignoreIds = {}
        # self.memScenarioMap = {}

    def generateID(self) :
        return str(uuid.uuid4())

    def readScenario(self):
        # hashTree
        # dict_keys(['headers', 'resourceId', 'variables', 'mockEnvironment', 'refType', 'active', 'index', 'environmentMap', 'type', 'isMockEnvironment', 'environmentEnable', 'referenced', 'enable', 'name', 'enableCookieShare', 'hashTree', 'id', 'mixEnable', 'projectId', 'clazzName'])
        
        if self.readed == True :
            return
        self.handleScenario(self.scenarioJson, self.variables, isLast=True)
        self.readed = True

    def exportBaseScenario(self) :
        print(self.name)
        sid = self.scenarioJson["id"]
        print(sid)
        output = "Scenario/base/" + self.name + ".json"
        with open(output, 'w', encoding='utf-8') as f:
            print(output) 
            json.dump(self.scenarioJson, f, ensure_ascii=False)
        # for key, value in BASE_SID_LIST.items() :
        #     output = "Scenario/base/" + value + ".json"
        #     if sid == key :
        #         with open(output, 'w', encoding='utf-8') as f:
        #             print(output) 
        #             json.dump(self.scenarioJson, f, ensure_ascii=False)

    def getBaseScenario(self, sid) :
        name = BASE_SID_LIST[sid]
        file = "/Users/ycj/pytest/pytest/MexInstallment/imgrate/base/" + name + ".json"
        with open(file, 'r') as f:
            fileData = json.load(f)
        return fileData

    def unpdateScenario(self):
        jsonStr = json.dumps(self.scenarioJson, ensure_ascii=False)
        self.data["scenarioDefinition"] = jsonStr
        self.data["modulePath"] = "/" + self.modulePath

    # 插入场景scenarios到nextScenario之前
    def lateInsertScenario(self, scenarios, nextScenario) :
        ret = self.findTargetLocation(self.scenarioJson, nextScenario)
        if ret == None :
            assert(0)
        parent = ret[0]
        resourceId = getResourceId(parent)
        if not (resourceId in self.lateInsertDic) :
            self.lateInsertDic[resourceId] = []
        index = ret[1]
        inserts = self.lateInsertDic[resourceId]
        for scenario in scenarios:
            inserts.append((index + len(inserts), scenario))
    
    # 删除scenario
    def lateDelScenario(self, scenario) :
        print("删除多余的一条：", scenario["name"])
        ret = self.findTargetLocation(self.scenarioJson, scenario)
        if ret == None :
            assert(0)
        parent = ret[0]
        index = ret[1]
        delScenario = parent["hashTree"][index]
        resourceId = getResourceId(parent)
        if not (resourceId in self.lateDelDic) :
            self.lateDelDic[resourceId] = []
        dels = self.lateDelDic[resourceId]
        dels.append(delScenario)

    # 在scenario中查找到target场景的位置
    def findTargetLocation(self, scenario, target) :
        stype = scenario["type"]
        if stype == "scenario" :
            hashTree = scenario["hashTree"]
            for index, value in enumerate(hashTree):  
                if value == target :
                    return (scenario, index)
                ret = self.findTargetLocation(value, target)
                if (ret != None and ret[1] == 0) :
                    return (scenario, index)
                if ret != None :
                    return ret
            return None
        else :
            return None
    
    # 检查断言是否一致
    def checkExpectData(self, assertData, key, checkData, precision = 2) :
        if (key == None) :
            return
        expectData = getExpectData(assertData, key)
        if (expectData == None) :
            return
        if (type(checkData) == str) :
            if expectData.startswith("${") == False :
                if (expectData != checkData) :
                    print("assert error:", expectData, checkData)
                    assert(0)
            else :
                print("数据异常")
        else :
            if (precision == 0) :
                expectData = int(expectData)
            else :
                expectData = float(expectData)
                checkData = round_to_even(checkData, precision)
            if (expectData != checkData) :
                print("assert error:", expectData, checkData)
                assert(0)

    def updateResult(self, result, key, value, precision = 2) :
        if (type(value) == str) :
            result["expect"] = value
        else :
            if (precision > 0) :
                result["expect"] = "{:.{}f}".format(value, precision)
            else :
                result["expect"] = str(value)
        result["description"] = key + " expect: " + result["expect"]
        result["enable"] = True
        
    # disable断言数据
    def disableExpectData(self, data, key) :
        results:list = data["jsonPath"]
        for result in results :
            expression = result["expression"]
            if (expression == key) :
                result["enable"] = False
                return

    # 更新断言结果数据
    def updateExpectData(self, data, key, value, precision = 2, needCheck = True, option = 'REGEX') :
        if (needCheck) :
            try :
                self.checkExpectData(data, key, value, precision)
            except AssertionError as e:  
                gErrorCases.append(self.name + " : " + key + " " + str(value) + " " + str(self.systime.date())) 

        results:list = data["jsonPath"]
        # exps = [" expect: ", " REGEX: ", " EQUALS: "] 
        exist = False
        for result in results :
            expression = result["expression"]
            if (expression == key) :
                self.updateResult(result, key, value, precision)
                exist = True
                break
            
        if exist == False :
            result = {}
            result["expression"] = key
            result["type"] = "JSON"
            result["option"] = option
            result["enable"] = True
            result["valid"] = True
            self.updateResult(result, key, value, precision)
            results.append(result)

    def printScenarioInfo(self, scenario) :

        sid = scenario['id'] if "id" in scenario else ""
        name = scenario['name'] if "name" in scenario else ""

        print(f"{sid}:{name}")
    
    def printStepInfo(self, scenario, stepInfo) :
        name = scenario['name'] if "name" in scenario else ""
        print(stepInfo,"--",name)

    def checInsertMock(self, scenario) :
        if not "hashTree" in scenario :
            return
        hashTree:list = scenario["hashTree"]
        for i, subScenario in enumerate(hashTree) :
            if subScenario['type'] == 'HTTPSamplerProxy' and "path" in subScenario and subScenario["path"] in self.mockInsertMap :
                path = subScenario["path"]
                gid = self.mockInsertMap[path]
                if i==0 or ("id" in hashTree[i-1] and hashTree[i-1]["id"] != gid):
                    insertScenario = self.getBaseScenario(gid)
                    hashTree.insert(i, insertScenario)
        
    def handleScenario(self, scenario, parentVariable = {}, stepInfo = "", isLast = False, inserted = False, parentScenario = None):

        if checkEnable(scenario) == False :
            return
        
        if "id" in scenario :
            if scenario["id"] in self.autoDisabledIds :
                unableScenario(scenario)
                return
            if scenario["id"] in self.ignoreIds :
                self.checInsertMock(scenario)
                return

        stype = scenario['type']
        step = 1

        if (len(stepInfo) == 0) :
            stepInfo = self.name + " : "
        else :
            stepInfo = stepInfo + "."

        # 获取环境变量
        curVariables = variablesFromScenario(scenario)
        for key,value in curVariables.items() :
            if key not in parentVariable :
                parentVariable[key] = value
            # else :
                # if parentVariable[key] != curVariables[key] :
                #     print(key, parentVariable[key], curVariables[key])
                #     print()
        variables = self.variables
        # self.variables.update({k: v for k, v in curVariables.items() if k not in self.variables})
        # variables = self.variables
        # variables = variablesFromScenario1(scenario, parentVariable)

        preMap = {}
        dataList = getPreScriptList(scenario)
        for scriptData in dataList :
            varsDic = getVarsFromScriptData(scriptData)
            if (len(varsDic) > 0) :
                for key, value in varsDic.items() :
                    if "__metersphere_env_id" in key :
                        continue
                    if (key not in ["${signature}"]) :
                        preMap[key] = value
                    if (key == "${userName}") :
                        preMap[key] = "${__userName}"
                    elif (value == "${__UUID}") :
                        value = self.generateID()
                    variables[key] = value

        if (stype == 'scenario') :
            self.checInsertMock(scenario)
            hashTree : list = scenario["hashTree"]
            # scenarioNum = len(hashTree)
            for subScenario in hashTree :
                if "id" in subScenario and subScenario["id"] in self.replaceScenarioMap.keys() :
                    sid = self.replaceScenarioMap[subScenario["id"]]
                    resourceId = getResourceId(subScenario)
                    enable = checkEnable(subScenario)
                    # asserts = subScenario["hashTree"][2]["hashTree"]
                    subScenario = self.getBaseScenario(sid)
                    subScenario["resourceId"] = resourceId
                    subScenario["enable"] = enable
                    # subScenario["hashTree"][2]["hashTree"] = asserts
                    hashTree[step-1] = subScenario
                    # print(subScenario["hashTree"][1]["whileController"]["timeout"]) # 循环等待时间
                self.handleScenario(subScenario, variables, stepInfo + str(step), isLast and step == len(scenario["hashTree"]), parentScenario=scenario)
                step += 1
            if inserted == False :
                resoureceId = getResourceId(scenario)
                if resoureceId in self.lateInsertDic :
                    inserts = self.lateInsertDic[resoureceId]
                    for insertTuple in inserts :
                        childIndex = insertTuple[0]
                        child = insertTuple[1]
                        hashTree.insert(childIndex, child)
                if resoureceId in self.lateDelDic :
                    dels = self.lateDelDic[resoureceId]
                    for delScenario in dels :
                        hashTree.remove(delScenario)

        elif (stype == 'HTTPSamplerProxy') :
            if (isLast) :
                self.ended = True
            
            idDic = {}
            responseMap = {}
            extractDataList = getExtractList(scenario)
            lateUpdateVars = {}
            for extractData in extractDataList :
                varsDic = getVarsFromExtractData(extractData)
                for key, value in varsDic.items() :
                    genid = self.generateID()
                    lateUpdateVars[value] = genid
                    idDic[key] = genid
                responseMap.update(varsDic)
            self.idDic = idDic
            path = scenario["path"]
            body = getBodyJson(scenario)
            headers = getHeaders(scenario)
            method = getMethod(scenario)
            params = getArguments(scenario)
            request = (path, params, body, headers, method, preMap, responseMap)

            self.handleAPI(scenario, request, variables, stepInfo, parentScenario=parentScenario)
            self.doAfterAPI(scenario, variables, responseMap, idDic)

        elif (stype == 'JSR223Processor') :
            self.handleScript(scenario)
            # vars = getVarsFromScriptData(scenario)
            # if len(vars) > 0 :
            #     self.variables.update(vars)
        elif (stype == 'LoopController') :
            hashTree : list = scenario["hashTree"]
            for subScenario in hashTree :
                self.handleScenario(subScenario, variables, stepInfo + str(step), isLast and step == len(scenario["hashTree"]), parentScenario=scenario)
                step += 1
        else :
            print(stype)
    
    def doAfterAPI(self, scenario, variables, responseMap, idDic) :
        print("doAfterAPI")

    def handleAPI(self, scenario, request, variable = {}, stepInfo = "", parentScenario = None):
        print("handleAPI")
        return False
    
    def handleScript(self, scenario) :
        print("handleScript")
        return False

class StatementScenario (DefalutScenario):  
    def __init__(self, scenarioData):  
        super().__init__(scenarioData)

        self.user = None
        self.curStatement = None

        self.view = None

        self.autoDisabledIds = [STATEMENT_VIEW_UPDATE_NOTIFICATION_GID]
        self.ignoreIds = [PRE_SERVICE_CHECK_GID]
        self.replaceScenarioMap = {}
        self.pipeline = []
        # self.replaceScenarioMap = {STATEMENT_GID:STATEMENT_CHECK_GID, STATEMENT_CHECK_GID:STATEMENT_CHECK_GID}
        # self.mockInsertMap = {"/v1.0/credit/cards/activation" : POMELO_GET_CARD_MOCK_GID,  # 激活卡请求添加mock请求
        #                       "/v1.0/credit/cards/replacement": POMELO_CREATE_CARD_MOCK_GID, # 换卡请求添加mock请求
        #                       "/v1.0/credit/contracts" : POMELO_SIGN_MOCK_GID }# 签约请求添加mock请求
        self.mockInsertMap = {}

        self.requestList = []

    def getRequestList(self) :
        self.handleScenario(self.scenarioJson, self.variables, isLast=True)
        return self.requestList

    def createBaseScenarioTime(self, updateDate) :

        scenario = self.getBaseScenario(CHANGE_DATE_GID)
        updateTime = datetime.combine(updateDate, time(12,00))
    
        s1 = scenario["hashTree"][0]
        timeStr = updateTime.strftime("%Y-%m-%d %H:%M:%S")
        dateStr = updateTime.strftime("%Y%m%d")
        updateBodyJson(s1, {"time" : timeStr})
        scenario["name"] = "系统时间-" + dateStr

        return scenario
    
    def createBatchXXLJobScenario(self, JobId) :
        scenario = self.getBaseScenario(XXL_JOB_TRIGGER_GID)



    def getTimeFromScenario(self, scenario) :
        variables = self.variables
        if scenario["type"] != 'HTTPSamplerProxy' :
            return None
        timeString = getBodyJson(scenario)["time"]
        if ("__timeShift" in timeString) :
            return None
        timeString = checkVariables(timeString, variables)
        if (timeString.startswith("${")) :
            timeString = checkVariables(timeString, variables)
        curTime = datetime.strptime(timeString,  "%Y-%m-%d %H:%M:%S")
        return curTime
        
    def existInScenario(self, scenario, curDate, targetId, targetDate) :
        stype = scenario["type"]
        if stype == "scenario" :
            if targetId == scenario["id"] and targetDate == curDate and checkEnable(scenario) == True:
                return True
            hashTree = scenario["hashTree"]
            if scenario["id"] == CHANGE_DATE_GID :
                changeDate = self.getTimeFromScenario(hashTree[0])
                if (changeDate != None) :
                    return changeDate
            for child in hashTree :
                ret = self.existInScenario(child, curDate, targetId, targetDate)
                if type(ret) == bool :
                    if ret == True :
                        return ret
                else :
                    curDate = ret.date()
        return False
        
    def checkDQData(self, data, ignoreDays = False) :

        assertData = getAssertData(data)
        
        dqDays, dqBucket, dqDueBucket, blockCodes = self.user.getDQInfo()

        status = "BLOCKED" if dqDueBucket > 0 else "ACTIVE"

        for i in range(3) :
            self.disableExpectData(assertData, f"$.data.blockCodes[{i}].blockCode")
            self.disableExpectData(assertData, f"$.data.blockCodes[{i}].blockReason")
        
        for i in range(len(blockCodes)) :
            if (not ignoreDays) or (not blockCodes[i].startswith("D")) :
                self.updateExpectData(assertData, f"$.data.blockCodes[{i}].blockCode", blockCodes[i])

        self.updateExpectData(assertData, "$.data.dqDays", dqDays, 0)
        self.updateExpectData(assertData, "$.data.dqBucket", dqBucket, 0)
        self.updateExpectData(assertData, "$.data.status", status)

        self.disableExpectData(assertData, "$.data.dqDueBucket")

        if ignoreDays :
            self.disableExpectData(assertData, "$.data.dqDays")
            self.disableExpectData(assertData, "$.data.dqBucket")

        return (dqDays, dqDueBucket)
        
    def checkTriggerDQData(self, data) :
        statement = self.user.curStatement
        assertData = getAssertData(data)
        if (statement.cif.getDQBucket() < 0 or statement.getHistoryUnpaidMinimum() <=0 ) :
            message = "task create fail, latest statement payment amount cover min payment amount"
            statusCode = "22850"
            status = "Business error"
            self.disableExpectData(assertData, "$.data")
        else :
            statusCode = "00000"
            status = "Success"
            message = ""
            delExpectData(assertData, "^500$", "regex")

        self.updateExpectData(assertData, "$.message", message, 0)
        self.updateExpectData(assertData, "$.statusCode", statusCode, 0)
        self.updateExpectData(assertData, "$.status", status, 0)

    # 核对账单结果数据
    def checkBillResultData(self, statement:Statement, data) :
        assertData = getAssertData(data)

        bill:StoriBill = statement.bill
        dueDate = bill.dueDate.strftime("%Y%m%d")
        statementDate = bill.statementDate.strftime("%Y%m%d")
        graceDate = bill.graceDate.strftime("%Y%m%d")
        billingCycle = bill.startDate.strftime("%Y%m%d") + "-" + bill.endDate.strftime("%Y%m%d")
        minPayment = round_to_even(bill.minimumPayment * 100, 0)
        newBalance = round_to_even(bill.newBalance * 100, 0)
        previousBalance = round_to_even(bill.previousBalance * 100, 0)
        
        # cat = 

        # self.updateExpectData(assertData, "$.data.cat", cat)

        self.updateExpectData(assertData, "$.status", "Success")
        # self.updateExpectData(assertData, "$.data.status", status)
        self.updateExpectData(assertData, "$.data.dueDate", dueDate)
        self.updateExpectData(assertData, "$.data.statementDate", statementDate)
        self.updateExpectData(assertData, "$.data.graceDate", graceDate)
        self.updateExpectData(assertData, "$.data.billingCycle", billingCycle)
        self.updateExpectData(assertData, "$.data.minPayment.amountInMnrUnits", minPayment, 0)
        self.updateExpectData(assertData, "$.data.newBalance.amountInMnrUnits", newBalance, 0)
        # self.updateExpectData(assertData, "$.data.graceDateUnpaidMiniAmount.amountInMnrUnits", graceDateUnpaidMiniAmount, 0)
        # self.updateExpectData(assertData, "$.data.dueDateUnpaidMiniAmount.amountInMnrUnits", dueDateUnpaidMiniAmount, 0)
        if (statement.lastStatement != None) :
            self.updateExpectData(assertData, "$.data.previousBalance.amountInMnrUnits", previousBalance, 0)

    def handleBillProcessData(self, scenario) :
        path = scenario["path"]
        if (path == "/backoffice/dfl/credit/statement/processDetail") :
            self.checkBillProcessData(self.user.getLastBillStatement(), scenario)
        elif (path == "backoffice/dfl/credit/activity/unsettledList") :
            print("to do")

    # 核对账单过程数据
    def checkBillProcessData(self, statement:Statement, data) :
    
        assertData = getAssertData(data)

        bill:StoriBill = statement.bill
        vat = round_to_even(bill.minimumDic[TradingType.VAT_FEE] + bill.minimumDic[TradingType.VAT_INT])
        interest = bill.minimumDic[TradingType.INT]
        fee = bill.minimumDic[TradingType.FEE]
        insVat = bill.minimumDic[TradingType.INS_VAT_INT]
        insInterest = bill.minimumDic[TradingType.INS_INT]
        insPrincipal = bill.minimumDic[TradingType.INS_PRIN] + bill.minimumDic[TradingType.INS_PRIN_MSI]
        endStatementBalance = bill.getEndBalance()
        totalInterest = bill.totalInterest
        adb = bill.adb
        unpaidMinPayment = round_to_even(bill.historyUnpaidMinimum)
        s1 = bill.s1
        s2 = bill.s2
        s3 = bill.s3
        calculateResult = bill.minimumPayment
        accountDQ = bill.accountDQ
        adb0 = bill.adbList[0]

        # 删除没有用的字段
        delExpectData(assertData, "$.data.minPayment.principal")
        
        self.updateExpectData(assertData, "$.status", "Success")
        self.updateExpectData(assertData, "$.data.minPayment.accountDQ", accountDQ)
        self.updateExpectData(assertData, "$.data.minPayment.vat", vat)
        self.updateExpectData(assertData, "$.data.minPayment.interest", interest)
        self.updateExpectData(assertData, "$.data.minPayment.fee", fee)
    
        self.updateExpectData(assertData, "$.data.minPayment.insVat", insVat)
        self.updateExpectData(assertData, "$.data.minPayment.insInterest", insInterest)
        # self.updateExpectData(assertData, "$.data.minPayment.insPrincipal", insPrincipal)
        delExpectData(assertData, "$.data.minPayment.insPrincipal")
        self.updateExpectData(assertData, "$.data.minPayment.endStatementBalance", endStatementBalance)
        
        self.updateExpectData(assertData, "$.data.minPayment.unpaidMinPayment", unpaidMinPayment)


        self.updateExpectData(assertData, "$.data.minPayment.calculateResultOne",s1)
        self.updateExpectData(assertData, "$.data.minPayment.calculateResultTwo",s2)
        self.updateExpectData(assertData, "$.data.minPayment.calculateResultThree",s3)
        self.updateExpectData(assertData, "$.data.minPayment.calculateResult", calculateResult)

        if totalInterest > 0 :
            self.updateExpectData(assertData, "$.data.interestCalculation.totalInterest", totalInterest)
            self.updateExpectData(assertData, "$.data.interestCalculation.adb", adb)
            self.updateExpectData(assertData, "$.data.adbCalculationList[0].initialBalance", adb0.originBalance)
            self.updateExpectData(assertData, "$.data.adbCalculationList[0].purchaseOrFee", adb0.positive)
            self.updateExpectData(assertData, "$.data.adbCalculationList[0].payment", -adb0.negative)
            self.updateExpectData(assertData, "$.data.adbCalculationList[0].endBalance", adb0.endBalance)
        else :
            self.disableExpectData(assertData, "$.data.interestCalculation.totalInterest")
            self.disableExpectData(assertData, "$.data.interestCalculation.adb")
            self.disableExpectData(assertData, "$.data.adbCalculationList[0].initialBalance")
            self.disableExpectData(assertData, "$.data.adbCalculationList[0].purchaseOrFee")
            self.disableExpectData(assertData, "$.data.adbCalculationList[0].payment")
            self.disableExpectData(assertData, "$.data.adbCalculationList[0].endBalance")
    
    def checkCreditLimit(self, scenario, variables) :
        print("额度查询")
        assertData = getAssertData(scenario)

        limit, available = self.user.getLimitInfo()

        self.updateExpectData(assertData, "$.data.limit", limit, 0)
        self.updateExpectData(assertData, "$.data.available", available, 0)
    
    def checkTransactionsDetail(self, scenario, variables) :
        print("交易详情查询")
    
    def checkTransactions(self, scenario, variables) :
        print("交易查询")

    def checkInstallmentConsultData(self, scenario, variables) :
        print("分期咨询")
        assertData = getAssertData(scenario)
        jsonObject = getBodyJson(scenario)
        principal = jsonObject["principal"]
        principal = checkVariables(principal, variables)
        insList = Installment.consult(principal)
        variables["${insList}"] = list(map(lambda x:x.data , insList))
        for i in range(len(insList)) :
            formattedMpr = insList[i].formattedMpr
            periods = insList[i].periods
            totalAmount =   insList[i].totalAmount
            checkStringBase = "$.data[" + str(i) + "]."
            self.checkExpectData(assertData, checkStringBase+"totalAmount", totalAmount, 0)
            self.checkExpectData(assertData, checkStringBase+"periods", periods, 0)
            self.checkExpectData(assertData, checkStringBase+"formattedMpr", formattedMpr)

    def handleSign(self, scenario, variables) :
        print("签约")

        data = getBodyJson(scenario)
        contractInfo = data["product"]
        contractInfo = checkVariables(contractInfo, variables)
        data["product"] = contractInfo
        
        cardId = self.idDic["$.data.card.id"]
        accountId = self.idDic["$.data.account.id"]

        cif = StoriCif(contractInfo, cardId)
        self.user = StoriUser(accountId, cif, self.systime)
        self.user.userName = self.name

        self.curStatement = self.user.curStatement
    
    def handleChangeCard(self, scenario, variables) :
        if (self.user != None) :
            cardId = self.idDic["$.data.id"]
            data = getBodyJson(scenario)
            self.user.exchangeCard(data=data, cardId=cardId)

    def handleBilling(self, scenario) :

        self.user.genBill()
        self.curStatement = self.user.curStatement

    def handlePomeloTrading(self, scenario, variables = {}) :

        if (self.user == None) :
            return

        path = scenario["path"]
        data = getBodyJson(scenario).copy()

        self.user.tradingPomeloRequestData(path, data, variables)

    def handleAdjustmentTrading(self, scenario, variables = {}) :
        data = getBodyJson(scenario)

        self.user.tradingAdjRequestData(data)

    def handleAppTrading(self, scenario, variables = {}) :
        path = scenario["path"]
        data = getBodyJson(scenario).copy()

        if '$.data.txnId' in self.idDic :
            tid = self.idDic['$.data.txnId']
        else :
            tid = None

        txnTime = self.systime
        # txnTime = self.curStatement.curTime
        utcTime = getUTCDateTime(txnTime)
        timeStr = getISO8601UTCTimeStr(utcTime)
        # timeStr = txnTime.strftime("%Y-%m-%dT%H:%M:%S.619Z")
        data['txnBizDetail']["txnTime"] = timeStr
        updateBodyJson(scenario, data)

        self.user.tradingAppRequestData(path, data, variables, tid)

    # 插入DQ通知
    def checkInsertDQTrigger(self, scenario, curTime) :
        if self.curStatement.lackOfDQTrigger(curTime.date()) :
            dqTriggerDate = self.curStatement.lastStatement.bill.DQTriggerDay
            if not self.existInScenario(self.scenarioJson, datetime.now().date(), DQ_NOTIFICATION_GID, dqTriggerDate) :
                print("添加一条DQ通知", dqTriggerDate)
                lateInsertList = []
                if self.systime.date() != dqTriggerDate :
                    timeScenario = self.createBaseScenarioTime(dqTriggerDate)
                    lateInsertList.append(timeScenario)

                DQScenario = self.getBaseScenario(DQ_NOTIFICATION_GID)
                lateInsertList.append(DQScenario)
                self.lateInsertScenario(lateInsertList, scenario)
                for insertScenario in lateInsertList :
                    self.handleScenario(insertScenario, inserted=True)
                return True

                # gNeedCheckedCases.append(self.name + "-" +  str(self.curStatement.bill.number))
        return False

    def handleChangeDate(self, scenario, request, variables, stepInfo, parentScenario) : #修改时间
        timeString = getBodyJson(scenario)["time"]
        if ("__timeShift" in timeString) :
            return
        timeString = checkVariables(timeString, variables)
        if (timeString.startswith("${")) :
            timeString = checkVariables(timeString, variables)
        curTime = datetime.strptime(timeString,  "%Y-%m-%d %H:%M:%S")
        if (self.user != None) :
            insertDQ = self.checkInsertDQTrigger(scenario, curTime)
            insertStmt = self.checkInsertStatement(scenario, curTime)
            if insertDQ or insertStmt:
                self.handleAPI(scenario, request, variables, stepInfo, parentScenario)
            else :
                self.systime = curTime
                self.user.changeTime(curTime)
        else :
            self.systime = curTime

    def handleInstallmentTrading(self, scenario, variables) : # 分期
        if (self.user == None) :
            return
        path = scenario["path"]
        data = getBodyJson(scenario)
        data = checkVariables(data, variables)
        if type(data) == int :
            data = self.variables["${insList}"][data]
            data["accountId"] = "${accountId}"
            data["referenceId"] = "${referenceId}"
            data["requestId"] = "${referenceId}"
        if "$.data.installmentId" in self.idDic :
            installmentId = self.idDic["$.data.installmentId"]
            data["installmentId"] = installmentId
        data = checkVariables(data, variables)
        self.user.tradingInsRequestData(data, variables)

    def handleXXLJob(self, scenario, variables) : # 
        jsonObject = getBodyJson(scenario)
        jobID = None
        executorParam = None
        for object in jsonObject :
            if (object["name"] == "id") :
                jobID = object["value"]
                break
            if (object["name"] == "executorParam") :
                executorParam = object["value"]
        if jobID == None :
            return
        if jobID == "${Job_Task_Benefit_Expired_Process}" :
            self.user.curStatement.handleMarketingExpiredBenefit()
        elif jobID == "${xxl_task_id_dq_status_update_process}" :
            self.user.updateDQ()
        elif jobID == "${xxl_task_id_refund_cancel_process}" :
            if "${installment_id}" in self.variables :
                insId = self.variables["${installment_id}"]
            self.user.cancelInsMannul(insId=insId)
        elif jobID == "${xxl_task_id_dq_cancel_process}" :
            self.user.cancelInsMannul()
        elif jobID == "${xxl_task_id_posted}" :
            self.user.adjustInsPostDate()

    def handleMarketing(self, scenario, variables) :
        path = scenario["path"]
        if (path == "/v1.0/credit/marketing/benefits") :
            print("权益查询")
            benefit = self.user.cif.freeIntBenefit()
            status = benefit["status"]
            assertData = getAssertData(scenario)
            self.updateExpectData(assertData, "$.data.benefits[0].status", status)
        else :
            data = getBodyJson(scenario)
            self.user.handleMarketingRequestData(path, data, variables)
    
    def updateViews(self) :
        view = self.getView()
        desp = view.getDescription()
        self.data["description"] = desp
        # self.data["tags"] = []

    def checkInsertStatement(self, scenario, curTime = None) :
        if self.curStatement== None or self.curStatement.isBilled :
            return False
        statementDate = self.curStatement.bill.statementDate
        if (curTime and curTime.date() <= statementDate) :
            return False
        ended = self.ended
        if ended :
            self.ended = False
        self.checkInsertDQTrigger(scenario, datetime.combine(statementDate, time(12,00)))

        print("添加一条出账", statementDate)
        lateInsertList = []
        if self.systime.date() != statementDate :
            timeScenario = self.createBaseScenarioTime(statementDate)
            lateInsertList.append(timeScenario)
        statementScenario = self.getBaseScenario(STATEMENT_CHECK_GID)
        lateInsertList.append(statementScenario)
        self.lateInsertScenario(lateInsertList, scenario)
        for insertScenario in lateInsertList :
            self.handleScenario(insertScenario, inserted=True)

        self.ended = ended

        return True
    
    def checkInsScript(self, script) :
        if "vars.putObject(\"ins_data\",getInsCalData)" in script :
            pattern = r'data\.get\((\d+)\)'
            match = re.search(pattern, script)
            if match:
                number = int(match.group(1))
                self.variables["${ins_data}"] = number
            return True
        return False
            
    def handleScript(self, scenario) :
        if "script" in scenario :
            script = scenario["script"]
            if not self.checkInsScript(script) :
                varsDic = getVarsFromScriptData(scenario)
                if len(varsDic) > 0 :
                    for key, value in varsDic.items() :
                        if "__metersphere_env_id" in key :
                            continue
                        if value == "${__UUID}" :
                            value = self.generateID()
                        # assert(value != "${__UUID}")
                        self.variables[key] = value
        return False

    def doAfterAPI(self, scenario, variables, responseMap, idDic) :
        # print("doAfterAPI")

        dataList = getExtractScriptList(scenario)
        for scriptData in dataList :
            self.handleScript(scriptData)

        for key, value in responseMap.items() :
            self.variables[value] = idDic[key]
        
        path = scenario["path"]
        if not self.user :
            return
        if (path == "/v1.0/credit/installments/installable") :
            pattern = r'\[(\d+)\]'
            for key, value in responseMap.items() :
                self.variables[value] = idDic[key]
                if value == "${referenceId}" :
                    match = re.search(pattern, key)
                    if match:
                        number = int(match.group(1))
                        trading = self.user.findCanInstallmentTrading(number)
                        if trading :
                            tid = self.user.findCanInstallmentTrading(number).tid
                            self.variables[value] = tid
                elif value == "${amount}" :
                    match = re.search(pattern, key)
                    if match:
                        number = int(match.group(1))
                        trading = self.user.findCanInstallmentTrading(number)
                        if trading :
                            amount = round_to_even(self.user.findCanInstallmentTrading(number).leftAmount * 100, 0)
                            self.variables[value] = amount
                    
    def handleAPI(self, scenario, request, variables = {},stepInfo = "", parentScenario = None):
        sid = scenario['id']
        # name = scenario['name']
        # print(name)
        
        if self.ended :
            if self.curStatement and not self.curStatement.isBilled :
                if self.systime.date() == self.curStatement.bill.startDate :
                    self.curStatement = self.user.getLastBillStatement()
                else :
                    self.checkInsertStatement(scenario)
                    # self.curStatement.label.autoMarkUnions()

        self.printStepInfo(scenario, stepInfo)

        if (self.systime == None) :
            self.systime = datetime.now()

        if self.systime :
            timeStr = self.systime.strftime("%Y-%m-%d %H:%M:%S")
            dateStr = self.systime.strftime("%Y%m%d")

        path = request[0]

        if path not in ["/api/admin/system/faketime",
                        "/api/credit/currentSystemTime"] :
            pid = len(self.requestList)
            if len(self.requestList) == 0 :
                vars = self.variables
            else :
                vars = variablesFromScenario(scenario)

            self.requestList.append((pid, self.name, timeStr, vars) + request)

        # 修改时间 /api/admin/system/faketime
        if (sid == CHANGE_DATE_SID) :
            if "name" in parentScenario and "权益过期时间" in parentScenario["name"] :
                return True
            self.handleChangeDate(scenario, request, variables, stepInfo, parentScenario)
        # 查询系统时间
        elif (sid == "9862d874-bd3e-4b3b-8b7d-583776263709") :
            assertData = getAssertData(scenario)
            self.updateExpectData(assertData, "$.data.currentSystemTime", dateStr, needCheck=False, option='CONTAINS')
        # 签约 /v1.0/credit/contracts
        elif (sid == SIGN_SID) :
            self.handleSign(scenario, variables)
        elif (sid == ACTIVE_CARD_SID) :
            data = getBodyJson(scenario)
            cardId = checkVariables(data["id"],variables)
            self.user.activeCard({"cardId":cardId})
        # 换卡 /v1.0/credit/cards/replacement
        elif (sid == CHANGE_CARD_SID) :
            self.handleChangeCard(scenario, variables)
        # 出账 /backoffice/dfl/credit/statement/create
        elif (path == StoriPath.StatementCreate) :
            self.handleBilling(scenario)
            if parentScenario["id"] == STATEMENT_CHECK_GID :
                parentScenario["name"] = "出账-" + dateStr
            
        # 查询最新已出账单 /backoffice/dfl/credit/statement/settled
        elif (sid == CHECK_LATEST_BILL_SID) :
            print("查询最新已出账单")
            if parentScenario["type"] == "LoopController" :
                parentScenario["whileController"]["value"] =  dateStr
                parentScenario["whileController"]["timeout"] = 30000
                print(parentScenario["whileController"]["value"])
            else :
                self.checkBillResultData(self.user.getLastBillStatement(), scenario)
        # 查询账单过程数据 /backoffice/dfl/credit/statement/processDetail
        elif (sid == CHECK_BILL_PROCESS_SID) :
            self.handleBillProcessData(scenario)
        # Pomelo交易
        elif (sid in POMELO_TRADING_SID_LIST) :
            self.handlePomeloTrading(scenario, variables)
        # APP交易
        elif (sid in APP_TRADING_SID_LIST) :
            self.handleAppTrading(scenario, variables)
        elif path =='/backoffice/dfl-ng/credit/adjustment' :
            self.handleAdjustmentTrading(scenario, variables)
        elif (sid == "51bdeb0e-893b-3583-24e8-00208a05c027") :
            self.handleAdjustmentTrading(scenario, variables)
        # 分期交易
        elif (sid == "b0fe042d-36f8-fd14-8031-d847d8c9e624") :
            self.handleInstallmentTrading(scenario, variables)
        # DQ触发
        elif (path == StoriPath.DQCreate) :
            self.user.createDQ()
            self.checkTriggerDQData( scenario)
        # DQ 天数更新
        elif (path == StoriPath.DQUpdate) :
            self.user.updateDQ()
        # 用户查询 /v1.0/credit/accounts/{accountId}
        elif (sid == "c4fd283d-11b4-4555-aeb9-8156e20564b6") :
            # DQ通知非首次DQ
            # 只有首次DQ时DQ通知才更新DQ天数，非首次DQ不更新DQ天数，只更新DQ Due Bucket
            if parentScenario["id"] == DQ_NOTIFICATION_GID and self.user.cif.DQDays != 1:
                result = self.checkDQData(scenario, ignoreDays=True)
            else :
                result = self.checkDQData(scenario)
            
            dqDays, dqDueBucket = result
            if parentScenario["id"] == DQ_NOTIFICATION_GID :
                parentScenario["name"] = "账单通知DQ-" + ("首次" if dqDays == 1 else "DueBucket:" + str(dqDueBucket))
            elif parentScenario["id"] == DQ_DAYS_UPDATE_GID :
                parentScenario["name"] = "DQ天数更新查询-" + "天数:" + str(dqDays) + ",DueBucket:" + str(dqDueBucket)
            else :
                scenario["name"] = "用户查询-DQ天数：" + str(dqDays) + ",DueBucket:" + str(dqDueBucket)

            # 检查DQ通知是否缺失
            if parentScenario["id"] == DQ_NOTIFICATION_GID and parentScenario["hashTree"][0]["path"] != "/backoffice/dfl/credit/dqTask/create" :
                assert(0)
        # 账单查询
        elif (sid == "8b34b333-59ec-4ff1-8d15-ad148c69161e") :
            print("账单查询")
        # 分期咨询
        # elif (sid == "c74fa01e-e01f-6db2-e49e-2571b4d7f214") :
        elif (path == "/v1.0/credit/installments/consult") :
            self.checkInstallmentConsultData(scenario, variables)
        # 交易详情查询 /v1.0/credit/transaction/detail
        elif (sid == "dd1d38b5-c045-cc5b-b7f9-9af3a5d9a84a") :
            self.checkTransactionsDetail(scenario, variables)
        # 交易查询 /v1.0/credit/transactions
        elif (sid == "ea50d022-e3b0-4ed7-be40-b0ad6b2376a9") :
            self.checkTransactions(scenario, variables)
        # 营销
        elif (sid == "e6797a5e-bc4f-4558-a145-b62d270cb09b" 
              or sid == "459e77dc-36bc-4518-9c7a-e0abe6ff68cb"
               or sid == "053c85b4-ac22-4f35-bdd2-7b5db34d4eb9") :
            self.handleMarketing(scenario, variables)
        # 查询额度
        elif (sid == "c8a05dfa-b9fd-4c91-bfe7-a0273bc6fd54") :
            self.checkCreditLimit(scenario, variables)
        elif (sid == "86ccaff2-1076-c527-5d73-c3a73e1e2ed6") :
            self.handleXXLJob(scenario, variables)
        elif (sid in OTHER_SID_LIST) :
            # 462f4677-a6c9-4453-95ac-d057c2da5d96:4.查询未出账单 
            # 61721c54-2d04-fc49-d720-66d76e3353a9:2.激活卡
            # 9862d874-bd3e-4b3b-8b7d-583776263709:查询系统时间
            # 19435b3f-2863-48d1-b2c5-40aff2dfd626:用户添加合约
            # a72c15b3-3f31-442e-9971-d0f271034d26:04.激活卡
            # 2c68a001-f148-432c-8d72-29ea0f7e5296:注册账号
            # 10b1a835-11ae-4059-a800-8f4e02a3bdaf:获取账号信息
            # c0e6a4e7-3625-4881-b742-5327a078fb23:获取用户合约
            # c12f36c0-a996-4452-97a7-448870cbc783:查询最新的明细
            # dd1d38b5-c045-cc5b-b7f9-9af3a5d9a84a:交易详情查询
            # 5b5a7eb4-9864-3490-245e-759b9a6724c2:DQ天数更新任务生成
            # 86ccaff2-1076-c527-5d73-c3a73e1e2ed6:xxljob trigger
            # ea50d022-e3b0-4ed7-be40-b0ad6b2376a9:交易查询
            # dd6d635e-d8c7-361b-c6f6-ceffe16d14e9:可分期单查询
            # d2e57bf3-6546-49d0-bd79-ea84fc62c3ae:Update card status & customer block
            # 1553ddd1-755c-5320-225f-166118c4ad2b:4）xxljob -集群任务-任务拆分-出账-Credit
            # c11fb186-f84b-4689-96d1-8dca0b0ebae2:新增人群用户
            # 1d2903b6-6a34-4ada-907d-ca1b2704eac6:账单列表分期入账
            return False
        else :
            print(sid)
            assert(0)
            return False
        return True
    
    # def getView(self) -> StoriView:
    #     if self.view == None :
    #         if self.user :
    #             self.view = StoriView(self.user)
    #         else :
    #             self.view = None
    #     return self.view

def excuteScenario(file, output = None):

    # 读取文件
    with open(file, 'r') as f:
        fileData = json.load(f)

    # fileData
    # dict_keys(['projectId', 'version', 'data', 'nodeTree'])
    # data (list)
    # dict_keys(['id', 'projectId', 'tags', 'userId', 'apiScenarioModuleId', 'modulePath', 'name', 'level', 'status', 'principal', 'stepTotal', 'schedule', 'createTime', 'updateTime', 'passRate', 'lastResult', 'reportId', 'num', 'originalState', 'customNum', 'createUser', 'version', 'deleteTime', 'deleteUserId', 'executeTimes', 'order', 'environmentType', 'environmentGroupId', 'versionId', 'refId', 'latest', 'scenarioDefinition', 'description', 'environmentJson'])
    
    dataList = fileData["data"]
    for data in dataList :
        # if (data["name"] != "第三期用例6.1") :
        #     continue
        # if (data["name"] !="第三期用例3.1") :
        #     continue
        # if (data["name"] == "用户卡block A001") :
        #     continue
        # if (data["name"] == "分期6期") :
        #     continue

        scenarioInstance = StatementScenario(data)
  
        scenarioInstance.readScenario()

        # 更新assert数据
        scenarioInstance.unpdateScenario()

        # 更新view数据
        scenarioInstance.updateViews()


    # # 保存文件
    # if (NewInterestCal) :
    #     if output != None :
    #         outputDir = os.path.split(output)[0]
    #     else :
    #         directory, filename = os.path.split(file)  
    #         name = filename.split(".")[0]
    #         extension = filename.split(".")[1]
    #         outputDir = directory + "/updated/"
    #         output = outputDir + name + "update."+extension

    #     if not os.path.exists(outputDir) :
    #         os.makedirs(outputDir)  
    #     with open(output, 'w', encoding='utf-8') as f:
    #         print(output) 
    #         json.dump(fileData, f, ensure_ascii=False)



