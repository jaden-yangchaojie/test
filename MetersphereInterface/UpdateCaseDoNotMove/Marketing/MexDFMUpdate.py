import json
import re

import jsonpath

from MetersphereInterface import MetersphereUtils

get_data = {
    "header": [
        ["activity_no", "activity_name", "activity_desc", "activity_rules", "crowd_no", "activity_start_time",
         "activity_end_time", "product_code", "user_rules"]], "data": [
        {"activity_no": "MK20220911120020", "activity_name": "cashback", "activity_desc": "cashback",
         "activity_rules": "{\"cashbackAmountCalMethod\":\"percent\",\"cashbackAmountCalParams\":\"0.7\",\"cashbackMatchRuleType\":\"rules_engine\",\"cashbackLimit\":{},\"customerCondition\":[{\"limitType\":\"signContract\",\"timeLineLimit\":{\"startDate\":\"2024-01-27T00:00:00\",\"endDate\":\"2024-01-28T23:59:59\"}}],\"multiCashbacklimit\":[{\"amountLimit\":{\"value\":\"20003\"}}]}",
         "crowd_no": 2.209100010010011e+31, "activity_start_time": "2024-01-01 00:00:00",
         "activity_end_time": "2024-06-30 23:59:59", "product_code": "STC002", "user_rules": ""},
        {"activity_no": "MK20230918120137", "activity_name": "cashback month amount Time Limit",
         "activity_desc": "cashback month amount Time Limit",
         "activity_rules": "{\"cashbackAmountCalMethod\":\"percent\",\"cashbackAmountCalParams\":\"0.07\",\"cashbackMatchRuleType\":\"rules_engine\",\"cashbackLimit\":{},\"multiCashbacklimit\":[{\"amountLimit\":{\"value\":\"20003\"},\"countLimit\":{\"value\":\"2\"},\"timeLineLimit\":{\"timeType\":\"month\"}}]}",
         "crowd_no": 2.310100010010011e+31, "activity_start_time": "2024-01-01 00:00:00",
         "activity_end_time": "2024-06-30 23:59:59", "product_code": "STC002", "user_rules": ""},
        {"activity_no": "MK20220912120028", "activity_name": "cashback Cycle fixAmount Time Limit",
         "activity_desc": "cashback Cycle fixAmount Time Limit",
         "activity_rules": "{\"cashbackAmountCalMethod\":\"fixAmount\",\"cashbackAmountCalParams\":\"10001\",\"cashbackMatchRuleType\":\"rules_engine\",\"cashbackLimit\":{},\"multiCashbacklimit\":[{\"countLimit\":{\"value\":\"1\"},\"timeLineLimit\": {\"timeType\":\"cycle\"}}]}",
         "crowd_no": 2.2102000100100113e+31, "activity_start_time": "2024-01-01 00:00:00",
         "activity_end_time": "2024-06-30 23:59:59", "product_code": "STC002", "user_rules": ""},
        {"activity_no": "MK20221020120452", "activity_name": "cashback fixAmount Time Limit",
         "activity_desc": "cashback fixAmount Time Limit",
         "activity_rules": "{\"cashbackAmountCalMethod\":\"fixAmount\",\"cashbackAmountCalParams\":\"10001\",\"cashbackMatchRuleType\":\"rules_engine\",\"cashbackLimit\":{},\"multiCashbacklimit\":[{\"countLimit\":{\"value\":\"2\"}}]}",
         "crowd_no": 2.2102000100100113e+31, "activity_start_time": "2024-01-01 00:00:00",
         "activity_end_time": "2024-06-30 23:59:59", "product_code": "STC002", "user_rules": ""},
        {"activity_no": "MK20240814041050", "activity_name": "cashback user amount Limit",
         "activity_desc": "cashback user amount Limit",
         "activity_rules": "{\"cashbackAmountCalMethod\":\"percent\",\"cashbackAmountCalParams\":\"0.07\",\"cashbackMatchRuleType\":\"rules_engine\",\"cashbackLimit\":{},\"multiCashbacklimit\":[{\"amountLimit\":{\"value\":\"20000\"}}]}",
         "crowd_no": 2.4081400100100113e+31, "activity_start_time": "2024-01-01 00:00:00",
         "activity_end_time": "2024-06-30 23:59:59", "product_code": "STC002",
         "user_rules": "[{\"amountLimit\":{\"amountLimitType\":\"creditLine\",\"value\":\"0.01\"}}]"},
        {"activity_no": "MK20240130003923", "activity_name": "cashback cycle amount Time Limit",
         "activity_desc": "cashback cycle amount Time Limit",
         "activity_rules": "{\"cashbackAmountCalMethod\":\"percent\",\"cashbackAmountCalParams\":\"0.07\",\"cashbackMatchRuleType\":\"rules_engine\",\"cashbackLimit\":{},\"multiCashbacklimit\":[{\"amountLimit\":{\"value\":\"20003\"},\"countLimit\":{\"value\":\"2\"},\"timeLineLimit\": {\"timeType\":\"cycle\"}}]}",
         "crowd_no": 2.401300010010011e+31, "activity_start_time": "2024-01-01 00:00:00",
         "activity_end_time": "2024-06-30 23:59:59", "product_code": "STC002", "user_rules": ""},
        {"activity_no": "MK20240808214110", "activity_name": "cashback New interval Time Limit",
         "activity_desc": "cashback New interval Time Limit",
         "activity_rules": "{\"cashbackAmountCalMethod\":\"percent\",\"cashbackAmountCalParams\":\"0.07\",\"cashbackMatchRuleType\":\"rules_engine\",\"cashbackLimit\":{},\"multiCashbacklimit\":[{\"countLimit\":{\"value\":\"1\"},\"timeLineLimit\":{\"timeType\":\"interval\",\"startDate\":\"2024-01-29T00:00:00\",\"endDate\":\"2024-03-01T23:59:59\"}}]}",
         "crowd_no": 2.406080010010011e+31, "activity_start_time": "2024-01-01 00:00:00",
         "activity_end_time": "2024-06-30 23:59:59", "product_code": "STC002", "user_rules": ""},
        {"activity_no": "MK20240804234531", "activity_name": "cashback New Limit",
         "activity_desc": "cashback New Limit",
         "activity_rules": "{\"cashbackAmountCalMethod\":\"percent\",\"cashbackAmountCalParams\":\"0.07\",\"cashbackMatchRuleType\":\"rules_engine\",\"cashbackLimit\":{},\"multiCashbacklimit\":[{\"timeLineLimit\":{\"timeType\":\"cycle\"},\"countLimit\":{\"value\":\"1\"}}]}",
         "crowd_no": 2.4080400100100113e+31, "activity_start_time": "2024-01-01 00:00:00",
         "activity_end_time": "2024-06-30 23:59:59", "product_code": "STC002", "user_rules": ""},
        {"activity_no": "MK20221127010016", "activity_name": "cashback New Time Limit",
         "activity_desc": "cashback New Time Limit",
         "activity_rules": "{\"cashbackAmountCalMethod\":\"percent\",\"cashbackAmountCalParams\":\"0.07\",\"cashbackMatchRuleType\":\"rules_engine\",\"cashbackLimit\":{},\"multiCashbacklimit\":[{\"countLimit\":{\"value\":\"2\"}}]}",
         "crowd_no": 2.407300010010011e+31, "activity_start_time": "2024-01-01 00:00:00",
         "activity_end_time": "2024-06-30 23:59:59", "product_code": "STC002", "user_rules": ""},
        {"activity_no": "MK20221117120358", "activity_name": "cashback New Account Limit",
         "activity_desc": "cashback New Account Limit",
         "activity_rules": "{\"cashbackAmountCalMethod\":\"percent\",\"cashbackAmountCalParams\":\"0.07\",\"cashbackMatchRuleType\":\"rules_engine\",\"cashbackLimit\":{},\"multiCashbacklimit\":[{\"amountLimit\":{\"value\":\"20003\"}}]}",
         "crowd_no": 2.501110010010011e+31, "activity_start_time": "2024-01-01 00:00:00",
         "activity_end_time": "2024-06-30 23:59:59", "product_code": "STC002", "user_rules": ""},
        {"activity_no": "MK20240113000023", "activity_name": "cashback New Account Time Limit 20240726112010",
         "activity_desc": "cashback New Account Time Limit 20240726112010",
         "activity_rules": "{\"cashbackAmountCalMethod\":\"percent\",\"cashbackAmountCalParams\":\"0.07\",\"cashbackMatchRuleType\":\"rules_engine\",\"cashbackLimit\":{},\"multiCashbacklimit\":[{\"amountLimit\":{\"value\":\"20003\"},\"countLimit\":{\"value\":\"2\"}}]}",
         "crowd_no": 2.407250010010011e+31, "activity_start_time": "2024-01-01 00:00:00",
         "activity_end_time": "2024-06-30 23:59:59", "product_code": "STC002", "user_rules": ""},
        {"activity_no": "MK20240422035921", "activity_name": "用户维度规则1场景测试",
         "activity_desc": "用户维度规则1场景测试",
         "activity_rules": "{\"cashbackAmountCalMethod\":\"percent\",\"cashbackAmountCalParams\":\"0.07\",\"cashbackMatchRuleType\":\"rules_engine\",\"cashbackLimit\":{\"accountLimit\":{\"timeLimit\":{\"timeType\":\"cycle\",\"value\":\"20003\"}}}}",
         "crowd_no": 2.404220010010011e+31, "activity_start_time": "2024-04-25 00:00:00",
         "activity_end_time": "2024-05-30 23:59:59", "product_code": "STC002",
         "user_rules": "[{\"timeLineLimit\":{\"timeType\":\"singContractDate\",\"value\":\"30\"}}]"},
        {"activity_no": "MK20240113000013", "activity_name": "Cashback Activity of Cycle Account Limit 20240229143041",
         "activity_desc": "Cashback Activity of Cycle Account Limit 20240229143041",
         "activity_rules": "{\"cashbackAmountCalMethod\":\"percent\",\"cashbackAmountCalParams\":\"0.07\",\"cashbackMatchRuleType\":\"rules_engine\",\"cashbackLimit\":{\"accountLimit\":{\"timeLimit\":{\"timeType\":\"cycle\",\"value\":\"20003\"}}}}",
         "crowd_no": 2.401130010010011e+31, "activity_start_time": "2024-01-01 00:00:00",
         "activity_end_time": "2024-06-30 23:59:59", "product_code": "STC002", "user_rules": "(null)"},
        {"activity_no": "MK20240229002204", "activity_name": "返现新模型", "activity_desc": "返现新模型",
         "activity_rules": "{\"cashbackAmountCalMethod\":\"percent\",\"cashbackAmountCalParams\":\"0.07\",\"cashbackMatchRuleType\":\"rules_engine\",\"cashbackRuleKnowledgeId\":\"rt_marketing_cashback_beta2\",\"cashbackLimit\":{\"accountLimit\":{\"timeLimit\":{\"timeType\":\"cycle\",\"value\":\"20003\"}}},\"multiCashbacklimit\":[{\"amountLimit\":{\"value\":\"20003\"},\"timeLineLimit\":{\"timeType\":\"cycle\"}}]}",
         "crowd_no": 2.402290010010011e+31, "activity_start_time": "2024-01-01 00:00:00",
         "activity_end_time": "2024-06-30 23:59:59", "product_code": "STC002", "user_rules": "(null)"},
        {"activity_no": "MK20240305032943", "activity_name": "Cashback Activity Of Interval Account Limit",
         "activity_desc": "Cashback Activity Of Interval Account Limit",
         "activity_rules": "{\"cashbackAmountCalMethod\":\"percent\",\"cashbackAmountCalParams\":\"0.07\",\"cashbackMatchRuleType\":\"rules_engine\",\"cashbackLimit\":{},\"multiCashbacklimit\":[{\"amountLimit\":{\"value\":\"20000\"},\"timeLineLimit\":{\"timeType\":\"interval\",\"startDate\":\"2024-01-29T00:00:00\",\"endDate\":\"2024-03-01T23:59:59\"}}]}",
         "crowd_no": 2.403050010010011e+31, "activity_start_time": "2024-01-01 00:00:00",
         "activity_end_time": "2024-06-30 23:59:59", "product_code": "STC002", "user_rules": "(null)"},
        {"activity_no": "MK20240305002838", "activity_name": "Cashback Activity Of Time Limit",
         "activity_desc": "Cashback Activity Of Time Limit",
         "activity_rules": "{\"cashbackAmountCalMethod\":\"percent\",\"cashbackAmountCalParams\":\"0.07\",\"cashbackMatchRuleType\":\"rules_engine\",\"cashbackLimit\":{},\"multiCashbacklimit\":[{\"countLimit\":{\"value\":\"1\"},\"timeLineLimit\":{\"timeType\":\"cycle\"}}]}",
         "crowd_no": 2.403050010010011e+31, "activity_start_time": "2024-01-01 00:00:00",
         "activity_end_time": "2024-06-30 23:59:59", "product_code": "STC002", "user_rules": "(null)"}]}
