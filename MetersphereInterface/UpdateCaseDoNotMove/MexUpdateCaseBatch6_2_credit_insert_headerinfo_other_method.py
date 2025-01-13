import json
import re

from jsonpath import jsonpath

from MetersphereInterface import MetersphereUtils


def update(key, dict_data):
    # 判断需要修改的key是否在初始字典中，在则修改
    if key in dict_data:
        # 将key为'gg'的值修改成'张三'
        # dict_data[key]='张三'
        dict_data["hashTree"] = json.loads(dict_data[key])
        del dict_data[key]
        # print(dict_data)
        # 循环字典获取到所有的key值和value值
        for keys, values in dict_data.items():
            # 判断valus值是否为列表或者元祖
            if isinstance(values, (list, tuple)):
                # 循环获取列表中的值
                for i in values:
                    # 判断需要修改的值是否在上一个循环出的结果中，在则修改
                    if key in i and isinstance(i, dict):
                        # 调用自身修改函数，将key的值修改成'张三'
                        update(key, i)
                    # else:
                    #     #否者则调用获取value函数
                    #     get_value(i)
            elif isinstance(values, dict):
                if key in values:
                    update(key, values)
                else:
                    for keys, values in values.items():
                        if isinstance(values, dict):
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


def only_find(get_data,insert_hash_tree_data):
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
        print(get_data["path"])
        if str(get_data["path"]).count("v1.0")>0:
            headers = list(get_data["headers"])
            get_headers_len=len(headers)
            if get_headers_len>0 and headers[get_headers_len-1]["valid"]==False:
                headers.pop(get_headers_len-1)
                headers.append(insert_hash_tree_data)
            else:
                headers.append(insert_hash_tree_data)
            get_data["headers"]=headers
            print("chuli ")

    if get_data["type"] == "scenario" and get_data["enable"] == True and (get_data['referenced']=="Copy" or get_data['referenced']=='Created'):
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            only_find(subScenario,insert_hash_tree_data)


def get_batch_id_list(module_ids):
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50, module_ids)
    return get_batch_ids


def fibonacci_handler(result, insert_hash_tree_data):
    hashTree = result["hashTree"]
    only_find(result,insert_hash_tree_data)
    result["hashTree"] = hashTree


def handler_process_data(id, insert_hash_tree_data):
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    # todo
    fibonacci_handler(result, insert_hash_tree_data)

    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]
    # get_daa=json.dumps(get_post_data)
    get_info_udpate = MetersphereUtils.update_scenario_detail(get_post_data)
    print(get_info_udpate)


if __name__ == '__main__':
    # 输入用例id
    module_id = [
        "9aa6c422-d881-4fd5-952c-2c4ad5896ee2"
    ]
    get_ids = get_batch_id_list(module_id)
    get_ids = ["e4de14f4-4675-4c78-a177-3b6bec48ea5b"]
    for get_id in get_ids:
        handler_process_data(get_id, {'enable': True, 'file': False, 'name': 'X-Customer-Id', 'required': True,
                                      'urlEncode': False, 'valid': True, 'value': '${X-Customer-Id}'})
