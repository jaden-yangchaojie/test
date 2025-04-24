from StoriUtils import getDicKeypath, currentTimeMillis, getRunTime, round_to_even, loggingExpect
from datetime import datetime, timedelta, timezone
from StoriRequest import retry_decorator, getUrlFromPath, getEnvHeaders, StoriFetch, replaceDicByMap, getTradingInfoFromBody, StoriPostXXLJob
import asyncio
import time
import json
from StoriSQL import StoriSQL
import uuid
import StoriPath
import os
from StoriUser import StoriUser
from StoriCif import StoriCif
from StoriCheck import StoriCheck
import logging

StoriPipelineRetryPathList = [StoriPath.UserRegister, 
                        StoriPath.UserLogin, 
                        StoriPath.UserGetContract, 
                        StoriPath.UserSignContract, 
                        StoriPath.UserAddContract,
                        StoriPath.StatementCreate,
                        StoriPath.UserActivateCard,
                        StoriPath.UserReplaceCard
                        ]

StoriPipelineSkipPathList = [
    StoriPath.StatementUnsettled,
    "/backoffice/dfl/credit/statement/settled",
        "/backoffice/dfl/credit/statement/processDetail",
        "/v1.0/credit/transactions",
        "/v1.0/credit/transaction/detail",
        "/v1.0/credit/accounts/{accountId}",
        ]

StoriPipelineTradingPathList = [# app
                                StoriPath.AppTradingAuth,
                                StoriPath.AppTradingPayment,
                                StoriPath.AppTradingPosting,
                                # pomelo
                                StoriPath.PomeloTradingAuth,
                                StoriPath.PomeloTradingPosting,
                                StoriPath.PomeloTradingNotify,
                                StoriPath.PomeloTradingDebit,
                                StoriPath.PomeloTradingCredit,
                                  # adj
                                StoriPath.AdjTrading, 
                                  ]

StoriPipelineTimeInterval = 5
# StoriPipelineTimeInterval = 0

StoriPipelineExportFolder = "export/autotest"
StoriBatchMode = False

