import aiohttp
import asyncio
from StoriConfigs import readServerConfigs
from datetime import datetime, timedelta
import uuid
import hmac
import base64
from hashlib import sha256
import json
from StoriUtils import round_to_even
from StoriConfigs import VAT_RATE
from enum import Enum
from functools import wraps
from aiohttp import FormData
import StoriPath
import re

# StoriTestEnv = "qa-test"
StoriTestEnv = "qa"
# StoriTenantEnv = "qa-shadow"
StoriTenantEnv = "qa-regular"

StoriEnv = readServerConfigs(StoriTestEnv, StoriTenantEnv)
StoriHostAPP = StoriEnv["appHost"]
StoriHostXXXJob = StoriEnv["xxljobHost"]
StoriHostCore = StoriEnv["coreHost"]
StoriAppKey = StoriEnv["appKey"]
StoriAppSecret = StoriEnv["api-secret"]
StoriApiKey = StoriEnv["api-key"]
StoriHostBKO = StoriEnv["bkoHost"]
StoriBkoKey = StoriEnv["bkoKey"]
StoriTenantId = StoriEnv["tenantId"]
StoriEntityId = StoriEnv["entityId"]

async def StoriHandleResponse(url:str, response):
    status = response.status
    if status == 200 :
        responseJson = await response.json()
        if url.startswith(StoriHostCore) :
            if "status" in responseJson and responseJson["status"] == "APPROVED":
                responseJson["status"] = "Success"
            elif "status" not in responseJson :
                responseJson["status"] = "Error"
        elif url.startswith(StoriHostAPP) :
            if "success" in responseJson and responseJson["success"] == True:
                responseJson["status"] = "Success"
            elif "status" not in responseJson :
                responseJson["status"] = "Error"
        elif url.startswith(StoriHostXXXJob) :
            if "code" in responseJson and responseJson["code"] == 200 :
                responseJson["status"] = "Success"
            else :
                responseJson["status"] = "Error"
    elif status == 204 and url.startswith(StoriHostCore) :
        responseJson = {"status":"Success", "message":""}
    else :
        try :
            responseJson = await response.json()
            if "status" not in responseJson :
                responseJson["status"] = "Error"
        except :
            responseJson = {"status":"Error", "message":response.reason}
    return responseJson 
            
async def StoriFetch(url:str, headers:dict={}, body={}, params:dict={}, method = 'POST'):
    # headers.update({'Content-Type': 'application/json'})
    async with aiohttp.ClientSession() as session:
        formData = None
        if method == "PUT" :
            doFunc = session.put
        elif method == "GET" :
            doFunc = session.get
        else :
            doFunc = session.post
            if url.startswith(StoriHostXXXJob) and type(body) == list :
                formData = FormData()
                for field in body :
                    formData.add_field(field["name"], field["value"], content_type=field["contentType"])
                body = None
        async with doFunc(url, headers=headers, json=body, params=params, data=formData) as response:
            return await StoriHandleResponse(url, response)

async def StoriPostXXLJob(jobName:str, accountId:str, params:dict = {}):
        
    headers = { "Cookie" : StoriEnv["xxljobCookie"]}
    url =  getUrlFromPath(StoriPath.XXLJob)
    data = getXXLJobParam(jobName)
    if "accountId" in data :
        data["accountId"] = accountId 
    elif "customParams" in data :
        data["customParams"]["accountId"] = accountId  
    for key in params :
        if key in data :
            data[key] = params[key]
    
    jobId = StoriEnv[jobName]
    async with aiohttp.ClientSession() as session:
        formData = FormData()
        formData.add_field('id', jobId, content_type='application/json')
        formData.add_field('executorParam', json.dumps(data), content_type='application/json')
        async with session.post(url, headers=headers, data=formData) as response:
            return await StoriHandleResponse(url, response)
        
