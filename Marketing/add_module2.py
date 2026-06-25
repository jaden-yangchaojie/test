import json

import jsonpath

from MetersphereInterface import MetersphereUtils

null=None

# result_data=     {
#                     "id": "3f646930-dc33-4329-b497-e2fd6182c3bd",
#                     "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
#                     "name": "返现集成测试",
#                     "parentId": "e510c91b-f33a-4738-8c5c-1b69a0ba1d00",
#                     "level": 2,
#                     "createTime": 1707027867604,
#                     "updateTime": 1750400326805,
#                     "pos": 262144.0,
#                     "label": "返现集成测试",
#                     "children": [
#                         {
#                             "id": "bf111fb8-f316-4a68-83fd-02e684479c7a",
#                             "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
#                             "name": "账期限额",
#                             "parentId": "3f646930-dc33-4329-b497-e2fd6182c3bd",
#                             "level": 3,
#                             "createTime": 1709185958424,
#                             "updateTime": 1715594861496,
#                             "pos": 65536.0,
#                             "label": "账期限额",
#                             "children": null,
#                             "caseNum": 13,
#                             "path": null
#                         },
#                         {
#                             "id": "58bf522b-2632-426b-bb54-8325807a9f96",
#                             "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
#                             "name": "账期限次",
#                             "parentId": "3f646930-dc33-4329-b497-e2fd6182c3bd",
#                             "level": 3,
#                             "createTime": 1709521805781,
#                             "updateTime": 1742801236906,
#                             "pos": 131072.0,
#                             "label": "账期限次",
#                             "children": null,
#                             "caseNum": 5,
#                             "path": null
#                         },
#                         {
#                             "id": "34873885-38a9-4cc2-af68-fda6a164452d",
#                             "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
#                             "name": "时间区间内限额",
#                             "parentId": "3f646930-dc33-4329-b497-e2fd6182c3bd",
#                             "level": 3,
#                             "createTime": 1709629508211,
#                             "updateTime": 1709629508211,
#                             "pos": 196608.0,
#                             "label": "时间区间内限额",
#                             "children": null,
#                             "caseNum": 10,
#                             "path": null
#                         },
#                         {
#                             "id": "5b3618f1-87d5-443b-8112-d0cb656724ce",
#                             "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
#                             "name": "时间区间内限次",
#                             "parentId": "3f646930-dc33-4329-b497-e2fd6182c3bd",
#                             "level": 3,
#                             "createTime": 1723173506569,
#                             "updateTime": 1743402907204,
#                             "pos": 229376.0,
#                             "label": "时间区间内限次",
#                             "children": null,
#                             "caseNum": 4,
#                             "path": null
#                         },
#                         {
#                             "id": "23dc3fed-e2a9-4f3f-8cbc-64dde5c9d488",
#                             "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
#                             "name": "新模型账期限额",
#                             "parentId": "3f646930-dc33-4329-b497-e2fd6182c3bd",
#                             "level": 3,
#                             "createTime": 1710395860692,
#                             "updateTime": 1710395860692,
#                             "pos": 262144.0,
#                             "label": "新模型账期限额",
#                             "children": null,
#                             "caseNum": 12,
#                             "path": null
#                         },
#                         {
#                             "id": "7c4c140c-24fd-4160-9cb6-d544c891535d",
#                             "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
#                             "name": "新模型账期限次",
#                             "parentId": "3f646930-dc33-4329-b497-e2fd6182c3bd",
#                             "level": 3,
#                             "createTime": 1712909441855,
#                             "updateTime": 1712909441855,
#                             "pos": 327680.0,
#                             "label": "新模型账期限次",
#                             "children": null,
#                             "caseNum": 4,
#                             "path": null
#                         },
#                         {
#                             "id": "e1949d36-fcd7-4329-bccd-7ee08c680174",
#                             "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
#                             "name": "新模型账期限次限额",
#                             "parentId": "3f646930-dc33-4329-b497-e2fd6182c3bd",
#                             "level": 3,
#                             "createTime": 1723534108593,
#                             "updateTime": 1724901628277,
#                             "pos": 360448.0,
#                             "label": "新模型账期限次限额",
#                             "children": null,
#                             "caseNum": 4,
#                             "path": null
#                         },
#                         {
#                             "id": "ac885d9e-1077-4f2b-8618-389edb5a69c7",
#                             "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
#                             "name": "新模型账期固定金额限次",
#                             "parentId": "3f646930-dc33-4329-b497-e2fd6182c3bd",
#                             "level": 3,
#                             "createTime": 1723779041159,
#                             "updateTime": 1724051297553,
#                             "pos": 376832.0,
#                             "label": "新模型账期固定金额限次",
#                             "children": null,
#                             "caseNum": 3,
#                             "path": null
#                         },
#                         {
#                             "id": "04aaf7bd-892e-4693-a300-3a5defcc10b7",
#                             "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
#                             "name": "用户维度规则",
#                             "parentId": "3f646930-dc33-4329-b497-e2fd6182c3bd",
#                             "level": 3,
#                             "createTime": 1713773207887,
#                             "updateTime": 1724051298364,
#                             "pos": 393216.0,
#                             "label": "用户维度规则",
#                             "children": [
#                                 {
#                                     "id": "7ac954ee-91b6-4727-b97c-7b6a9fdeb7f2",
#                                     "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
#                                     "name": "以签约时间为计算返现有效期",
#                                     "parentId": "04aaf7bd-892e-4693-a300-3a5defcc10b7",
#                                     "level": 4,
#                                     "createTime": 1713773274690,
#                                     "updateTime": 1714361458990,
#                                     "pos": 65536.0,
#                                     "label": "以签约时间为计算返现有效期",
#                                     "children": null,
#                                     "caseNum": 13,
#                                     "path": null
#                                 },
#                                 {
#                                     "id": "b2fa4d8f-060f-4b75-b1ed-f231291f4c9c",
#                                     "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
#                                     "name": "以CL为返现额度",
#                                     "parentId": "04aaf7bd-892e-4693-a300-3a5defcc10b7",
#                                     "level": 4,
#                                     "createTime": 1713773299696,
#                                     "updateTime": 1713773318196,
#                                     "pos": 131072.0,
#                                     "label": "以CL为返现额度",
#                                     "children": null,
#                                     "caseNum": 8,
#                                     "path": null
#                                 }
#                             ],
#                             "caseNum": 21,
#                             "path": null
#                         },
#                         {
#                             "id": "2d18b60f-d9f4-4350-9f71-8f47af280d43",
#                             "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
#                             "name": "活动时间限额",
#                             "parentId": "3f646930-dc33-4329-b497-e2fd6182c3bd",
#                             "level": 3,
#                             "createTime": 1714372610206,
#                             "updateTime": 1714372610206,
#                             "pos": 458752.0,
#                             "label": "活动时间限额",
#                             "children": null,
#                             "caseNum": 5,
#                             "path": null
#                         },
#                         {
#                             "id": "75674695-3926-4843-b950-511aa6c998b0",
#                             "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
#                             "name": "活动时间限次",
#                             "parentId": "3f646930-dc33-4329-b497-e2fd6182c3bd",
#                             "level": 3,
#                             "createTime": 1714372619522,
#                             "updateTime": 1714372619522,
#                             "pos": 524288.0,
#                             "label": "活动时间限次",
#                             "children": null,
#                             "caseNum": 4,
#                             "path": null
#                         },
#                         {
#                             "id": "d1846ff5-de8e-46c8-8966-a02b6ed544f3",
#                             "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
#                             "name": "活动时间限额限次",
#                             "parentId": "3f646930-dc33-4329-b497-e2fd6182c3bd",
#                             "level": 3,
#                             "createTime": 1721877281643,
#                             "updateTime": 1722222401576,
#                             "pos": 589824.0,
#                             "label": "活动时间限额限次",
#                             "children": null,
#                             "caseNum": 10,
#                             "path": null
#                         },
#                         {
#                             "id": "5a051b3c-fa96-4a6d-a6f9-5ae6c502c8a9",
#                             "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
#                             "name": "活动时间固定金额限次",
#                             "parentId": "3f646930-dc33-4329-b497-e2fd6182c3bd",
#                             "level": 3,
#                             "createTime": 1723776059114,
#                             "updateTime": 1723776059114,
#                             "pos": 655360.0,
#                             "label": "活动时间固定金额限次",
#                             "children": null,
#                             "caseNum": 5,
#                             "path": null
#                         },
#                         {
#                             "id": "f6a947be-1886-4405-8a14-7bd07ba3bee5",
#                             "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
#                             "name": "自然月限额限次",
#                             "parentId": "3f646930-dc33-4329-b497-e2fd6182c3bd",
#                             "level": 3,
#                             "createTime": 1724901642885,
#                             "updateTime": 1724901642885,
#                             "pos": 720896.0,
#                             "label": "自然月限额限次",
#                             "children": null,
#                             "caseNum": 3,
#                             "path": null
#                         },
#                         {
#                             "id": "249853ab-6860-4726-9670-447142620f38",
#                             "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
#                             "name": "根据签约范围添加活动返现资格",
#                             "parentId": "3f646930-dc33-4329-b497-e2fd6182c3bd",
#                             "level": 3,
#                             "createTime": 1732593060342,
#                             "updateTime": 1732593071041,
#                             "pos": 786432.0,
#                             "label": "根据签约范围添加活动返现资格",
#                             "children": null,
#                             "caseNum": 3,
#                             "path": null
#                         }
#                     ],
#                     "caseNum": 115,
#                     "path": null
#                 }
# get_object_list=jsonpath.jsonpath(result_data,"$..name")
# print(get_object_list)
get_list_data = MetersphereUtils.module_list()
dict_data_list=[]
get_level1 = jsonpath.jsonpath(get_list_data,"$.data.[?(@.name=='营销')].children[?(@.name=='redemption集成测试new关闭mock')].children.[id,name,parentId,level,label])")
print(get_level1)
num = len(get_level1)
for i, get_one in enumerate(get_level1):
    if i < num - 1 and i % 4 == 0:

        dict_data_list.append({"id": get_level1[i], "name": get_level1[i + 1],"parentId":get_level1[i + 2],"level":get_level1[i + 3]})