class StoriPipeLine:
    def __init__(self):  
        self.userEnv = {} # 保存环境变量
        self.userErrorResult = {} # 保持运行结果
        self.userContext = {} # 保存用户上下文环境
        self.sql = StoriSQL()
        self.contractLock = asyncio.Lock() # 签约加锁，签约接口不支持并发
        self.statementLock = asyncio.Lock() # 出账加锁，出账接口不支持并发
        self.benefitLock = asyncio.Lock() # 权益发放锁，测试用例人群都是一个，不能并发，并发会导致权益发错
        self.benefitLockUser = None
        self.errorFileHandle = None
        self.envFileHandle = None
        self.finishFileHanle = None
        self.fileLock = asyncio.Lock() 
        self.pipelineId = None
        self.resultId = None
        self.userCheck = {}
        self.userDBData = {}

        self.requestDetail = [] # 保存请求明细

        self.logger = logging.getLogger('pipeline')
        self.logger.setLevel(logging.DEBUG)

    def __del__(self):
        self.saveAndCloseFiles()
    
    def saveAndCloseFiles(self) :
        # 保存执行结果
        if self.errorFileHandle :
            json.dump(self.userErrorResult, self.errorFileHandle, ensure_ascii=False, indent=4)
            self.errorFileHandle.close()
            self.errorFileHandle = None
        if self.envFileHandle :
            json.dump(self.userEnv, self.envFileHandle, ensure_ascii=False, indent=4)
            self.envFileHandle.close()
            self.envFileHandle = None
        if self.finishFileHanle :
            self.finishFileHanle.close()
            self.finishFileHanle = None

        filename = f"{self.folder}/pipeline_lastExcute.json"
        with open(filename, 'w') as file:
            json.dump({"pipelineId":self.pipelineId, "resultId":self.resultId}, file, ensure_ascii=False, indent=4)
        filename = f"{self.folder}/pipeline_requestdetail.json"
        with open(filename, 'w') as file:
            json.dump(self.requestDetail, file, ensure_ascii=False, indent=4)

    def build(self, toPipeLineList) :
        requestPipeLine = {}
        if StoriBatchMode :
            statementMap = {}
            dqMap = {}

        for pipe in toPipeLineList :
            path = pipe[4]
            if path in StoriPipelineSkipPathList :
                continue

            user = pipe[1]
            timeStr = pipe[2]
            curDateStr = timeStr[:10]
            if not curDateStr in requestPipeLine :
                requestPipeLine[curDateStr] = [[],{},[]] # pre, useraction, after
                preList:list = requestPipeLine[curDateStr][0]
                pid = len(preList)
                preList.append(self.genChangeTime(pid, timeStr))

            if not user in self.userErrorResult :
                self.userErrorResult[user] = []
            if not user in self.userContext :
                self.userContext[user] = {"totalRequest":0, "terminate" : False}

            if not user in self.userDBData :
                self.userDBData[user] = {"statement":[]}
            self.userContext[user]["sucessRequest"] = 0
            self.userContext[user]["failedRequest"] = 0

            if StoriBatchMode == True :
                if path == StoriPath.StatementCreate :
                    dataStr = timeStr[:10]
                    if dataStr not in statementMap :
                        statementMap[dataStr] = {user}
                        afterList:list = requestPipeLine[curDateStr][2]
                        pid = len(afterList)
                        taskList = self.genCreateStatementTaskList(pid, timeStr)
                        afterList.extend(taskList)
                    else :
                        statementMap[dataStr].append(user)
                    continue
            
            userActions = requestPipeLine[curDateStr][1]
            if not user in userActions :
                userActions[user] = []
            actions:list = userActions[user]
            actions.append(pipe)
            self.userContext[user]["totalRequest"] += 1


        return requestPipeLine
    
    def savePipeline(self, pipeline) :
        # 保存pipeline
        time_str = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
        self.pipelineId = time_str
        folder = self.folder if self.folder else StoriPipelineExportFolder 
        filename = f"{folder}/pipeline_{time_str}.json"
        with open(filename, 'w') as file:
            json.dump(pipeline, file, ensure_ascii=False, indent=4)
    
    def check(self, userResult) :
        if userResult == None :
            return
        checkIds = []
        localCalResults = {}
        dbData = {}
        for key in userResult :
            if key in self.userErrorResult :
                continue
            accountId = self.userEnv[key]["${accountId}"]
            checkIds.append(accountId)
            user:StoriUser = userResult[key]
            user.accountId = accountId
            dbData[key] = self.userDBData[key]
            localCalResults[key] = user
        storiCheck = StoriCheck(checkIds, localCalResults, dbData)
        checkErrors = storiCheck.check()
        self.logger.error(checkErrors)

        for user in checkErrors :
            if not user in self.userErrorResult :
                self.userErrorResult[user] = checkErrors[user]
            else :
                errorList:list = self.userErrorResult[user]
                errorList.extend(checkErrors[user])

    # 执行pipeline
    def run(self, toPipeLineList = None, userResult = None, userVars = None) :
        time_str = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
        folder = f"{StoriPipelineExportFolder}/{time_str}"
        self.folder = folder
        if not os.path.exists(folder):
            os.makedirs(folder)

        file_handler = logging.FileHandler(f'{folder}/log.log')
        console_handler = logging.StreamHandler()
        file_handler.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        if toPipeLineList == None :
            filename = f"{folder}/pipeline_lastExcute.json"
            with open(filename, 'r') as file:
                data = json.load(file)
                pipelineId = data["pipelineId"]
            
            filename = f"{folder}/pipeline_{pipelineId}.json"
            with open(filename, 'r', encoding='utf-8') as file:
                toPipeLineList:list = json.load(file)
        else :
            toPipeLineList = sorted(toPipeLineList, key=lambda x: x[2])
            self.savePipeline(toPipeLineList)
        self.userEnv = userVars
        pipeline = self.build(toPipeLineList)

        try:
            self.asyncRun(pipeline)
            self.check(userResult)
        except Exception as e:
            loggingExpect(self.logger, e)
            self.saveAndCloseFiles()

    # 重新执行失败的pipeline
    def reRun(self, timestamp = None) :
        if timestamp == None :
            lastedDir = None
            for root, dirs, files in os.walk(StoriPipelineExportFolder):
                for dir in dirs:
                    if len(dir) == 17:
                        if lastedDir :
                            lastedDir = max(lastedDir, dir)
                        else :
                            lastedDir = dir
            if lastedDir :
                folder = f"{StoriPipelineExportFolder}/{lastedDir}"
            else :
                self.logger.error("no rerun pipeline")
                return
        else :
            folder = f"{StoriPipelineExportFolder}/{timestamp}"
        self.folder = folder
        
        filename = f"{folder}/pipeline_lastExcute.json"
        with open(filename, 'r') as file:
            data = json.load(file)
            pipelineId = data["pipelineId"]
            resultId = data["resultId"]
            self.pipelineId = pipelineId
        
        filename = f"{folder}/erorr_{resultId}.json"
        with open(filename, 'r', encoding='utf-8') as file:
            errorDic:dict = json.load(file)
            if len(errorDic) <= 0 :
                self.logger.debug("all success")
                return
        
        filename = f"{folder}/pipeline_{pipelineId}.json"
        with open(filename, 'r', encoding='utf-8') as file:
            toPipeLineList:list = json.load(file)

        self.userEnv = {}

        # 过滤pipeline
        filterList = []
        for pipe in toPipeLineList :
            user = pipe[1]
            if not user in errorDic :
                continue
            filterList.append(pipe)
        pipeline = self.build(filterList)

        try:
            self.asyncRun(pipeline)
        except Exception as e:
            loggingExpect(self.logger, e)

    # 异步执行pipeline
    @getRunTime
    def asyncRun(self, requestPipeLine) :
        time_str = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
        folder = self.folder

        self.resultId = time_str
        filename = f"{folder}/erorr_{time_str}.json"
        self.errorFileHandle = open(filename, 'w')
        filename = f"{folder}/env_{time_str}.json"
        self.envFileHandle = open(filename, 'w')
        filename = f"{folder}/finish_{time_str}.json"
        self.finishFileHanle = open(filename, 'a', encoding='utf-8')

        # 执行pipeline
        asyncio.run(self.runAllRequestLines(requestPipeLine))

    def genChangeTime(self, pid, timeStr) :
        path = StoriPath.ChangeTime
        body = {"time":timeStr}
        pipe = (pid, "", timeStr, {}, path, {}, body, {"Content-Type":"application/json"}, "POST", {}, {})
        return pipe
    
    def genCreateStatementTaskList(self, pid, timeStr) :
        taskList = []
        # path = StoriPath.XXLJob
        # body = [
        # {"name":"id","value": StoriEnv["xxljobIdPayment"],"contentType":'application/json'},
        # {"name":"executorParam", "value":json.dumps(executorParam),"contentType":'application/json'}
        # ]
        # body = {"time":timeStr}
        # pipe = (pid, "", timeStr, {}, path, {}, body, {"Content-Type":"application/json"}, "POST", {}, {})
        return taskList
    
    async def updateUserLeftRequest(self, user, isSuccess = True) :
        if not user in self.userContext:
            return
        success = self.userContext[user]["sucessRequest"]
        failed = self.userContext[user]["failedRequest"]
        total = self.userContext[user]["totalRequest"]
        
        if isSuccess :
            success = success + 1
            self.userContext[user]["sucessRequest"] = success
        else :
            failed = failed + 1
            self.userContext[user]["failedRequest"] = failed
        
        self.logger.info(f"{user}, total: {total}, success: {success}, failed: {failed}")
        
        if success + failed >= total :
            if failed == 0 :
                if user in self.userErrorResult:
                    del self.userErrorResult[user]
                async with self.fileLock :
                    env = self.userEnv[user]
                    accountId = env["${accountId}"]
                    self.finishFileHanle.write(user + " " + accountId + "\n")
    
    async def runAllRequestLines(self, requestPipeLine:dict) :
        allDate = requestPipeLine.keys()
        allDate = sorted(allDate)
        dateNum = len(allDate)
        index = 0
        for dateStr in allDate :
            self.logger.info(f"process: {index}/{dateNum}")
            dateActions = requestPipeLine[dateStr]
            for action in dateActions[0] :
                await self.doRequestAction(dateStr, action=action)
            await self.doWait(StoriPipelineTimeInterval)
            await self.doDateActions(dateStr, dateActions[1])
            await self.doWait(StoriPipelineTimeInterval)
            for action in dateActions[2] :
                await self.doRequestAction(dateStr, action=action)
            index += 1
        await self.changeToCurTime()
        await self.sql.safeClose()
    
    async def changeToCurTime(self):
        systime = datetime.now() - timedelta(hours=14)
        timeStr = systime.strftime("%Y-%m-%d %H:%M:%S")
        body = {"time":timeStr}
        url = getUrlFromPath(StoriPath.ChangeTime)
        await StoriFetch(url, body=body)
    
    async def doDateActions(self, dateStr:str, dateActions:dict):
        asyncTasks = []
        for user in dateActions.keys() :
            userActions = dateActions[user]
            asyncTasks.append(self.doUserActions(dateStr, user, userActions))
        await asyncio.gather(*asyncTasks)

    async def doUserActions(self, dateStr:str, user:str, userActions:list):
        try :
            for action in userActions :
                await self.doRequestAction(dateStr, action, user) 
        except Exception as e:
            loggingExpect(self.logger, e)

            self.userContext[user]["terminate"] = True
            errorList:list = self.userErrorResult[user] if user in self.userErrorResult else []
            errorList.append(str(e))
            if self.benefitLockUser == user :
                self.benefitLock.release()

    def getUserSql(self, user) :
        return self.sql

    @retry_decorator(max_retries=10)
    async def doCheckChangeTimeRequest(self, dateStr):
        url = getUrlFromPath(StoriPath.QueryTime)
        timestamp = int(time.time() * 1000)
        response = await StoriFetch(url, params={"t":timestamp}, method="GET")
        if response["status"] == "Success" :
            if "".join(dateStr.split("-")) in response["data"]["currentSystemTime"] :
                return True
        return False
    
    # 开卡费检查
    @retry_decorator(max_retries=10)
    async def doCheckOpenFee(self, user) :
        env = self.userEnv[user]
        accountId = env["${accountId}"]

        sql = self.getUserSql(user)
        data = await sql.queryLastestProcess(accountId, 3)
        if len(data) != 3 :
            return False
        for trading in data :
            sub_type = trading["sub_type"]
            if sub_type != "OPEN_FEE" :
                return False
            if trading["type"] == "ADJUSTMENT":
                request_id = trading["request_id"]
        await self.doPaymentJob(user, accountId, request_id, isOpenAdj=True)
        return True
    
    # 换卡费检查
    @retry_decorator(max_retries=10)
    async def doCheckExchangeFee(self, user) :
        env = self.userEnv[user]
        accountId = env["${accountId}"]

        sql = self.getUserSql(user)
        data = await sql.queryLastestProcess(accountId, 2)
        if len(data) != 2 :
            return False
        for trading in data :
            sub_type = trading["sub_type"]
            if sub_type != "CARD_REPLACEMENT_FEE" :
                return False
        return True
    
    # 出账检查
    @retry_decorator(max_retries=20)
    async def doCheckStatementRequest(self, user, dateStr) :
        env = self.userEnv[user]
        accountId = env["${accountId}"]
        dateStr = "".join(dateStr.split("-"))
        sql = self.getUserSql(user)
        # data = await sql.queryStatementTask(accountId, accountId+"_"+dateStr)
        data = await sql.queryStatement(accountId, limit=1)
        if len(data) > 0 :
            data = data[0]
            statement_dt = data["statement_dt"]
            if statement_dt == dateStr :
                statmentList:list = self.userDBData[user]["statement"]
                statmentList.append(data)
                return True
        return False

    # DQ通知检查
    @retry_decorator(max_retries=10)
    async def doCheckDQNotify(self, user) :
        env = self.userEnv[user]
        accountId = env["${accountId}"]
        sql = self.getUserSql(user)

        data = await sql.queryGeneralTask(accountId, "DELINQUENCY",limit=1)
        if len(data) > 0 :
            data = data[0]
            reference_key:str = data["reference_key"]
            status = data["status"]
            dateStr = self.userContext[user]["lastStatementDate"]
            dateStr = "".join(dateStr.split("-"))
            if reference_key.endswith(dateStr) and status == "SUCCESS":
                return True
        return False

    # DQ更新检查
    @retry_decorator(max_retries=10)
    async def doCheckDQUpdate(self, user, dateStr) :
        env = self.userEnv[user]
        accountId = env["${accountId}"]
        sql = self.getUserSql(user)
        data = await sql.queryGeneralTask(accountId, "DQ_STATUS_UPDATE",limit=1)
        if len(data) > 0 :
            data = data[0]
            reference_key:str = data["reference_key"]
            status = data["status"]
            dateStr = "".join(dateStr.split("-"))
            self.logger.info(reference_key)
            if reference_key.endswith(dateStr) and status == "SUCCESS":
                return True
        return False

    # 还款分配任务检查更新
    @retry_decorator(max_retries=10)
    async def doCheckPaymentTask(self, user, reference_key, needSuccess = False) :
        env = self.userEnv[user]
        accountId = env["${accountId}"]
        sql = self.getUserSql(user)
        data = await sql.queryPaymentTask(accountId, reference_key, limit=1)
        if len(data) > 0 :
            data = data[0]
            status = data["status"]
            self.logger.info(f"payment task status : {status}")
            if data["status"] == "RUNNING" :
                return False
            if needSuccess and data["status"] != "SUCCESS" :
                await StoriPostXXLJob("xxljobIdPayment", accountId)
                return False
            return True
        return False

    # 还款分配检查
    @retry_decorator(max_retries=10)
    async def doCheckPaymentActivity(self, user, reference_key, amt) :
        env = self.userEnv[user]
        accountId = env["${accountId}"]
        sql = self.getUserSql(user)
        data = await sql.queryAccountActivity(accountId, reference_key)
        success = False
        if len(data) > 0 :
            data = data[0]
            handle_status = data["handle_status"]
            pmt_amt = data["pmt_amt"]
            if handle_status == "PMT_FN_NO" :
                success = False
            elif amt != pmt_amt :
                success = False
            else :
                success = True
        if not success :
            await StoriPostXXLJob("xxljobIdPayment", accountId)
        return success
    
    # 交易检查
    @retry_decorator(max_retries=10)
    async def doCheckTradingRequest(self, user, path, body) :
        env = self.userEnv[user]
        accountId = env["${accountId}"]

        sql = self.getUserSql(user)

        data = await sql.queryLastestProcess(accountId, 1)
        if len(data) > 0 :
            data = data[0]
            isPomelo, amount, txnType, local_date_time = getTradingInfoFromBody(body)
            if path in [StoriPath.AppTradingPayment, StoriPath.AppTradingPosting, StoriPath.PomeloTradingPosting]:
                status = 'posted'
            elif path in [StoriPath.AppTradingAuth, StoriPath.PomeloTradingAuth , StoriPath.PomeloTradingDebit]:
                status = 'pending'
            elif path == StoriPath.PomeloTradingCredit and (txnType == 'PAYMENT' or txnType =='REFUND'):
                status = "pending"
            elif path == StoriPath.AdjTrading :
                status == None
            else :
                status = ""

            self.logger.info(f"body {isPomelo} {amount} {txnType} {local_date_time} {status}")
            
            isPomelo0 = data['channel'] == "POMELO"
            txnType0 = data['type']
            if txnType0 == "RE_REFUND" :
                txnType0 = "REFUND"
            # action_type = data['action_type']
            amount0 = int(data['amt'])
            effective_time_local0 = data['transaction_local_time'].to_pydatetime()
            status0 = data['status']
            
            self.logger.info(f"sql {isPomelo0} {amount0} {txnType}0 {effective_time_local0} {status0}")
            request_id = data['request_id']

            checkOK = False
            if status0 == 'canceled' and amount0 == 0 :
                if path == StoriPath.PomeloTradingNotify:
                    checkOK = True
            else :
                if isPomelo0 == isPomelo or amount0 == amount and txnType0 == txnType:
                    if status == status0 :
                        # if (txnType == "PAYMENT" or txnType == "REFUND" or txnType == "ADJUSTMENT") and status == "posted" :
                        #     await self.doPaymentJob(user, accountId, request_id)
                        checkOK = True
                    elif status == "" and status0 in ['pending', 'canceled' , 'rejected']:
                        checkOK = True
            if checkOK :
                self.userContext[user]["lastActivity"] = data
                return True
        return False
    
    @retry_decorator(max_retries=10)
    async def doCheckBenifit(self, user, benefit_name, status) :
        env = self.userEnv[user]
        accountId = env["${accountId}"]
        sql = self.getUserSql(user)
        data = await sql.queryBenefitRecord(accountId)
        for benefit in data :
            if benefit_name == benefit["benefit_name"] and status == benefit["status"]:
                return True
        return False

    async def doWait(self, second, msg = "") :
        self.logger.debug(f"wait {second}s ... {msg}")
        await asyncio.sleep(second)

    async def doRequestAction(self, dateStr, action, user="", retry = 0) :

        pid, user, timeStr, variables, path, params, body, headers, method, preMap, responseMap = action

        if user in self.userContext and self.userContext[user]["terminate"] == True:
            return

        if not user in self.userEnv:
            self.userEnv[user] = {}
        env = self.userEnv[user]
        
        userInstance = None
        accountId = None

        if user in self.userCheck :
            userInstance:StoriUser = self.userCheck[user]
            if "${accountId}" in env :
                accountId = env["${accountId}"]
        if accountId :
            self.logger.info(accountId)

        # 更新环境变量
        utcTime = datetime.strptime(timeStr, '%Y-%m-%d %H:%M:%S') + timedelta(hours=6)
        format_utc = utcTime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'
        preMap["${systemTimestamp}"] = timeStr
        preMap["${systemTimestampUtc}"] = format_utc
        preMap["${timestampUtcIso8601}"] = utcTime.strftime("%Y-%m-%dT%H:%M:%S")
        for key in preMap :
            value = preMap[key]
            if value == "${__UUID}" :
                value = str(uuid.uuid4())
            elif value == "${__userName}" :
                 value = "autotest-" + str(currentTimeMillis())
            if key == '${benefitName}' :
                value = "Interest-free benefit " + datetime.now().strftime('%Y%m%d%H%M%S')
            env[key] = value

        for key in variables :
            if key not in env :
                env[key] = variables[key]
            
        skipPaths = []
        # skipPaths.append(StoriPath.ChangeTime)
        # skipPaths.append(StoriPath.StatementCreate)
        if path in skipPaths :
            await self.updateUserLeftRequest(user)
            return
        url = getUrlFromPath(path)

        # 如果是xxl-job任务
        if path == StoriPath.XXLJob :
            xxlJobName = None
            for data in body :
                if data["name"] == "id" :
                    xxlJobName = data["value"]
                    break

        # 从环境变量更新请求参数
        replaceDicByMap(params, env)
        replaceDicByMap(body, env)

        # print("running path:", path)

        # 请求头参数更新
        headers= getEnvHeaders(headers, body)

        if path == StoriPath.UserSignContract:
            async with self.contractLock :
                response = await StoriFetch(url, headers, body, params)
                await self.doWait(0.3)
        elif path == StoriPath.StatementCreate :
            async with self.statementLock :
                response = await StoriFetch(url, headers, body, params)
                await self.doWait(0.3)
        else :
            if path == StoriPath.MKAddCrowdUser :
                await self.benefitLock.acquire()
                self.benefitLockUser = user
            response = await StoriFetch(url, headers, body, params, method)
        
        errorList:list = self.userErrorResult[user] if user in self.userErrorResult else []

        self.requestDetail.append({"user":user, "url":url, "headers":headers, "body":body, "params":params})

        if response["status"] != "Success" :
            isError = True
            if path in StoriPipelineTradingPathList :
                if "statusCode" in response and response["statusCode"] in ["22757", "22334"] :
                    isError = False 
                elif response["status"] == "REJECTED" :
                    isError = False
            if path == StoriPath.DQCreate :
                if "statusCode" in response and response["statusCode"] in ["22850", "22155", "22757"] :
                    isError = False 
            if isError :
                self.logger.error(f"error: {user} {url}")
                errorResult = {}
                errorResult["pid"] = pid
                errorResult["path"] = path
                errorResult["timeStr"] = timeStr
                errorResult["headers"] = headers
                errorResult["body"] = body
                errorResult["response"] = response
                errorResult["params"] = params
                self.logger.error(json.dumps(errorResult, indent=4, ensure_ascii=False))
                    
                if path in StoriPipelineRetryPathList:
                    retry = retry + 1
                    if retry > 10 :
                        self.userContext[user]["terminate"] = True
                    else :
                        errorResult = None
                        await self.doWait(retry)
                        self.logger.info(f"retry: {retry}")
                        await self.doRequestAction(dateStr, action, user, retry=retry)
                
                if errorResult :
                    errorList.append(errorResult)
                    self.userErrorResult[user] = errorList
                    await self.updateUserLeftRequest(user, isSuccess=False)
            else :
                await self.updateUserLeftRequest(user)
        else :
            if responseMap and env:
                # 从返回值更新环境变量
                self.updateEnvFromResponse(env, response, responseMap)

            checkResult = True
            # 改时间后，时间检查
            if path == StoriPath.ChangeTime:
                await self.doWait(StoriPipelineTimeInterval)
                checkResult = await self.doCheckChangeTimeRequest(dateStr)
                self.logger.info(f"Date Changed: {dateStr}")

                # userInstance改时间
                if userInstance :
                    userInstance.changeTime(datetime.strptime(timeStr, '%Y-%m-%d %H:%M:%S'))
            # 签约后记录签约信息，检查有没有账单数据库开卡交易
            elif path == StoriPath.UserSignContract :
                contract = body["product"]
                self.userContext[user]["contract"] = contract
                if int(contract["params"]["openFee"]) != 0 :
                    await self.doWait(5)
                    checkResult = await self.doCheckOpenFee(user)
                
                # 创建一个userInstance
                cardId = getDicKeypath(response, "data.card.id")
                accountId = getDicKeypath(response, "data.account.id")
                open_date = datetime.strptime(dateStr, '%Y-%m-%d')
                cif = StoriCif(contract, cardId=cardId)
                userInstance = StoriUser(accountId, cif, open_date)
                self.userCheck[user] = userInstance

            elif path == StoriPath.UserReplaceCard :
                reason = body["reason"]
                contract = self.userContext[user]["contract"]
                if int(contract["params"]["cardReplacementFee"]) != 0 and reason in  ["DAMAGE", "PIN_BLOCK", "LOST", "STOLEN", "NON_DELIVERY"]:
                    await self.doWait(3)
                    checkResult = await self.doCheckExchangeFee(user)
                
                # userInstance换卡
                cardId = getDicKeypath(response, "data.id")
                userInstance.exchangeCard(body, cardId)

            # 交易后，检查账单数据库有没有交易记录
            elif path in StoriPipelineTradingPathList :
                checkResult = await self.doCheckTradingRequest(user, path, body)

                # userInstance交易
                if checkResult :
                    tradingData = self.userContext[user]["lastActivity"]
                    if tradingData["type"] in ["PAYMENT", "RE_REFUND", "ADJUSTMENT"] and tradingData["status"] == "posted" :
                        request_id = tradingData['request_id']
                        amt = round_to_even(tradingData["amt"]/100)
                        await self.doPaymentJob(user, accountId, request_id, amt=amt)

                    userInstance.trading(tradingData)
                else :
                    print()

            # 出账后，检查账单数据库有没有账单记录，出账有没有完成
            elif path == StoriPath.StatementCreate :
                await self.doWait(5)
                checkResult = await self.doCheckStatementRequest(user, dateStr)
                self.userContext[user]["lastStatementDate"] = dateStr

                # userInstance出账
                userInstance.genBill()
            # DQ通知后检查任务有没有执行完成
            elif path == StoriPath.DQCreate :
                checkResult = await self.doCheckDQNotify(user)
                userInstance.createDQ()

                await self.doWait(8)
            elif path == StoriPath.DQUpdate :
                if userInstance :
                    userInstance.updateDQ()

                    if userInstance.cif.DQDays > 0 :
                        await self.doWait(5)
                        await self.doCheckDQUpdate(user, dateStr)
            
            elif path == StoriPath.XXLJob :
                if xxlJobName :
                    if "Job_Task_Benefit_Release_Process" in xxlJobName :
                        benefit_name = env["${benefitName}"]
                        await self.doCheckBenifit(user, benefit_name, "UNUSE")
                        self.benefitLock.release()
                    elif "Job_Task_Benefit_Expired_Process" in xxlJobName :
                        benefit_name = env["${benefitName}"]
                        await self.doCheckBenifit(user, benefit_name, "EXPIRED")
            elif path == StoriPath.MKCancelBenefit :
                benefit_name = env["${benefitName}"]
                await self.doCheckBenifit(user, benefit_name, "CANCELED")

            # 记录验证错误
            if checkResult == False :
                errorResult = {}
                errorResult["pid"] = pid
                errorResult["path"] = path
                errorResult["timeStr"] = timeStr
                errorResult["body"] = body
                errorResult["resean"] = "check error"
                if errorResult :
                    errorList.append(errorResult)
                    self.userErrorResult[user] = errorList
            
            if checkResult :
                await self.updateUserLeftRequest(user)
            else :
                await self.updateUserLeftRequest(user, isSuccess=False)
                if path in StoriPipelineRetryPathList:
                    self.userContext[user]["terminate"] = True
            self.logger.info(f"success: {pid} {url}")

    async def doPaymentJob(self, user, accountId, request_id=None, isOpenAdj = False, amt = 0) :
        if request_id != None : # 检查当前accountId payment task没有running状态的时候，再执行job
            await self.doCheckPaymentTask(user, request_id)
        
        await StoriPostXXLJob("xxljobIdPayment", accountId)
        if isOpenAdj :
            return await self.doCheckPaymentTask(user, request_id, needSuccess=True)
        else :
            userInstance:StoriUser = self.userCheck[user]
            balance = userInstance.cif.balance
            if balance > 0:
                await StoriPostXXLJob("xxljobIdPayment", accountId)
                if balance > amt :
                    return await self.doCheckPaymentTask(user, request_id, needSuccess=True)
                else :
                    return await self.doCheckPaymentActivity(user, request_id, round_to_even(balance * 100, 0))

    async def doDQNotifyJob(self, accountId) :
        await StoriPostXXLJob("xxljobIdDQNotify", accountId)
    
    async def doDQUpdateJob(self, accountId) :
        await StoriPostXXLJob("xxljobIdDQUpdate", accountId)

    async def doStatementJob(self, accountId) :
        await StoriPostXXLJob("xxljobIdStatement", accountId)

    def updateEnvFromResponse(self, env, response, responseMap:dict) :
        for key in responseMap.keys() :
            keypath = key.split(".")
            if len(keypath) < 2 :
                continue
            if keypath[0] == "$" :
                data = getDicKeypath(response, keypath[1:])
                if data != None :
                    value = responseMap[key]
                    env[value] = data