def getXXLJobParam(jobName) :
    executorParam = {
        "entityId" : StoriEntityId,
        "tenantId" : StoriTenantId
    }
    if "Batch" in jobName :
        executorParam.update({"customParams": {"maxDid": 7,"maxTid": 0}})
    elif "Job_Credit_Statement_Auto" in jobName :
        executorParam.update({"customParams": {}})
    else :
        executorParam.update({
                      "autoProcess" : True,
                        "accountId" : None,
                          "priority" : None, 
                          "referenceKey" : None,
                            "createTimeLocal" : None, 
                            "createTimeUtc" : None, 
                            "updateTimeLocal" : None, 
                            "updateTimeUtc" : None })
    if jobName == "xxljobIdPayment" :
        executorParam["taskSource"] = "CREDIT_CARD_STATEMENT"
        executorParam["taskType"] = "PAYMENT"
        executorParam["taskProcessStrategyEnum"] = "ACCOUNT_SERIAL"
    elif jobName == "xxljobIdDQNotify" :
        executorParam["taskSource"] = "CREDIT_CARD_STATEMENT"
        executorParam["taskType"] = "DELINQUENCY"
        executorParam["taskProcessStrategyEnum"] = "DEFAULT"
    elif jobName == "xxljobIdDQUpdate" :
        executorParam["taskSource"] = "CREDIT_CARD_CONTROL"
        executorParam["taskType"] = "DQ_STATUS_UPDATE"
        executorParam["taskProcessStrategyEnum"] = "DEFAULT"
    elif jobName == "xxljobIdStatement" :
        executorParam["taskSource"] = "CREDIT_CARD_STATEMENT"
        executorParam["taskType"] = "STATEMENT"
        executorParam["taskProcessStrategyEnum"] = "DEFAULT"
    elif jobName == "xxljobIdBatchPayment" :
        executorParam["taskSource"] = "CREDIT_CARD_STATEMENT"
        executorParam["taskType"] = "PAYMENT_DAILY"
        executorParam["batchMode"] = "day"
    return executorParam

def getSign(timestamp, endpoint, body):
    if type(body) == dict :
        body = json.dumps(body)
    content = f"{timestamp}{endpoint}{body}"
    secret_bytes = base64.b64decode(StoriAppSecret)
    hmac_sha256 = hmac.new(secret_bytes, digestmod=sha256)
    hmac_sha256.update(content.encode('utf-8'))
    bytes = hmac_sha256.digest()
    sign = f"hmac-sha256 {base64.b64encode(bytes).decode('utf-8')}"
    return sign

def getUrlFromPath(path:str) :
    if path.startswith('/backoffice/') or path.startswith("/v1.0/backoffice-ng/") :
        url = StoriHostBKO + path
    elif path.startswith('/api/') or path.startswith('/v1.0/') :
        url = StoriHostAPP + path
    elif path.startswith('/transactions/') :
        url = StoriHostCore + path
    elif path.startswith('/xxl-job-admin/') :
        url = StoriHostXXXJob + path
    else :
        assert(0)
    return url

def getEnvHeaders(headers:dict, body = "") :
    for key in headers.keys() :
        value:str = headers[key]
        if value.startswith("${") and value.endswith("}") :
            value = value[2:-1]
            if value == "__UUID" :
                headers[key] = str(uuid.uuid4())
            elif value == "signature" :
                timestamp = headers["X-Timestamp"]
                endpoint = headers["X-Endpoint"]
                sign = getSign(timestamp, endpoint, body)
                headers[key] = sign
            elif value in StoriEnv :
                value = StoriEnv[value]
                headers[key] = value
            else :
                print(value)
                assert(0)
    return headers

def replace_values(match, replaceMap:dict):
    replace = replaceMap.get(match.group(0), StoriEnv.get(match.group(1), match.group(0)))
    if type(replace)==str and replace.startswith("${") :
        print(replace)
        return ""
    if type(replace) != str :
        replace = str(replace)
    return replace

def replaceDicByMap(d, replaceMap) :
    if replaceMap == None or len(replaceMap) <= 0:
        return None
    if type(d) == dict :
        for key in d :
            ret = replaceDicByMap(d[key], replaceMap)
            if ret != None :
                d[key] = ret
    elif type(d) == list :
        for i in range(len(d)) :
            ret = replaceDicByMap(d[i], replaceMap)
            if ret != None:
                d[i] = ret
    elif type(d) == str:
        if "__UUID" in d : # 换卡接口写错了，应该${__UUID}，写成了{__UUID}}
        # if d == "${__UUID}" :
            return str(uuid.uuid4())

        pattern = r'\$\{(.*?)\}'
        replaced = re.sub(pattern, lambda match: replace_values(match, replaceMap), d)
        return replaced
        # if d in replaceMap :
        #     return replaceMap[d]
        # if d.startswith('${') and d.endswith('}') :
        #     d = d[2:-1]
        #     if d in StoriEnv :
        #         return StoriEnv[d]
        #     else :
        #         print(d)
            # assert(0)
    return None

