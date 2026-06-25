import json

import mysql.connector

activity_no="MK20260602212918"
benefit_batch_no = "24050100100100111100000000010137"





need_field=True
need_origin_data=False

db_config={
"qa-aurora-global": "core-banking-mysql-qa.cluster-cpuztzrlf1ji.us-east-1.rds.amazonaws.com",
"qa-aurora-gateway": "core-banking-gateway-mysql-qa.cluster-cpuztzrlf1ji.us-east-1.rds.amazonaws.com",
"qa-aurora-cif": "core-banking-cif-qa.cluster-cpuztzrlf1ji.us-east-1.rds.amazonaws.com",
"qa-aurora-trading01": "core-banking-trading-qa.cluster-cpuztzrlf1ji.us-east-1.rds.amazonaws.com",
"qa-aurora-trading02": "core-banking-trading02-qa.cluster-cpuztzrlf1ji.us-east-1.rds.amazonaws.com",
"qa-aurora-batch01": "core-banking-batch-qa.cluster-cpuztzrlf1ji.us-east-1.rds.amazonaws.com",
"qa-aurora-batch02": "core-banking-batch02-qa.cluster-cpuztzrlf1ji.us-east-1.rds.amazonaws.com",
"qa-aurora-bko": "core-banking-bko-qa.cluster-cpuztzrlf1ji.us-east-1.rds.amazonaws.com"
}
password='8MfbNdxr6mHfEBPQ'
database='configA1'
connection = mysql.connector.connect(
    host=db_config["qa-aurora-cif"],
    port='3306',
    user='core-dml-qa',
    password=password,
    database=database,
    connection_timeout=10 # 连接超时10秒
)

cursor = connection.cursor(dictionary=need_field)
print("mk_activity***********")

sql_statement="SELECT * from mk_activity where activity_no='"+activity_no+"' limit 500"
cursor.execute(sql_statement)
result=cursor.fetchall()
if need_origin_data==True:
    result = json.dumps(result, ensure_ascii=False, default=str)
print(result)

print("**************************")
print("mk_activity_task***********")

sql_statement="SELECT * from mk_activity_task where activity_no='"+activity_no+"' limit 500;"
cursor.execute(sql_statement)
result=cursor.fetchall()
if need_origin_data==True:
    result = json.dumps(result, ensure_ascii=False, default=str)
    # result = dict(result)
    print()
print(result)

print("**************************")
print("mk_common_param***********")
sql_statement="SELECT * from mk_common_param where activity_no='"+activity_no+"' limit 500;"
cursor.execute(sql_statement)
result=cursor.fetchall()
if need_origin_data==True:
    result = json.dumps(result, ensure_ascii=False, default=str)
print(result)

print("**************************")
print("mk_bf_instance***********")
sql_statement="SELECT * from mk_bf_instance where benefit_batch_no='"+benefit_batch_no+"' limit 500;"
print(sql_statement)
cursor.execute(sql_statement)
result=cursor.fetchall()
if need_origin_data==True:
    result = json.dumps(result, ensure_ascii=False, default=str)
print(result)


print("**************************")
print("mk_bf_instance_rules***********")
sql_statement="SELECT * from configA1.mk_bf_instance_rules where benefit_batch_no='"+benefit_batch_no+"' limit 500;"
cursor.execute(sql_statement)
result=cursor.fetchall()
if need_origin_data==True:
    result = json.dumps(result, ensure_ascii=False, default=str)
print(result)

print("**************************")
print("mk_bf_instance_stock***********")

sql_statement="SELECT * from mk_bf_instance_stock where benefit_batch_no='"+benefit_batch_no+"' limit 500;"
cursor.execute(sql_statement)
result=cursor.fetchall()
json_result = json.dumps(result, ensure_ascii=False, default=str)
print(json_result)


connection.close()

