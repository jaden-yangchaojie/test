import json
import re
import time

from MetersphereInterface import MetersphereUtils


def get_batch_id(module_id):
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50, [
        module_id
    ])
    return get_batch_ids


def get_batch_id(module_id_list):
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50, module_id_list)
    return get_batch_ids


def handler_process_data(id, insert_hash_tree_data):
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")


    result = json.loads(get_sce_data)
    hashTree = list(result["hashTree"])
    for i,get_data_1 in enumerate(hashTree):
        if str(get_data_1['name']).count("用户签约（数据驱动模式）-单库单表")>0:
            get_index=hashTree[i]["index"]
            hashTree[i]["parentIndex"]=get_index
            hashTree[i]["domain"]=""
            hashTree[i]["checkBox"]=False
            hashTree[i]["isBatchProcess"]=False
            hashTree[i]["isLeaf"]=False
            hashTree[i]["disabled"]=True
            hashTree[i]["showExtend"]=True
            for k,get_data_2 in enumerate(hashTree[i]["hashTree"]):
                if 'name' in get_data_2 and str(get_data_2['name']).count("如果签约重试之后成功，则可忽略该步骤的校验")>0:
                    get_data_2['doMultipartPost']=bool(False)
                    get_data_2['parentIndex']=str(str(get_index)+"_1")
                    get_data_2["checkBox"]=bool(False)
                    get_data_2["isBatchProcess"]=bool(False)
                    get_data_2["isLeaf"]=bool(True)
                    get_data_2["disabled"]=bool(True)
                    get_data_2["caseEnable"]=bool(True)
                    get_data_2["deleted"]=bool(False)
                    hashTree[i]["hashTree"][k]=get_data_2

    result["hashTree"] = hashTree
    data["data"]["scenarioDefinition"] = result
    variables = list(result['variables'])
    for i, get_bas in enumerate(variables):
        variables[i]["num"] = i + 1
    data["data"]['variables'] = result['variables']
    # version=data["data"]['version']
    # version = version + 1
    # data["data"]['version']=version
    data["data"]["updateTime"] = int(time.time() * 1000)
    get_post_data = data["data"]
    data["data"]["env"]="{\"11406dc7-8340-401f-813f-3511a97d3fbb\":\"343ca1b7-f080-4f5d-ad65-867e3308f2b7\"}"
    data["data"]["environmentMap"] ={"core-banking":"qa-test-dfl-marketing-new"}
    data["data"]["scheduleObj"] = {
        "scheduleStatus": "",
        "scheduleCorn": "",
        "scheduleExecuteTime": "",
        "enable": False,
        "id": "",
        "resourceId": data["data"]['refId']
    }
    data["data"]['projectName']="core-banking"
    data["data"]['userName']="Administrator"
    data["data"]['creatorName'] = "Administrator"
    data["data"]['principalName'] = "Administrator"
    data["data"]['projectName'] = "core-banking"
    data["data"]['versionEnable'] = None

    get_info_udpate = MetersphereUtils.update_scenario_detail(get_post_data)
    print(get_info_udpate)
    get_pdsi=json.loads(get_info_udpate.text)
    get_get = get_pdsi.get("data").get("scenarioDefinition")
    result1 = json.loads(get_get)
    print(result1)


if __name__ == '__main__':

    insert_hash_tree_data = []
    get_ids = ["af012843-886d-4b09-a493-3424e7689706"]
    for get_id in get_ids:
        handler_process_data(get_id, insert_hash_tree_data)