print(dict_data_list)
for get_one in dict_data_list:
    print(str({ str(get_one["id"]):str(get_one["name"])})+str(","))
# parentId="320f2f60-ab7e-4cfa-b341-d3e566c417f1"
# for get_one in dict_data_list:
#     MetersphereUtils.add_module(get_one["level"],parentId,get_one["name"])


result_data1={
                    "id": "3908bb07-db8b-428a-a491-4829339f8983",
                    "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                    "name": "redemption集成测试",
                    "parentId": "e510c91b-f33a-4738-8c5c-1b69a0ba1d00",
                    "level": 2,
                    "createTime": 1722845515485,
                    "updateTime": 1722845555601,
                    "pos": 458752.0,
                    "label": "redemption集成测试",
                    "children": [
                        {
                            "id": "ad23325c-292e-4c98-b0eb-adb5b65beab5",
                            "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                            "name": "账期限额",
                            "parentId": "3908bb07-db8b-428a-a491-4829339f8983",
                            "level": 3,
                            "createTime": 1722845574932,
                            "updateTime": 1722845574932,
                            "pos": 65536.0,
                            "label": "账期限额",
                            "children": null,
                            "caseNum": 11,
                            "path": null
                        },
                        {
                            "id": "32f262dc-16fe-41f7-abfd-abb52755077a",
                            "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                            "name": "账期限次",
                            "parentId": "3908bb07-db8b-428a-a491-4829339f8983",
                            "level": 3,
                            "createTime": 1724046676809,
                            "updateTime": 1724046676809,
                            "pos": 131072.0,
                            "label": "账期限次",
                            "children": null,
                            "caseNum": 3,
                            "path": null
                        },
                        {
                            "id": "49372faa-695a-4add-aa5e-b7a92d4fa86b",
                            "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                            "name": "账期限额限次",
                            "parentId": "3908bb07-db8b-428a-a491-4829339f8983",
                            "level": 3,
                            "createTime": 1724067187175,
                            "updateTime": 1724067187175,
                            "pos": 196608.0,
                            "label": "账期限额限次",
                            "children": null,
                            "caseNum": 3,
                            "path": null
                        },
                        {
                            "id": "3653b516-2c90-4922-a409-3072a47c5665",
                            "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                            "name": "账期固定金额限次",
                            "parentId": "3908bb07-db8b-428a-a491-4829339f8983",
                            "level": 3,
                            "createTime": 1724121135982,
                            "updateTime": 1724121135982,
                            "pos": 262144.0,
                            "label": "账期固定金额限次",
                            "children": null,
                            "caseNum": 4,
                            "path": null
                        },
                        {
                            "id": "00c67fd5-26ba-40a8-857b-0446a3325cf9",
                            "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                            "name": "区间限次",
                            "parentId": "3908bb07-db8b-428a-a491-4829339f8983",
                            "level": 3,
                            "createTime": 1724124897477,
                            "updateTime": 1724124897477,
                            "pos": 327680.0,
                            "label": "区间限次",
                            "children": null,
                            "caseNum": 4,
                            "path": null
                        },
                        {
                            "id": "1a507c10-ee53-40d5-a345-d3fc485e14c4",
                            "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                            "name": "区间限额",
                            "parentId": "3908bb07-db8b-428a-a491-4829339f8983",
                            "level": 3,
                            "createTime": 1724134876270,
                            "updateTime": 1724134876270,
                            "pos": 393216.0,
                            "label": "区间限额",
                            "children": null,
                            "caseNum": 4,
                            "path": null
                        },
                        {
                            "id": "dbab2217-17cf-4568-bca4-97478f835319",
                            "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                            "name": "活动限额",
                            "parentId": "3908bb07-db8b-428a-a491-4829339f8983",
                            "level": 3,
                            "createTime": 1724146082315,
                            "updateTime": 1724146082315,
                            "pos": 458752.0,
                            "label": "活动限额",
                            "children": null,
                            "caseNum": 6,
                            "path": null
                        },
                        {
                            "id": "751eba06-a992-469b-a76f-879581fe12bc",
                            "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                            "name": "活动限次",
                            "parentId": "3908bb07-db8b-428a-a491-4829339f8983",
                            "level": 3,
                            "createTime": 1724146088131,
                            "updateTime": 1724146088131,
                            "pos": 524288.0,
                            "label": "活动限次",
                            "children": null,
                            "caseNum": 5,
                            "path": null
                        },
                        {
                            "id": "32b769a2-330a-44e5-8e4c-c9627ca014b6",
                            "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                            "name": "活动限额限次",
                            "parentId": "3908bb07-db8b-428a-a491-4829339f8983",
                            "level": 3,
                            "createTime": 1724146095039,
                            "updateTime": 1724146095039,
                            "pos": 589824.0,
                            "label": "活动限额限次",
                            "children": null,
                            "caseNum": 8,
                            "path": null
                        },
                        {
                            "id": "02a5e826-191d-46ec-b129-6580ccfbdd82",
                            "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                            "name": "活动固定金额限次",
                            "parentId": "3908bb07-db8b-428a-a491-4829339f8983",
                            "level": 3,
                            "createTime": 1724146107144,
                            "updateTime": 1724146107144,
                            "pos": 655360.0,
                            "label": "活动固定金额限次",
                            "children": null,
                            "caseNum": 5,
                            "path": null
                        },
                        {
                            "id": "585018d8-65f0-4d07-8c71-09f8577e0e61",
                            "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                            "name": "用户维度规则",
                            "parentId": "3908bb07-db8b-428a-a491-4829339f8983",
                            "level": 3,
                            "createTime": 1724220594643,
                            "updateTime": 1724220594643,
                            "pos": 720896.0,
                            "label": "用户维度规则",
                            "children": [
                                {
                                    "id": "9467c339-b1eb-4c86-9034-45df6c26d14c",
                                    "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                                    "name": "用户维度返现有效期",
                                    "parentId": "585018d8-65f0-4d07-8c71-09f8577e0e61",
                                    "level": 4,
                                    "createTime": 1724220607174,
                                    "updateTime": 1724229664372,
                                    "pos": 65536.0,
                                    "label": "用户维度返现有效期",
                                    "children": null,
                                    "caseNum": 7,
                                    "path": null
                                },
                                {
                                    "id": "cfded6de-8bb6-4e98-8939-71060a550581",
                                    "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                                    "name": "用户维度限额",
                                    "parentId": "585018d8-65f0-4d07-8c71-09f8577e0e61",
                                    "level": 4,
                                    "createTime": 1724220617653,
                                    "updateTime": 1724220617653,
                                    "pos": 131072.0,
                                    "label": "用户维度限额",
                                    "children": null,
                                    "caseNum": 7,
                                    "path": null
                                }
                            ],
                            "caseNum": 14,
                            "path": null
                        },
                        {
                            "id": "15c2fae4-1a3a-4b39-b816-7c2c1e775282",
                            "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                            "name": "自然月限额限次",
                            "parentId": "3908bb07-db8b-428a-a491-4829339f8983",
                            "level": 3,
                            "createTime": 1724913133961,
                            "updateTime": 1724913133961,
                            "pos": 786432.0,
                            "label": "自然月限额限次",
                            "children": null,
                            "caseNum": 3,
                            "path": null
                        }
                    ],
                    "caseNum": 70,
                    "path": null
                },