new_get_data = {}
for get_one in get_data["data"]:
    activity_no = get_one['activity_no']
    new_get_data[activity_no] = get_one

get_data1 = [
    {
        "用例个数": 13,
        "活动号": "MK20240113000013",
        "关联人群": "24011300100100111100000000098887",
        "activity_rules_updated_fix": {
            "cashbackRule": {
                "type": "percent",
                "calAlg": {
                    "type": "single",
                    "param": "0.07",
                    "rules": []
                },
                "limit": [{
                    "limitType": "cycle",
                    "amountLimit": "20003",

                }]
            },
            "transactionRule": {}
        },
        "活动规则": {
            "cashbackAmountCalMethod": "percent",
            "cashbackAmountCalParams": "0.07",
            "cashbackMatchRuleType": "rules_engine",
            "cashbackLimit": {
                "accountLimit": {
                    "timeLimit": {
                        "timeType": "cycle",
                        "value": "20003"
                    }
                }
            }
        },
        "人群规则": {
            "productCode": "STC002",
            "openDate": "2024-01-28T02:00:00",
            "openEndDate": "2024-01-28T02:59:59"
        },
        "规则类型": "账期限额"
    },
    {
        "用例个数": 5,
        "活动号": "MK20240305002838",
        "关联人群": "24030500100100111100000000099127",
        "activity_rules_updated_fix": {
            "cashbackRule": {
                "type": "percent",
                "calAlg": {
                    "type": "single",
                    "param": "0.07",
                    "rules": []
                },
                "limit": [{
                    "limitType": "cycle",
                    "countLimit": "1",

                }]
            },
            "transactionRule": {}
        },
        "活动规则": {
            "cashbackAmountCalMethod": "percent",
            "cashbackAmountCalParams": "0.07",
            "cashbackLimit": {
                "repeatsLimit": {
                    "timeLimit": {
                        "timeType": "cycle",
                        "value": "1"
                    }
                }
            }
        },
        "人群规则": {
            "productCode": "STC002",
            "openDate": "2024-01-28T00:00:00",
            "openEndDate": "2024-01-28T01:00:00"
        },
        "规则类型": "账期限次"
    },
    {
        "用例个数": 10,
        "活动号": "MK20240305032943",
        "关联人群": "24030500100100111100000000099128",
        "activity_rules_updated_fix": {
            "cashbackRule": {
                "type": "percent",
                "calAlg": {
                    "type": "single",
                    "param": "0.07",
                    "rules": []
                },
                "limit": [{
                    # "limitType": "interval",
                    "limitType": "campaignPeriod",
                    "amountLimit": "20000"
                    # "startDate": "2024-01-29T00:00:00",
                    # "endDate": "2024-03-01T23:59:59"

                }]
            },
            "transactionRule": {}
        },
        "活动规则": {
            "cashbackAmountCalMethod": "percent",
            "cashbackAmountCalParams": "0.07",
            "cashbackMatchRuleType": "rules_engine",
            "cashbackLimit": {},
            "multiCashbacklimit": [
                {
                    "amountLimit": {
                        "value": "20000"
                    },
                    "timeLineLimit": {
                        "timeType": "interval",
                        "startDate": "2024-01-29T00:00:00",
                        "endDate": "2024-03-01T23:59:59"
                    }
                }
            ]
        },
        "人群规则": {
            "productCode": "STC002",
            "openDate": "2024-01-28T03:00:00",
            "openEndDate": "2024-01-28T03:59:59"
        },
        "规则类型": "时间区间限额"
    },
    {
        "用例个数": 4,
        "活动号": "MK20240808214110",
        "关联人群": "24060800100100111100000000102515",
        "activity_rules_updated_fix": {
            "cashbackRule": {
                "type": "percent",
                "calAlg": {
                    "type": "single",
                    "param": "0.07",
                    "rules": []
                },
                "limit": [{
                    # "limitType": "interval",
                    "limitType": "campaignPeriod",
                    # "startDate": "2024-01-29T00:00:00",
                    # "endDate": "2024-03-01T23:59:59",
                    "countLimit": "1",
                }]
            },
            "transactionRule": {}
        },
        "活动规则": {
            "cashbackAmountCalMethod": "percent",
            "cashbackAmountCalParams": "0.07",
            "cashbackMatchRuleType": "rules_engine",
            "cashbackLimit": {},
            "multiCashbacklimit": [
                {
                    "countLimit": {
                        "value": "1"
                    },
                    "timeLineLimit": {
                        "timeType": "interval",
                        "startDate": "2024-01-29T00:00:00",
                        "endDate": "2024-03-01T23:59:59"
                    }
                }
            ]
        },
        "人群规则": {
            "productCode": "STC002",
            "openDate": "2024-01-28T01:00:00",
            "openEndDate": "2024-01-28T01:59:59"
        },
        "规则类型": "时间区间限次"
    },
    {
        "用例个数": 12,
        "活动号": "MK20240229002204",
        "关联人群": "24022900100100111100000000099415",
        "activity_rules_updated_fix": {
            "cashbackRule": {
                "type": "percent",
                "calAlg": {
                    "type": "single",
                    "param": "0.07",
                    "rules": []
                },
                "limit": [{
                    "limitType": "cycle",
                    "amountLimit": "20003"
                }]
            },
            "transactionRule": {}
        },
        "活动规则": {
            "cashbackAmountCalMethod": "percent",
            "cashbackAmountCalParams": "0.07",
            "cashbackMatchRuleType": "rules_engine",
            "cashbackRuleKnowledgeId": "rt_marketing_cashback_beta2",
            "cashbackLimit": {},
            "multiCashbacklimit": [
                {
                    "amountLimit": {
                        "value": "20003"
                    },
                    "timeLineLimit": {
                        "timeType": "cycle"
                    }
                }
            ]
        },
        "人群规则": {
            "productCode": "STC002",
            "openDate": "2024-01-28T04:00:00",
            "openEndDate": "2024-01-28T04:59:59"
        },
        "规则类型": "新模型账期限额"
    },
    {
        "用例个数": 4,
        "活动号": "MK20240804234531",
        "关联人群": "24080400100100111100000000102240",
        "activity_rules_updated_fix": {
            "cashbackRule": {
                "type": "percent",
                "calAlg": {
                    "type": "single",
                    "param": "0.07",
                    "rules": []
                },
                "limit": [{
                    "limitType": "cycle",
                    "countLimit": "1",
                }]
            },
            "transactionRule": {}
        },
        "活动规则": {
            "cashbackAmountCalMethod": "percent",
            "cashbackAmountCalParams": "0.07",
            "cashbackMatchRuleType": "rules_engine",
            "cashbackLimit": {},
            "multiCashbacklimit": [
                {
                    "timeLineLimit": {
                        "timeType": "cycle"
                    },
                    "countLimit": {
                        "value": "1"
                    }
                }
            ]
        },
        "人群规则": {
            "productCode": "STC002",
            "openDate": "2024-01-28T05:00:00",
            "openEndDate": "2024-01-28T05:59:59"
        },
        "规则类型": "新模型账期限次"
    },
    {
        "用例个数": 4,
        "活动号": "MK20240130003923",
        "关联人群": "24013000100100111100000000102786",
        "activity_rules_updated_fix": {
            "cashbackRule": {
                "type": "percent",
                "calAlg": {
                    "type": "single",
                    "param": "0.07",
                    "rules": []
                },
                "limit": [{
                    "limitType": "cycle",
                    "amountLimit": "20003",
                    "countLimit": "2",
                }]
            },
            "transactionRule": {}
        },
        "活动规则": {
            "cashbackAmountCalMethod": "percent",
            "cashbackAmountCalParams": "0.07",
            "cashbackMatchRuleType": "rules_engine",
            "cashbackLimit": {},
            "multiCashbacklimit": [
                {
                    "amountLimit": {
                        "value": "20003"
                    },
                    "countLimit": {
                        "value": "2"
                    },
                    "timeLineLimit": {
                        "timeType": "cycle"
                    }
                }
            ]
        },
        "人群规则": {
            "productCode": "STC002",
            "openDate": "2024-01-28T06:00:00",
            "openEndDate": "2024-01-28T06:59:59"
        },
        "规则类型": "新模型账期限次限额"
    },
    {
        "用例个数": 3,
        "活动号": "MK20220912120028",
        "关联人群": "22102000100100111100000000103327",
        "activity_rules_updated_fix": {
            "cashbackRule": {
                "type": "fixAmount",
                "calAlg": {
                    "type": "single",
                    "param": "10001",
                    "rules": []
                },
                "limit": [{
                    "limitType": "cycle",
                    "countLimit": "1",

                }]
            },
            "transactionRule": {}
        },
        "活动规则": {
            "cashbackAmountCalMethod": "fixAmount",
            "cashbackAmountCalParams": "10001",
            "cashbackMatchRuleType": "rules_engine",
            "cashbackLimit": {},
            "multiCashbacklimit": [
                {
                    "countLimit": {
                        "value": "1"
                    },
                    "timeLineLimit": {
                        "timeType": "cycle"
                    }
                }
            ]
        },
        "人群规则": {
            "productCode": "STC002",
            "openDate": "2024-01-28T07:00:00",
            "openEndDate": "2024-01-28T07:59:59"
        },
        "规则类型": "新模型账期固定金额"
    },
    {
        "用例个数": 13,
        "活动号": "MK20240422035921",
        "关联人群": "24042200100100111100000000099966",
        "activity_rules_updated_fix": {
            "cashbackRule": {
                "type": "percent",
                "calAlg": {
                    "type": "single",
                    "param": "0.07",
                    "rules": []
                },
                "limit": [{
                    "limitType": "cycle",
                    "amountLimit": "20003",

                }]
            },
            "transactionRule": {}
        },
        "活动规则": {
            "cashbackAmountCalMethod": "percent",
            "cashbackAmountCalParams": "0.07",
            "cashbackMatchRuleType": "rules_engine",
            "cashbackLimit": {
                "accountLimit": {
                    "timeLimit": {
                        "timeType": "cycle",
                        "value": "20003"
                    }
                }
            }
        },
        "人群规则": {"productCode": "STC002", "openDate": "2024-04-16T00:00:00", "openEndDate": "2024-04-30T23:59:59"},
        "规则类型": "用户维度规则（以签约时间为计算方式）"
    },
    {
        "用例个数": 8,
        "活动号": "MK20240814041050",
        "关联人群": "24081400100100111100000000103074",
        "activity_rules_updated_fix": {
            "cashbackRule": {
                "type": "percent",
                "calAlg": {
                    "type": "single",
                    "param": "0.07",
                    "rules": []
                },
                "limit": [{
                    "limitType": "campaignPeriod",
                    "amountLimit": "20000"
                }]
            },
            "transactionRule": {}
        },
        "活动规则": {
            "cashbackAmountCalMethod": "percent",
            "cashbackAmountCalParams": "0.07",
            "cashbackMatchRuleType": "rules_engine",
            "cashbackLimit": {},
            "multiCashbacklimit": [
                {
                    "amountLimit": {
                        "value": "20000"
                    }
                }
            ]
        },
        "人群规则": {
            "productCode": "STC002",
            "openDate": "2024-02-28T00:00:00",
            "openEndDate": "2024-02-28T23:59:59"
        },
        "规则类型": "用户维度规则（以CL返现额度）"
    },
    {
        "用例个数": 5,
        "活动号": "MK20221117120358",
        #
        "关联人群": "25011100100100111100000000101556",
        "activity_rules_updated_fix": {
            "cashbackRule": {
                "type": "percent",
                "calAlg": {
                    "type": "single",
                    "param": "0.07",
                    "rules": []
                },
                "limit": [{
                    "limitType": "campaignPeriod",
                    "amountLimit": "20003"
                }]
            },
            "transactionRule": {}
        },
        "活动规则": {
            "cashbackAmountCalMethod": "percent",
            "cashbackAmountCalParams": "0.07",
            "cashbackMatchRuleType": "rules_engine",
            "cashbackLimit": {},
            "multiCashbacklimit": [
                {
                    "amountLimit": {
                        "value": "20003"
                    }
                }
            ]
        },
        "人群规则": {
            "productCode": "STC002",
            "openDate": "2024-01-28T14:00:00",
            "openEndDate": "2024-01-28T14:59:59"
        },
        "规则类型": "活动时间限额"
    },
    {
        "用例个数": 4,
        "活动号": "MK20221127010016",
        "关联人群": "24073000100100111100000000102028",
        "activity_rules_updated_fix": {
            "cashbackRule": {
                "type": "percent",
                "calAlg": {
                    "type": "single",
                    "param": "0.07",
                    "rules": []
                },
                "limit": [{
                    "limitType": "campaignPeriod",
                    "countLimit": "2"
                }]
            },
            "transactionRule": {}
        },
        "活动规则": {
            "cashbackAmountCalMethod": "percent",
            "cashbackAmountCalParams": "0.07",
            "cashbackMatchRuleType": "rules_engine",
            "cashbackLimit": {},
            "multiCashbacklimit": [
                {
                    "countLimit": {
                        "value": "2"
                    }
                }
            ]
        },
        "人群规则": {
            "productCode": "STC002",
            "openDate": "2024-01-28T09:00:00",
            "openEndDate": "2024-01-28T09:59:59"
        },
        "规则类型": "活动时间限次"
    },
    {
        "用例个数": 10,
        "活动号": "MK20240113000023",
        "关联人群": "24072500100100111100000000101556",
        "activity_rules_updated_fix": {
            "cashbackRule": {
                "type": "percent",
                "calAlg": {
                    "type": "single",
                    "param": "0.07",
                    "rules": []
                },
                "limit": [{
                    "limitType": "campaignPeriod",
                    "countLimit": "2",
                    "amountLimit": "20003"
                }]
            },
            "transactionRule": {}
        },
        "活动规则": {
            "cashbackAmountCalMethod": "percent",
            "cashbackAmountCalParams": "0.07",
            "cashbackMatchRuleType": "rules_engine",
            "cashbackLimit": {},
            "multiCashbacklimit": [
                {
                    "amountLimit": {
                        "value": "20003"
                    },
                    "countLimit": {
                        "value": "2"
                    }
                }
            ]
        },
        "人群规则": {
            "productCode": "STC002",
            "openDate": "2024-01-28T08:00:00",
            "openEndDate": "2024-01-28T08:59:59"
        },
        "规则类型": "活动时间限额限次"
    },
    {
        "用例个数": 5,
        "活动号": "MK20221020120452",
        "关联人群": "22102000100100111100000000103326",

        "activity_rules_updated_fix": {
            "cashbackRule": {
                "type": "fixAmount",
                "calAlg": {
                    "type": "single",
                    "param": "10001",
                    "rules": []
                },
                "limit": [{
                    "limitType": "campaignPeriod",
                    "countLimit": "2"
                }]
            },
            "transactionRule": {}
        },
        "活动规则": {"cashbackAmountCalMethod": "fixAmount", "cashbackAmountCalParams": "10001",
                     "cashbackMatchRuleType": "rules_engine", "cashbackLimit": {},
                     "multiCashbacklimit": [{"countLimit": {"value": "2"}}]},
        "人群规则": {
            "productCode": "STC002",
            "openDate": "2024-01-28T10:00:00",
            "openEndDate": "2024-01-28T10:59:59"
        },
        "规则类型": "活动时间固定金额限次"
    },
    {
        "用例个数": 5,
        "活动号": "MK20230918120137",
        "关联人群": "23101000100100111100000000103604",

        "activity_rules_updated_fix": {
            "cashbackRule": {
                "type": "percent",
                "calAlg": {
                    "type": "single",
                    "param": "0.07",
                    "rules": []
                },
                "limit": [{
                    "limitType": "month",
                    "countLimit": "2",
                    "amountLimit": "20003"
                }]
            },
            "transactionRule": {}
        },
        "活动规则": {"cashbackAmountCalMethod": "percent", "cashbackAmountCalParams": "0.07",
                     "cashbackMatchRuleType": "rules_engine", "cashbackLimit": {}, "multiCashbacklimit": [
                {"amountLimit": {"value": "20003"}, "countLimit": {"value": "2"},
                 "timeLineLimit": {"timeType": "month"}}]},
        "人群规则": {
            "productCode": "STC002",
            "openDate": "2024-01-28T15:00:00",
            "openEndDate": "2024-01-28T15:59:59"
        },
        "规则类型": "自然月限额限次"
    },
    {
        "用例个数": 5,
        "活动号": "MK20220911120020",
        "关联人群": "22091000100100111100000000104344",

        "activity_rules_updated_fix": {
            "cashbackRule": {
                "type": "percent",
                "calAlg": {
                    "type": "single",
                    "param": "0.07",
                    "rules": []
                },
                "limit": [{
                    "limitType": "signContract",

                    "amountLimit": "20003"
                }]
            },
            "transactionRule": {}
        },
        "活动规则": {"cashbackAmountCalMethod": "percent", "cashbackAmountCalParams": "0.7",
                     "cashbackMatchRuleType": "rules_engine", "cashbackLimit": {}, "customerCondition": [
                {"limitType": "signContract",
                 "timeLineLimit": {"startDate": "2024-01-27T00:00:00", "endDate": "2024-01-28T23:59:59"}}],
                     "multiCashbacklimit": [{"amountLimit": {"value": "20003"}}]},
        "人群规则": {
            "productCode": "STC002",
            "openDate": "2024-01-28T15:00:00",
            "openEndDate": "2024-01-28T15:59:59"
        },
        "规则类型": "自然月限额限次"
    }
]
# 组合数据
final_data = {}
for get_one in get_data1:
    activityNo = get_one["活动号"]
    crowdNo = get_one["关联人群"]
    openDate = get_one["人群规则"]["openDate"]
    openEndDate = get_one["人群规则"]["openEndDate"]
    activityStartTime = ""
    activityEndTime = ""
    if str(new_get_data[activityNo]).count("interval") > 0 or str(new_get_data[activityNo]).count("signContract") > 0:
        activity_rules = eval(new_get_data[activityNo]["activity_rules"])
        timeLineLimit_list = jsonpath.jsonpath(activity_rules, "$..timeLineLimit")
        timeLineLimit = timeLineLimit_list[0]
        activityStartTime = timeLineLimit["startDate"]
        activityEndTime = timeLineLimit["endDate"]
    else:
        #
        activityStartTime = new_get_data[activityNo]['activity_start_time'].replace(" ", "T")
        activityEndTime = new_get_data[activityNo]['activity_end_time'].replace(" ", "T")
    activityRules = new_get_data[activityNo]["activity_rules"]
    activityName = new_get_data[activityNo]['activity_name']
    activity_rules_updated_fix = get_one["activity_rules_updated_fix"]
    tmp_data = {"activityNo": activityNo, "crowdNo": crowdNo, "openDate": openDate, "openEndDate": openEndDate,
                "activityStartTime": activityStartTime, "activityEndTime": activityEndTime,
                "activityRules": activityRules, "activity_rules_updated_fix": activity_rules_updated_fix,
                "activityName": activityName}
    print(tmp_data)
    final_data[activityNo] = tmp_data

