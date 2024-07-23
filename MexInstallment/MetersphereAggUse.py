
import json
import time
from datetime import datetime

from ColInstallment import ColScenarioHandler
from MexInstallment import MetersphereUtils
import jsonpickle
key = 'scenarioDefinition'
def update(key,dict_data):
    #判断需要修改的key是否在初始字典中，在则修改
    if key in dict_data:
        #将key为'gg'的值修改成'张三'
        # dict_data[key]='张三'
        dict_data["hashTree"] = json.loads(dict_data[key])
        del dict_data[key]
        #print(dict_data)
        #循环字典获取到所有的key值和value值
        for keys,values in dict_data.items():
            #判断valus值是否为列表或者元祖
            if isinstance(values,(list,tuple)):
                #循环获取列表中的值
                for i in values:
                    #判断需要修改的值是否在上一个循环出的结果中，在则修改
                    if key in i and isinstance(i,dict):
                        #调用自身修改函数，将key的值修改成'张三'
                        update(key,i)
                    # else:
                    #     #否者则调用获取value函数
                    #     get_value(i)
            elif isinstance(values,dict):
                if key in values:
                    update(key,values)
                else:
                    for keys,values in values.items():
                        if isinstance(values,dict):
                            update(key, values)
    else:
        # 循环获取原始字典的values值
        for keys, values in dict_data.items():
            # 判断values值是否是列表或者元祖
            if isinstance(values, (list, tuple)):
                # 如果是列表或者元祖则循环获取里面的元素值
                for i in values:
                    # 判断需要修改的key是否在元素中
                    if key in i:
                        # 调用修改函数修改key的值
                        update(key, i)
                    # else:
                    #     # 否则调用获取values的值函数
                    #     get_value(i)
            # 判断values值是否为字典
            elif isinstance(values, dict):
                # 判断需要修改的key是否在values中
                if key in values:
                    # 调用修改函数修改key的值
                    update(key, values)
                # else:
                #     # 获取values值的函数
                #     get_value(values)
    return dict_data

def fibonacci(get_data, dds):

    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
        get_path = get_data["path"]
        get_body = get_data["body"]
        if get_data["path"] == "/api/admin/system/faketime":
            get_raw = json.loads(get_data["body"]["raw"])
            if str(get_raw["time"]).count("__timeShift") > 0:
                print()
            else:
                dds.append(get_raw["time"])
    # if get_data["type"]=="JDBCSampler" and get_data["enable"] == True:
    #     get_sql = get_data["query"]
    #     if str(get_sql).count(" set ")>0:
    #         get_dict = {"path":"update_sql","update_sql":  get_sql}
    #         dds.append(get_dict)

    elif get_data["type"] == "scenario" and get_data["enable"] == True:
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            fibonacci(subScenario, dds)

