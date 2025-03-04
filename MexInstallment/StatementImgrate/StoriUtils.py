
import math
from datetime import datetime, timedelta
import time
import logging
import traceback

# 银行家算法
def round_to_even(number, precision = 2):  

    assert(precision <= 6)

    if (abs(number) < 0.000000001) :
        return 0
    
    flag = False
    if (number < 0) :
        flag = True
        number = 0.00 - number

    # 获取整数部分leftStr，和小数部分decimalStr
    numStr = str(number)
    assert(("e" in numStr) == False)
    numList = numStr.split(".")
    assert(len(numList) > 0)
    leftStr = numList[0]
    decimalStr = ""
    if(len(numList) > 1) :
        decimalStr = numList[1]
    
    # 如果小数部分的位数>精度
    if (len(decimalStr) > precision) :
        # 移位precision
        while(len(decimalStr) < precision) :
            decimalStr = decimalStr + "0"
        appenleftStr = decimalStr[:precision]
        leftStr += appenleftStr
        decimalStr = decimalStr[precision:]

        midNum = int(5)
        left = int(leftStr)

        # 查看小数部分第一位
        d1 = int(0)
        if (len(decimalStr) > 0) :
            d1 = int(decimalStr[0])
        
        # >5 进位  
        if d1 > midNum:  
            left = left + int(1)
        # =5   
        elif d1 == midNum:  
            if float("0." + decimalStr) != 0.5 : # 5后面不全是0，进位
                left = left + int(1)
            else : # 5后面全是0
                if left % 2 != 0: # 奇数，进位  
                    left = left + int(1)

        if (precision == 0) :
            number = left
        elif left == 0 :
            number = left
        else :
            leftStr = str(left)
            while len(leftStr) < precision + 1 :
                leftStr = "0"+ leftStr
            decimalStr = leftStr[-precision:]
            leftStr = leftStr[0:-precision]
            numStr = leftStr + "." + decimalStr
            number = float(numStr)

    if flag == True:
        number = 0.00-number
    if (precision == 0) :
        number = int(number)

    return number 

# assert(round_to_even(3.1512, 2)==3.15)
# assert(round_to_even(3.1552, 2)==3.16)
# assert(round_to_even(3.1569, 2)==3.16)
# assert(round_to_even(3.1550, 2)==3.16)

# assert(round_to_even(-3.1512, 2)==-3.15)
# assert(round_to_even(-3.1552, 2)==-3.16)
# assert(round_to_even(-3.1569, 2)==-3.16)
# assert(round_to_even(-3.1550, 2)==-3.16)

# assert(round_to_even(19.455, 2)==19.46)
# assert(round_to_even(-19.455, 2)==-19.46)
# assert(round_to_even(0, 2)==0)
# assert(round_to_even(0.1, 2)==0.1)
# assert(round_to_even(0.0512, 2)==0.05)

# assert(round_to_even(1.3322676295501878e-15, 2)==0)
# assert(float("0.500000") == 0.5)

# 等额本息计算
def calculate_monthly_payment(total_amount, mpr, periods, msi = False):  
      
    # 使用公式计算每期分期等额本息  
    if msi :
        monthly_payment = total_amount / periods
    else :
        monthly_payment = total_amount * mpr / (1 - math.pow((1 + mpr), -periods))  
      
    return round_to_even(monthly_payment, 0)

def snake_to_camel(snake_str):
    # 除了第一个单词首字母小写，其他单词首字母大写并连接
    words = snake_str.split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])

def currentTimeMillis() :
    dt = datetime.now()
    milliseconds = int(dt.timestamp() * 1000000)
    return milliseconds

def getDicKeypath(d, keypath):
    first:str = keypath[0]
    if first.endswith("]") :
        keys = first.split("[")
        key = keys[0]
        first = keys[1]
        firstNum = int(first[:-1])
        if len(key) > 0 :
            if key in d :
                d = d[key]
            else :
                return None
        if type(d) != list :
            return None
        if len(keypath) == 1:
            return d[firstNum]
        return getDicKeypath(d[firstNum], keypath[1:])
    else :
        if type(d) != dict :
            return None
        if not (first in d) :
            return None
        if len(keypath) == 1 :
            return d[first]
        return getDicKeypath(d[first], keypath[1:])

def getRunTime(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录开始时间
        result = func(*args, **kwargs)  # 调用原始函数
        end_time = time.time()  # 记录结束时间
        execution_time = end_time - start_time
        print(f"执行总时间: {execution_time} 秒")
        return result
    return wrapper


def getUTCDateTime(local_time) :
    if type(local_time) == str :
        local_time = datetime.strptime(local_time, '%Y-%m-%d %H:%M:%S')
    utcTime = local_time + timedelta(hours=6)
    return utcTime

def getUTCTimeStr(utcTime) :
    utc_str = utcTime.strftime("%Y-%m-%dT%H:%M:%S")
    return utc_str

def getISO8601UTCTimeStr(utcTime) :
    ios8601_utc = utcTime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'
    return ios8601_utc

def loggingExpect(logger:logging, e) :
    logger.critical(e)
    tb = traceback.extract_tb(e.__traceback__)
    filename, lineno, funcname, text = tb[-1]
    logger.info(filename)
    logger.info(lineno)
    logger.info(funcname)

# reDic = {'customer_id': ['${customerId}', '${customerId}'], 'contract_id': '${customerId}', 'account_id': '${accountId}', 'card_id': '${cardId}', 'product_code': '${productCode}', 'user_id': '${userId}'}
# reMap = {'${customerId}': 100}

# replaceDicByMap(reDic, reMap)
# print(reDic)

    
# nested_dict = {
#     'key1': 'value1',
#     'key2': {
#         'key3': [
#             {'k8':'value3'},
#             {'k9':'value9'},
#             {'k7':'value7'},
#         ],
#         'key4': {
#             'key5': 'value5'
#         }
#     }
# }

# ret = getDicKeypath(nested_dict, ["key2","key3","[1]","k9"])
# print(ret)


# $.data.accountActivityList[0].referenceId

# response = {'data': {'accountActivityList': [{'mccCode': '4816', 'amount': 10000, 'effectiveTimeLocal': '2024-06-29T18:36:40.000+00:00', 'description': 'MEXICO, AMAZON MX, ', 'subType': 'AUTH', 'type': 'PURCHASE', 'effectiveDayLocal': '20240629', 'currencyCode': 'MXN', 'referenceId': '24062900002001111100006759388785', 'merchantName': 'AMAZON MX', 'status': 'NORMAL'}, {'mccCode': '4816', 'amount': 10000, 'effectiveTimeLocal': '2024-06-29T18:23:07.000+00:00', 'description': 'MEXICO, AMAZON MX, ', 'subType': 'AUTH', 'type': 'PURCHASE', 'effectiveDayLocal': '20240629', 'currencyCode': 'MXN', 'referenceId': '24062900002001111100006759388784', 'merchantName': 'AMAZON MX', 'status': 'NORMAL'}], 'pageNo': 1, 'pageSize': 100, 'originPageNo': 0}, 'message': '', 'status': 'Success', 'statusCode': '00000', 'timestamp': '2024-06-17T07:52:36.942-06:00'}
# path = "$.data.accountActivityList[0].referenceId".split(".")[1:]
# ret = getDicKeypath(response, path)
# print(ret)

