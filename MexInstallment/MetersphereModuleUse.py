import json

from ColInstallment import ColScenarioHandler
from MexInstallment import MetersphereUtils

#模块化 组装用例
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

def module_combine(result):
    hash_tree_list = []
    # 3655a904-6b4c-4afb-99a3-a4a41bbf6a35
    hash_tree_1 = MetersphereUtils.get_scenario_list(["2cebfeb3-1805-4a93-bbb1-5bade52451f4"])[0]
    hash_tree_1 = json.loads(hash_tree_1["scenarioDefinition"])
    update("scenarioDefinition", hash_tree_1)
    hash_tree_list.append(hash_tree_1)
    # hash_tree_2 = MetersphereUtils.get_scenario_list(["1eefc592-4db0-4098-9aff-87ba14bd174e"])[0]
    # hash_tree_2 = json.loads(hash_tree_2["scenarioDefinition"])
    # update("scenarioDefinition", hash_tree_2)
    # hash_tree_list.append(hash_tree_2)


    return hash_tree_list

if __name__ == '__main__':
    ########新建场景
    # post_data={"principal": "admin", "apiScenarioModuleId": "0fb10472-44f4-4544-a1c6-54de82cfb218", "follows": [],
    #  "modulePath": "/墨西哥分期/数据准备/断言&DB操作", "name": "test_for1",
    #  "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb", "id": "16c9fb27", "status": "Underway", "level": "P0",
    #  "bodyFileRequestIds": [], "scenarioFileIds": []}
    # get_result=MetersphereUtils.create(post_data)
    # print(get_result)

    data = ColScenarioHandler.get_scenario_detail_all_info("3d333c4a-d599-4b3b-b36b-04a9d1fe87b1")
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    #####前置

    #######组合
    hash_tree_list=module_combine(result)




    ########update场景
    # todo
    result["hashTree"]=hash_tree_list[0]["hashTree"]

    data["data"]["scenarioDefinition"] = result
    # data["data"]["scenarioDefinition"] = json.dumps(result, ensure_ascii=False)
    get_post_data = data["data"]


    get_update_info=MetersphereUtils.update(get_post_data)
    print("*************")
    print(get_update_info)

