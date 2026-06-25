import json

get_result={"order_ids": ["25121200002001111100006306482497"], "card_id": "111100200022954863", "account_id": "11110011000211505632", "time_ids": {"25121200002001111100006306482497": "2025-12-12T12:00:39"}, "customer_id": "1111001000108863"}


order_id_map_to_time_ids=get_result["time_ids"]


customer_id = get_result["customer_id"]
account_id =  get_result["account_id"]
card_id =  get_result["card_id"]
incentive_flag = "MK20250413114503_first_5"
activity_no="MK20250413114503"

order_ids =get_result["order_ids"]

for i,order_id in enumerate(order_ids):
        get_time=order_id_map_to_time_ids[order_id]
        stat_date=str(get_time).split("T")[0]
        get_ddb_type = {"TableName": "adm-cb-credit-mk-customer-cashback-activity-ddb",
                      "Item": {"activity_no": {"S": activity_no},
                              "activity_no_order_id": {"S": (str(activity_no)+"_" + str(order_id))},
                              "update_time_local": {"S": get_time},
                              "customer_id": {"S": customer_id},
                              "order_id": {"S": order_id},
                              "incentive_flag": {"S": incentive_flag},
                              "account_id": {"S": account_id},
                              "card_id": {"S": card_id},
                              "create_time_local": {"S": get_time},
                              "stat_date": {"S":stat_date }
                              }
                      }
        print(json.dumps(json.dumps(get_ddb_type))+",")