def getTradingInfoFromBody(body) :
    data = body

    if "event_detail" in body : # pomelo通知
        data = body["event_detail"]
    
    if "amountDetail" in data : # 调整
        data = data["amountDetail"]
        isPomelo = False
        amount = int(data["amount"]["total"])
        txnType = data["type"]
        if txnType ==  "ADJ_FEE" and data["subType"] != "LATE_FEE":
            txnType = "ADJ_VAT" #产生的最后一笔交易是vat
            amount = round_to_even(amount * VAT_RATE, 0)
        local_date_time = ""
    elif "transaction" in data : # pomelo
        isPomelo = True
        transcation = data["transaction"]
        local_date_time = transcation["local_date_time"]
        amount = round_to_even(float(data["amount"]["local"]["total"]) * 100, 0)
        txnType = transcation["type"]
    else : # app
        isPomelo = False
        amount = int(data['txnAmount'])
        txnType = data["txnType"]
        local_date_time = data["txnBizDetail"]["txnTime"]
    return (isPomelo, amount, txnType, local_date_time)

def retry_decorator(max_retries=5):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            nonlocal max_retries
            attempts = 0
            while attempts < max_retries:
                success = await func(*args, **kwargs)
                if success :
                    print(f"Attempt {func.__name__} {attempts} success")
                    return True
                attempts += 1
                print(f"Attempt {func.__name__} {attempts} failed, retrying in {attempts} seconds...")
                await asyncio.sleep(attempts)
            print(f"{func.__name__} failed after {max_retries} retries.")
            return False
        return wrapper
    return decorator

# 生成request
def genRequestData(url:str, body:dict, params:dict={}, headers={}, method = "POST", responseMap ={}) :
    # headers
    headers = getEnvHeaders(headers)
    url = getUrlFromPath(url)
    return {"url":url, "body":body, "params":params, "headers":headers, "method":method, "responseMap": responseMap}

# 发送请求
async def StoriRequest(request):
    method = request["method"]
    url = request["url"]
    headers = request["headers"]
    body = request["body"]
    params = request["params"]
    response = await StoriFetch(url, headers=headers, body=body, params=params, method=method)
    print(response)
    return response

def StoriDoRequest(request) :
    asyncio.run(StoriRequest(request))

# 修改时间请求
def genChangeTimeRequest(timeStr) :
    url = StoriPath.ChangeTime
    if type(timeStr) == datetime :
        timeStr = timeStr.strftime(("%Y-%m-%d %H:%M:%S"))
    body = {"time":timeStr}
    return genRequestData(url, body)

# xxljob任务
def genXXLJobRequest(jobName) :
    executorParam = getXXLJobParam(jobName)
    url = StoriPath.XXLJob
    body = [
        {"name":"id","value": StoriEnv["jobName"],"contentType":'application/json'},
        {"name":"executorParam", "value":json.dumps(executorParam),"contentType":'application/json'}
        ]
    headers={"Cookie":StoriEnv["xxljobCookie"]}
    return genRequestData(url, body, headers=headers)

# dfl注册
def genDflRegisterRequest(loginname) :
    url = StoriPath.UserRegister
    body = {"loginname":loginname,"password":"123"}
    return genRequestData(url, body)

# dfl登录
def genDflLoginRequest(loginname) :
    url = StoriPath.UserLogin
    body = {"loginname":loginname,"password":"123"}
    return genRequestData(url, body, responseMap={'$.data.[0].user_id': '${userId}'})

# 用户信息补充
def genContractRequest() :
    url = StoriPath.UserGetContract
    userId = "${userId}"
    body = {"userId":userId}
    return genRequestData(url, body)

# 签约
def genSignRequest(body) :
    url = StoriPath.UserSignContract
    headers = {"x-api-key":StoriAppKey, "X-Customer-Id":"1111662001020242"}
    userId = "${userId}"
    body["requestId"] = userId
    body["customer"]["referenceCustId"] = userId
    responseMap = {'$.data.account.id': '${accountId}', 
                   '$.data.product.productCode': '${productCode}',
                     '$.data.contract.id': '${contractId}',
                       '$.data.card.id': '${cardId}', 
                       '$.data.customer.id': '${customerId}',
                         '$.data.card.processorCardId': '${pomeloCardId}', 
                         '$.data.customer.processorCustId': '${pomeloUserId}'}
    return genRequestData(url, body, headers=headers, responseMap=responseMap)

