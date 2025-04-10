import os
from datetime import datetime, timedelta
import yaml

UDI_DIC = {}
CYCLE_LIST_12 = []
CYCLE_LIST_27 = []

MINIMUM_PAYMENT_THRESHOLD = 100
VAT_RATE = 0.16

InstallmentAprDic = {3:0.300000, 6:0.400000, 9:0.500000, 12:0.600000}

def readCycle(day) :
    cycleList = []
    if (day == 12) :
        cycleList = CYCLE_LIST_12
    elif (day == 27) :
        cycleList = CYCLE_LIST_27
    else :
        assert(0)
    if (len(cycleList) > 0) :
        return cycleList

    keys = ["initialDay", "endDay", "statementDay", "dueDay", "graceDay"]
    num = len(keys)
    with open('const/StatementCycle'+str(int(day)), 'r', encoding='utf-8') as file:  
        content = file.read()  
        lines = content.split()
        print(len(lines))
        assert(len(lines) % num == 0)
        for i in range(int(len(lines)/num)) :
            dic = {}
            index = i * num
            for j in range(len(keys)) :
                value = datetime.strptime(lines[index +j], "%Y%m%d").date()
                dic[keys[j]] = value
            dic["DQTriggerDay"] = dic["dueDay"] + timedelta(days=1)
            cycleList.append(dic)
        print(cycleList)
    return cycleList

def readUDI() : 
    udiDic = UDI_DIC
    if (len(udiDic) > 0) :
        return udiDic
    with open('const/UDI', 'r', encoding='utf-8') as file:  
        content = file.read()  
        lines = content.split()
        for i in range(len(lines)>>1) :
            index = i << 1
            dateStr = lines[index]
            udiStr = lines[index+1]
            date = datetime.strptime(dateStr, "%Y%m%d").date()
            udi = float(udiStr)
            udiDic[date] = udi
            # udiDic[dateStr] = udi
        return udiDic
  
def readSQLConfigs() :
    with open('const/SQL.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

def readServerConfigs(env, tenant) :
    absolute_path=os.getcwd()
    with open(absolute_path+'/const/server.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
        env:dict = config[env]
        tenant:dict = config[tenant]
        env.update(tenant)
        env.update({
            "crowdNo" : "23010100100100999100000000089343",
            "benefitBatchNo" : "23012000100100111100000005378273",
            "email00" : "metersphere00@example.org"
        })
    return env
