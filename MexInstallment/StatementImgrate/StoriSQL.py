import aiomysql
import aiomysql.cursors
from StoriConfigs import readSQLConfigs
import pandas as pd
from StoriUtils import snake_to_camel
import asyncio
from functools import wraps

class StoriSQL:
    def __init__(self):  
        self.configs = readSQLConfigs()
        self.resultData = {}
        self.pools = {}
        self.poolLock = asyncio.Lock()

    async def safeClose(self) :
        try : 
            for key in self.pools:
                pool = self.pools[key]
                pool.close()
                await pool.wait_closed()
        except Exception as e :
            print(e)
        finally :
            self.pools = {}

    # 根据accountId查询分库分表信息
    def getAccountIdKey(self, accountId:str, table:str) :
        isShadow = accountId.startswith("999")
        did = accountId[4:6] # 库id
        if did == "00" :
            table = "default"
        tableInfo:str = self.configs["tables"][table]
        tableInfos = tableInfo.split("-")
        batchSuffix = tableInfos[0]
        dbPrefix = tableInfos[1]
        if batchSuffix in ["global", "cif"]:
            tid = ""
            batchID = ""
            if isShadow :
                dbSuffix = "Shadow"
            else :
                dbSuffix = "A1"
        else :
            if isShadow :
                batchID = ("01" if int(did)%2==0 else "02")
                dbSuffix = "Shadow" + did
            else :
                batchID = ("01" if int(did)<=3 else "02")    
                dbSuffix = "A" + did

        if batchSuffix == "global" :
            tid = ""
        else :
            tid = "_" + str(int(accountId[-3:-1]) % 20).zfill(2) # 表id
        
        batchName = "qa-aurora-" + batchSuffix + batchID
        dbName = dbPrefix + dbSuffix
        return (batchName, dbName, tid)
    
    async def getPool(self, batchName, dbName) :
        async with self.poolLock :
            key = batchName+":"+dbName
            if key in self.pools :
                pool = self.pools[key]
            else :
                defaults:dict = self.configs["defaults"]
                config = defaults.copy()
                host = self.configs["batches"][batchName]
                config["host"] = host
                config["db"] = dbName
                pool = await aiomysql.create_pool(**config)
                self.pools[key] = pool
        return pool
    
    def dbquery_decorator():
        def decorator(func):
            @wraps(func)
            async def wrapper(self, *args, **kwargs):
                table, keys, condition, tid0 = await func(self, *args, **kwargs)
                accountId = args[0]
                batchName, dbName, tid = self.getAccountIdKey(accountId, table)
                try:
                    # print(f"connect {batchName} : {dbName}")
                    pool = await self.getPool(batchName, dbName)
                    async with pool.acquire() as conn:
                        async with conn.cursor() as cursor:
                            if tid != None and len(tid) > 0 and tid0 != None:
                                tid = tid0
                            df = await StoriSqlQuery(cursor, keys, table, condition, tid)
                            if type(df) == pd.DataFrame :
                                data = df.to_dict('records')
                            else :
                                data = []
                    return data
                except Exception as e:
                    print(e)
            return wrapper
        return decorator
    
    @dbquery_decorator()
    async def queryGeneralTask(self, accountId, taskType, limit = 0):
        condition = f"account_id = '{accountId}' and task_type = '{taskType}'"
        if limit != 0 :
            condition += f" ORDER BY id DESC LIMIT {limit} "
        table = "cc_task_general"
        keys = ["reference_key", "status", "task_params", "task_type", "task_source"]
        return (table, keys, condition, "")
    
    @dbquery_decorator()
    async def queryPaymentTask(self, accountId, reference_key, limit = 0):
        condition = f"account_id = '{accountId}' and task_type = 'PAYMENT' and reference_key = '{reference_key}'"
        if limit != 0 :
            condition += f" ORDER BY id DESC LIMIT {limit} "
        table = "cc_task_payment"
        keys = ["reference_key", "status", "task_params", "task_type", "task_source"]
        return (table, keys, condition, "")
    
    @dbquery_decorator()
    async def queryUserAccount(self, accountId):
        condition = f"parent_account_no = '{accountId}'"
        table = "cc_crt_account"
        keys = ["customer_id", "contract_id", "open_date", "balance", "parent_account_no"]
        return (table, keys, condition, "")

    @dbquery_decorator()
    async def queryInstallment(self, accountId) :
        table="cc_ins_installment_info"
        keys = ["account_id", "reference_id","periods","apply_time_local","principal"]
        condition = f"account_id = '{accountId}'"
        return (table, keys, condition, None)
    
    @dbquery_decorator()
    async def queryBenefitRecord(self, accountId) :
        table="mk_bf_receive_record"
        keys = ["account_id", "benefit_type", "benefit_name", "benefit_snapshot", "status", "benefit_no", "usage_time", "usage_amount"]
        condition = f"account_id = '{accountId}'"
        return (table, keys, condition, None)
    
    @dbquery_decorator()
    async def queryDQStatus(self, accountId) :
        table="cc_ctl_dq_status"
        keys = ["account_id", "dq_days","dq_bucket","status","due_bucket","start_due_date","recovery_date","last_check_date"]
        condition = f"account_id = '{accountId}'"
        return (table, keys, condition, "")
    
    @dbquery_decorator()
    async def queryUserParams(self, accountId, contract_id) :
        table = "cc_par_common_param"
        keys = ["param_key", "param_value", "product_code"]
        condition = f"product_code = '{contract_id}@CONTRACT'"
        tid = "_" + contract_id[4:6] + contract_id[-2]
        return (table, keys, condition, tid)
    
    @dbquery_decorator()
    async def queryLastestProcess(self, accountId, limit = 0) :
        table="cc_bs_activity_process"
        keys=["create_time_local", "reference_id", "type", "sub_type", "action_type", "amt", "effective_time_local", "transaction_local_time", "status", "channel","request_id"]
        condition = f"account_id = '{accountId}'"
        if limit != 0 :
            condition += f" ORDER BY id DESC LIMIT {limit} "
        return (table, keys, condition, None)
    
    @dbquery_decorator()
    async def queryAccountActivity(self, accountId, request_id = None) :
        table="cc_bs_account_activity"
        keys=["create_time_local", "type", "handle_status", "request_id", "amt", "pmt_amt", "effective_time_local", "post_time_local","type","sub_type","reference_id","post_status"]
        condition = f"account_id = '{accountId}'"
        if request_id :
            condition += " and request_id = '{request_id}'"
        return (table, keys, condition, None)
    
    @dbquery_decorator()
    async def queryStatement(self, accountId, limit = 0, settled=True) :
        table="cc_bs_statement"
        keys = ["statement_id", "account_id", "create_time_local", "billing_cycle","statement_dt","due_dt","grace_dt","previous_bal","new_bal","min_pmt","pmt_amt","current_pmt_amt","pending_pmt_amt","grace_dt_unpaid_mini_amt","due_dt_unpaid_mini_amt","activity_summary","status"]                
        condition = f"account_id = '{accountId}'"

        if settled == True :
            condition += " and statement_dt != 'UNSETTLED' "
        if limit != 0 :
            condition += f" ORDER BY id DESC LIMIT {limit} "
        return (table, keys, condition, None)
    
    @dbquery_decorator()
    async def queryStatementTask(self, accountId, reference_key) :
        table="cc_bs_statement"
        keys = ["account_id", "create_time_local", "status"]                
        condition = f"account_id = '{accountId}' and task_type = 'CREDIT_CARD_STATEMENT' and reference_key = '{reference_key}'"
        condition += f" ORDER BY id DESC LIMIT {1} "
        return (table, keys, condition, None)
    
    @dbquery_decorator()
    async def queryPaymentAllocation(self, accountId, statementIds:list = None) :
        table="cc_pmt_payment_allocation"
        keys = ["account_id", "create_time_local", "pmt_effective_time_local", "account_activity_id", "pmt_id", "activity_statement_id", "payment_statement_id", "statement_id", "type", "subtype", "amt"]                
        condition = f"account_id = '{accountId}'"
        if statementIds :
            statements = ", ".join(statementIds)
            condition += f"IN {statements}"
        return (table, keys, condition, None)
    
    async def getAccountContractInfo(self, accountId:str, data) :
        results = await self.queryUserAccount(accountId)
        if results and len(results) > 0 :
            data["account"] = results[0]
            contract_id = data["account"]['contract_id']
        else :
            assert(0)
        
        results = await self.queryUserParams(accountId, contract_id)
        params = {}
        for result in results :
            key = snake_to_camel(result["param_key"])
            params[key] = result["param_value"]
        data["params"] = params
    
    async def getAccountDataForReconstruct(self, accountId:str) :
        data = {
            "accountId" : accountId 
        }
        self.resultData[accountId] = data

        async def task1() :
            results = await self.queryStatement(accountId)
            data["statement"] = results

        async def task2() :
            results = await self.queryPaymentAllocation(accountId)
            data["payment"] = results

        async def task3() :
            results = await self.queryDQStatus(accountId)
            if len(results) > 0 :
                data["dq"] = results[-1]

        async def task4() :
            results = await self.queryAccountActivity(accountId)
            data["activity"] = results

        async def task5() :
            results = await self.queryInstallment(accountId)
            data["installment"] = results

        async def task6() :
            result = await self.queryBenefitRecord(accountId)
            data["benefit"] = result

        asyncTasks = []
        asyncTasks.append(self.getAccountContractInfo(accountId, data))
        asyncTasks.append(task1())
        asyncTasks.append(task2())
        asyncTasks.append(task3())
        asyncTasks.append(task4())
        asyncTasks.append(task5())
        asyncTasks.append(task6())
        await asyncio.gather(*asyncTasks)
        return data
     

    async def getAccountData(self, accountId:str) :
        data = {
            "accountId" : accountId 
        }
        self.resultData[accountId] = data

        async def task2() :
            results = await self.queryInstallment(accountId)
            data["installment"] = results
        
        async def task3() :
            results = await self.queryDQStatus(accountId)
            if len(results) > 0 :
                data["dq"] = results[-1]

        async def task4() :
            results = await self.queryLastestProcess(accountId)
            data["activity"] = results

        async def task5() :
            results = await self.queryStatement(accountId)
            data["statement"] = results

        async def task6() :
            result = await self.queryBenefitRecord(accountId)
            data["benefit"] = result

        asyncTasks = []
        asyncTasks.append(self.getAccountContractInfo(accountId, data))
        asyncTasks.append(task2())
        asyncTasks.append(task3())
        asyncTasks.append(task4())
        asyncTasks.append(task5())
        asyncTasks.append(task6())
        await asyncio.gather(*asyncTasks)
        return data
     
    async def runAcccountsDataTasks(self, accounts:list, forRecovery = False) :
        asyncTasks = []
        for accountId in accounts :
            if forRecovery :
                asyncTasks.append(self.getAccountDataForReconstruct(accountId))
            else :
                asyncTasks.append(self.getAccountData(accountId))
        results = await asyncio.gather(*asyncTasks)
        await self.safeClose()

    def getAccountsData(self, accounts:list, forRecovery=False) :
        asyncio.run(self.runAcccountsDataTasks(accounts, forRecovery))
        return self.resultData
    
async def StoriSqlQuery(cursor: aiomysql.cursors.Cursor, keys : list, table :str, condition, tid="", retDF = True) :
    comma_separated_string = ','.join(keys)
    sql = f"select {comma_separated_string} from {table}{tid} where {condition}"
    # print(f"{sql}")
    await cursor.execute(sql)
    results = await cursor.fetchall()
    if retDF :
        if len(results)==0 :
            return None
        df = pd.DataFrame(results)
        df.columns = keys
        return df
    return results