# 添加合约
def genAddContracRequest() :
    url = StoriPath.UserAddContract
    body = {
        "customer_id": "${customerId}",
        "contract_id": "${contractId}",
        "account_id": "${accountId}",
        "card_id": "${cardId}",
        "product_code": "${productCode}",
        "user_id": "${userId}"
    }
    return genRequestData(url, body)

# 出账
def genBillRequest(accountId) :
    url = StoriPath.StatementCreate
    headers = {"x-api-key":StoriBkoKey}
    body = {"accountId": accountId}
    return genRequestData(url, body=body, headers=headers)

# # pomelo交易
# def genPomeloTradingRequest(path, body) :
#     url = StoriHostCore + path
#     headers = {"x-idempotency-key":"${__UUID}",
#                "X-Api-Key":StoriApiKey,
#                "X-Signature":"${signature}",
#                "X-Timestamp":1678967946,
#                "X-Endpoint":path}
#     return genRequestData(url, body, headers)

# # app交易
# def genAppTradingRequest(path, body) :
#     url = StoriHostAPP + path
#     headers = {"x-api-key":StoriAppKey}
#     body["apiKey"] = StoriAppKey
#     return genRequestData(url, body, headers)

# 激活卡
def genActiveCardRequest() :
    url = StoriPath.UserActivateCard
    headers = {"x-api-key":StoriAppKey}
    body = {
        "id": "${cardId}"
    }
    return genRequestData(url, body, headers)

# 换卡
def genExchangeCardRequest(body) :
    url = StoriPath.UserReplaceCard
    headers = {"x-api-key":StoriAppKey}
    return genRequestData(url, body, headers)

# sign = getSign("1678967946", "/transactions/v1/notifications", "test")
# print("sign")
# print(sign)

# print(str(uuid.uuid4()))

# async def testXjob() :
#     response = await StoriPostXXLJob("xxljobIdBatchPayment", accountId="11110211000000467489")
#     print(response)

# asyncio.run(testXjob())

# request = genBillRequest("11110211000000433705")
# StoriDoRequest(request)

# async def test() :
#     name = "xxljobIdPayment"
    
#     executorParam = getXXLJobParam(name)
#     executorParam["accountId"] = "11110011000055817010"   

#     body = [
#         {"name":"id","value": StoriEnv["xxljobIdPayment"],"contentType":'application/json'},
#         {"name":"executorParam", "value":json.dumps(executorParam),"contentType":'application/json'}
#         ]
    
#     url = getUrlFromPath(StoriPath.XXLJob)

#     # formData = FormData()
#     # formData.add_field('id', StoriEnv["xxljobIdPayment"], content_type='application/json')
#     # formData.add_field('executorParam', json.dumps(executorParam), content_type='application/json')

#     # for filed in body :
#     #     formData.add_field(filed["name"], filed["value"], content_type=filed["contentType"])

#     response = await StoriFetch(url, headers={"Cookie":StoriEnv["xxljobCookie"]}, body=body, params={}, method="POST")
#     print(response)

# asyncio.run(test())

# body1 = {"requestId":"3158093b-e7b9-4890-89e3-fa113bdaf384","customer":{"referenceCustId":"c9ae8442e6ca4a42bc197a8746018ea2","firstName":"Test","middleName":"Test","lastName":"Test","lastName2":"Test","birthdate":"19980830","email":"Sheldon.Bogan@gmail.com","idType":"INE","idValue":"656-317-7130","gender":"MALE","zipCode":"01724","streetName":"Fisher Lights","streetNumber":"234","city":"Aniyahburgh","region":"North Frankiemouth","country":"MEX"},"product":{"productCode":"STC001","cardType":"PHYSICAL","params":{"statementDay":"27","initialCreditLine":"1000000","initialCreditLineShow":"10000.00","apr":"89.90","subproductCode":"construye","openFee":"20000","openFeeShow":"200","disputeFee":"15000","disputeFeeShow":"150.00","cashWithdrawalNational":"5.00","cashWithdrawalInternational":"5.00","cardReplacementFee":"2000","cardReplacementFeeShow":"20.00","lateFeeMaxAmount":"3500","lateFeeMaxAmountShow":"35.00","lateFeeMethod":"tier","checkBalanceNational":"0","checkBalanceInternational":"0","clabe":""}},"embosser":{"name":"GID"},"apiKey":""}
# body["requestId"] = str(uuid.uuid4())
# body["customer"]["referenceCustId"] = body["requestId"]
# request = genSignRequest(body1)
# StoriDoRequest(request)