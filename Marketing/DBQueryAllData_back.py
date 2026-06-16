import json
import time

import jsonpath
import mysql.connector

activity_no = "MK20251120000006"
benefit_batch_no = "25112000100100333300000000000010"

need_field = True
need_origin_data = False

db_config = {
    "qa-aurora-global": "core-banking-mysql-qa.cluster-cpuztzrlf1ji.us-east-1.rds.amazonaws.com",
    "qa-aurora-gateway": "core-banking-gateway-mysql-qa.cluster-cpuztzrlf1ji.us-east-1.rds.amazonaws.com",
    "qa-aurora-cif": "core-banking-cif-qa.cluster-cpuztzrlf1ji.us-east-1.rds.amazonaws.com",
    "qa-aurora-trading01": "core-banking-trading-qa.cluster-cpuztzrlf1ji.us-east-1.rds.amazonaws.com",
    "qa-aurora-trading02": "core-banking-trading02-qa.cluster-cpuztzrlf1ji.us-east-1.rds.amazonaws.com",
    "qa-aurora-batch01": "core-banking-batch-qa.cluster-cpuztzrlf1ji.us-east-1.rds.amazonaws.com",
    "qa-aurora-batch02": "core-banking-batch02-qa.cluster-cpuztzrlf1ji.us-east-1.rds.amazonaws.com",
    "qa-aurora-bko": "core-banking-bko-qa.cluster-cpuztzrlf1ji.us-east-1.rds.amazonaws.com"
}
password = '8MfbNdxr6mHfEBPQ'
database = 'configA1'
connection = mysql.connector.connect(
    host=db_config["qa-aurora-cif"],
    port='3306',
    user='core-dml-qa',
    password=password,
    database=database,
    connection_timeout=10  # 连接超时10秒
)

cursor = connection.cursor(dictionary=need_field)
print("mk_activity***********")

sql_statement = 'SELECT * from configA1.mk_activity where (activity_name like "%自动化%" or activity_desc like "%自动化%") and activity_name not like "%activityName%" limit 1000;'
cursor.execute(sql_statement)
result = cursor.fetchall()
if need_origin_data == True:
    # result = json.loads(result, ensure_ascii=False, default=str)
    result = json.loads(result)
print(result)
# 目标表名
table_name = "configA1.mk_activity"
get_time = str(int(time.time()))

def create_insert_sql(result,file_path):
    with open(file_path, 'w') as file:
        # 生成 INSERT SQL
        for get_one in result:

            # 排除 id 字段
            filtered_data = {k: v for k, v in get_one.items() if k != "id"}
            columns = ", ".join(filtered_data.keys())
            values = ", ".join([f"'{v}'" if v is not None else "NULL" for v in filtered_data.values()])
            insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
            print(insert_sql)
            file.write(insert_sql)
        file.close()


file_path = get_time + "mk_activity.txt"
create_insert_sql(result,file_path)
get_all_activity_no = jsonpath.jsonpath(result, "$..activity_no")
print("**************************")


print("mk_activity_task***********")

sql_statement = 'SELECT * from configA1.mk_activity_task where task_name like "%自动化%" or task_desc like "%自动化%" limit 1000;'
cursor.execute(sql_statement)
result = cursor.fetchall()
if need_origin_data == True:
    # result = json.dumps(result, ensure_ascii=False, default=str)
    result = dict(result)
print(result)
file_path= get_time + "mk_activity_task.txt"
create_insert_sql(result,file_path)

print("************非特殊情况已经不需要了**************")
print("mk_common_param***********")
sql_statement = ("SELECT * from configA1.mk_common_param where activity_no in (" + str(get_all_activity_no).replace("[","")
                 .replace("]","") + ") limit 500;")
cursor.execute(sql_statement)
result = cursor.fetchall()
if need_origin_data == True:
    result = json.dumps(result, ensure_ascii=False, default=str)
print(result)
file_path = get_time + "mk_common_param.txt"
create_insert_sql(result,file_path)

print("**************************")
print("mk_bf_instance***********")
sql_statement = 'SELECT * from configA1.mk_bf_instance where benefit_name like "%自动化%" limit 500;'
print(sql_statement)
cursor.execute(sql_statement)
result = cursor.fetchall()
if need_origin_data == True:
    result = json.dumps(result, ensure_ascii=False, default=str)
print(result)
file_path = get_time + "mk_bf_instance.txt"
create_insert_sql(result,file_path)
get_all_benefit_no = jsonpath.jsonpath(result, "$..benefit_batch_no")

print("**************************")
print("mk_bf_instance_rules***********")
sql_statement = "SELECT * from configA1.mk_bf_instance_rules where benefit_batch_no in (" +str(get_all_benefit_no).replace("[","").replace("]","") + ") limit 500;"
cursor.execute(sql_statement)
result = cursor.fetchall()
if need_origin_data == True:
    result = json.dumps(result, ensure_ascii=False, default=str)
print(result)
file_path = get_time + "mk_bf_instance_rules.txt"
create_insert_sql(result,file_path)
print("**************************")
print("mk_bf_instance_stock***********")

sql_statement = "SELECT * from configA1.mk_bf_instance_stock where benefit_batch_no in (" + str(get_all_benefit_no).replace("[","").replace("]","") + ") limit 500;"
cursor.execute(sql_statement)
result = cursor.fetchall()
json_result = json.dumps(result, ensure_ascii=False, default=str)
print(json_result)
file_path = get_time + "mk_bf_instance_stock.txt"
create_insert_sql(result,file_path)
connection.close()