final_data_mapping = {"${cashbackCycleAccountLimitActivityNo}": "MK20240113000013",
                      "${cashbackCycleTimeLimitActivityNo}": "MK20240305002838",
                      "${cashbackIntervalAccountLimitActivityNo}": "MK20240305032943",
                      "${cashbackIntervalTimeLimitActivityNo}": "MK20240808214110",
                      "${cashbackNewCycleAccountLimitActivityNo}": "MK20240229002204",
                      "${cashbackNewCycleTimeLimitActivityNo}": "MK20240804234531",
                      "${cashbackNewCycleAccountTimeLimitActivityNo}": "MK20240130003923",
                      "${cashbackCycleFixAmountTimeLimitActivityNo}": "MK20220912120028",
                      "${cashbackUserCycleAccountLimitActivityNo}": "MK20240422035921",
                      "${cashbackUserAccountLimitActivityNo}": "MK20240814041050",
                      "${cashbackNewAccountLimitActivityNo}": "MK20221117120358",
                      "${cashbackNewTimeLimitActivityNo}": "MK20221127010016",
                      "${cashbackNewAccountTimeLimitActivityNo}": "MK20240113000023",
                      "${cashbackNewFixAmountTimeLimitActivityNo}": "MK20221020120452",
                      "${cashbackMonthAccountTimeLimitActivityNo}": "MK20230918120137",
                      "${cashbackCustomerCondition}": "MK20220911120020"}