def fibonacci1(get_data, get_time_collection):

    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
        if get_data["path"] == "/api/admin/system/faketime":
            get_raw = json.loads(get_data["body"]["raw"])
            if str(get_raw["time"]).count("__timeShift") > 0:
                print()
            get_time_collection.append(get_raw["time"])


    if get_data["type"]=="JDBCSampler" and get_data["enable"] == True:
        print()

    elif get_data["type"] == "scenario" and get_data["enable"] == True:
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            fibonacci(subScenario, get_time_collection)
if __name__ == '__main__':
    ########聚合
    data = ColScenarioHandler.get_scenario_detail_all_info("3d333c4a-d599-4b3b-b36b-04a9d1fe87b1")
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    #####前置
    ######
    hash_tree_list = []
    # 3655a904-6b4c-4afb-99a3-a4a41bbf6a35
    hash_tree_1 = MetersphereUtils.get_scenario_list(["3655a904-6b4c-4afb-99a3-a4a41bbf6a35"])[0]
    hash_tree_1 = json.loads(hash_tree_1["scenarioDefinition"])
    update("scenarioDefinition", hash_tree_1)

    hash_tree_2 = MetersphereUtils.get_scenario_list(["8ef443b6-afcb-4356-a01c-169359bb4a5e"])[0]
    hash_tree_2 = json.loads(hash_tree_2["scenarioDefinition"])
    update("scenarioDefinition", hash_tree_2)
    get_time_line=[]
    #混合
    fibonacci(hash_tree_1,get_time_line)
    #'未出账退款（多笔多期）-多笔未出账&全额退款'
    fibonacci(hash_tree_2, get_time_line)
    get_time_line=set(get_time_line)
    get_time_line=list(get_time_line)
    get_time_line.sort()
    print(get_time_line)
    get_time_line.append("2099-02-02 00:00:00")
    for i,get_time in enumerate(get_time_line):
        if i < len(get_time_line)-1:
            next_get_time=get_time_line[i + 1]

            get_fa = False
            for get_sub_hashTree in hash_tree_1["hashTree"]:
                if json.dumps(get_sub_hashTree).count(get_time_line[i]) > 0 and json.dumps(get_sub_hashTree).count(
                        "/api/admin/system/faketime") > 0:
                    get_time_collection = []
                    fibonacci1(get_sub_hashTree, get_time_collection)
                    if len(get_time_collection)>0:
                        get_fa = True
                        hash_tree_list.append(get_sub_hashTree)

                elif json.dumps(get_sub_hashTree).count("/api/admin/system/faketime") > 0 and get_fa == True:
                    get_time_collection = []
                    fibonacci1(get_sub_hashTree, get_time_collection)
                    if len(get_time_collection)>0:
                        # time_1 = time.strftime("%Y-%m-%d %H:%M:%S", )
                        time_1 = time.mktime(time.strptime(get_time_collection[0], '%Y-%m-%d %H:%M:%S'))
                        # time_2 = time.strftime("%Y-%m-%d %H:%M:%S", next_get_time)
                        time_2 = time.mktime(time.strptime(next_get_time, '%Y-%m-%d %H:%M:%S'))

                        if time_1 >= time_2:
                            get_fa = False
                            break
                elif get_fa == True:
                    hash_tree_list.append(get_sub_hashTree)
            # get_fa = False
            # for get_sub_hashTree in hash_tree_2["hashTree"]:
            #     if json.dumps(get_sub_hashTree).count(get_time_line[i]) > 0 and json.dumps(get_sub_hashTree).count(
            #             "/api/admin/system/faketime") > 0:
            #         get_time_collection = []
            #         fibonacci1(get_sub_hashTree, get_time_collection)
            #         if len(get_time_collection) > 0:
            #             get_fa = True
            #             hash_tree_list.append(get_sub_hashTree)
            #     elif json.dumps(get_sub_hashTree).count("/api/admin/system/faketime") > 0 and get_fa == True:
            #         get_time_collection = []
            #         fibonacci1(get_sub_hashTree, get_time_collection)
            #
            #         if len(get_time_collection) > 0:
            #             # time_1 = time.strftime("%Y-%m-%d %H:%M:%S", )
            #             time_1 = time.mktime(time.strptime(get_time_collection[0], '%Y-%m-%d %H:%M:%S'))
            #             # time_2 = time.strftime("%Y-%m-%d %H:%M:%S", next_get_time)
            #             time_2 = time.mktime(time.strptime(next_get_time, '%Y-%m-%d %H:%M:%S'))
            #
            #             if time_1 >= time_2:
            #                 get_fa = False
            #                 break
            #     elif get_fa == True:
            #         hash_tree_list.append(get_sub_hashTree)








    ########update场景
    # todo
    result["hashTree"]=hash_tree_list

    data["data"]["scenarioDefinition"] = result
    # data["data"]["scenarioDefinition"] = json.dumps(result, ensure_ascii=False)
    get_post_data = data["data"]
    get_update_info=MetersphereUtils.update(get_post_data)
    print("*************")
    print(get_update_info)

