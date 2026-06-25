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
database = 'configB1'
connection = mysql.connector.connect(
    host=db_config["qa-aurora-cif"],
    port='3306',
    user='core-dml-qa',
    password=password,
    database=database,
    connection_timeout=10  # 连接超时10秒
)

cursor = connection.cursor(dictionary=need_field)
get_time = str(int(time.time()))
file_path = get_time + "mk_activity.txt"
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines("mk_activity***********\n")
    print("mk_activity***********")
    sql_statement = 'SELECT * from configB1.mk_activity where (activity_name like "%自动化%" or activity_desc like "%自动化%") and activity_name not like "%activityName%" limit 1000;'
    cursor.execute(sql_statement)
    result = cursor.fetchall()
    if need_origin_data == True:
        # result = json.loads(result, ensure_ascii=False, default=str)
        result = json.loads(result)
    # print(result)
    # 目标表名
    table_name = "corebankingB1.mk_activity"

    # 生成 INSERT SQL
    for get_one in result:
        # 排除 id 字段
        filtered_data = {k: v for k, v in get_one.items() if k != "id"}
        columns = ", ".join(filtered_data.keys())
        values = ", ".join([f"'{v}'" if v is not None else "NULL" for v in filtered_data.values()])
        insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
        print(insert_sql)
        f.writelines(insert_sql+"\n")



    get_all_activity_no = jsonpath.jsonpath(result, "$..activity_no")
    print("**************************")
    print("mk_activity_task***********")
    f.writelines("mk_activity_task***********\n")

    sql_statement = 'SELECT * from mk_activity_task where task_name like "%自动化%" or task_desc like "%自动化%" limit 1000;'
    cursor.execute(sql_statement)
    result = cursor.fetchall()
    if need_origin_data == True:
        # result = json.dumps(result, ensure_ascii=False, default=str)
        result = dict(result)
    # print(result)
    for get_one in result:

        # 排除 id 字段
        filtered_data = {k: v for k, v in get_one.items() if k != "id"}
        columns = ", ".join(filtered_data.keys())
        values = ", ".join([f"'{v}'" if v is not None else "NULL" for v in filtered_data.values()])
        insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
        print(insert_sql)
        f.writelines(insert_sql+"\n")

connection.close()