is_updated = 0

true = True


def handler_process_data(id, insert_str_data):
    global is_updated
    is_updated = 0

    # 预处理
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    activityNoMappingList = []
    for get_one_step in result['hashTree']:
        if str(get_one_step).count("${cashback") > 0 and get_one_step['enable'] == True and get_one_step[
            'referenced'] != "REF":
            pattern = r'\$\{cash[a-zA-Z]+\}'
            get_find = re.findall(pattern, str(get_one_step))
            print(get_find)
            # 可能会有bug,找规律
            for get_one_str_info in get_find:
                if str(get_one_str_info).count("ActivityNo") > 0:
                    activityNoMappingList.append(get_one_str_info)

    # todo
    list1 = list(final_data_mapping.keys())
    intersection = [item for item in list1 if item in activityNoMappingList]
    get_activity_no = final_data_mapping[intersection[-1]]
    get_one_acitivity_all_data = final_data[get_activity_no]
    activity_rules_updated_fix = get_one_acitivity_all_data["activity_rules_updated_fix"]
    activity_rules_updated_fix_string = json.dumps(json.dumps(json.dumps(activity_rules_updated_fix)))
    activityName = get_one_acitivity_all_data["activityName"]
    get_insert_tmp_string = (
        (str(insert_str_data).replace("${activityStartTime_replace}", get_one_acitivity_all_data['activityStartTime'])
         .replace("${activityEndTime_replace}", get_one_acitivity_all_data['activityEndTime']))
        .replace("${activityRules_replace}", activity_rules_updated_fix_string)
        .replace("${activityName}", activityName)
        .replace("activity_no_vars_replace", str(intersection[-1]).replace("${", "").replace("}", ""))

        .replace("${crowd_no_vars_replace}", get_one_acitivity_all_data['crowdNo']))
    get_insert_tmp_string1 = get_insert_tmp_string.replace('\"""', '"').replace("\"\"\\\"", '"')
    get_insert_tmp_string1 = get_insert_tmp_string1
    get_insert_data = eval(get_insert_tmp_string1)
    hashTree = result['hashTree']
    for index, get_one_step in enumerate(hashTree):
        if str(get_one_step["name"]).count("创建人群和返现") > 0:
            hashTree.insert(index, get_insert_data)
            is_updated = 1
            break
    for i, get_data in enumerate(hashTree):
        hashTree[i]["index"] = i + 1
    # fibonacci_handler(result, get_insert_tmp)
    # todo
    result['hashTree'] = hashTree
    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]

    if is_updated == 1:
        print("had updated")
        get_info_udpate = MetersphereUtils.update_scenario_detail(get_post_data)
        print(get_info_udpate)
    else:
        print("no need to update")


if __name__ == '__main__':

    get_module_id =[
  "0097dd1f-b2fb-4207-beef-0974bba136f1"
]
    get_ids = MetersphereUtils.get_batch_ids(1, 50, get_module_id)
    # 要插入的数据
    # get_ids=["75d65826-4688-4c06-b501-ff26cbcf2c96"]
    fix_id = "54f70004-cf95-4db3-bde1-57f083d7bcc0"
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(fix_id) if fix_id.isdigit() else fix_id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    insert_str_data = result
    insert_str_data['referenced'] = 'Copy'
    for get_id in get_ids:
        handler_process_data(get_id, insert_str_data)
