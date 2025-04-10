import json
import re

from MetersphereInterface import MetersphereUtils

def get_batch_id(module_id):
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50,[
  module_id
])
    return get_batch_ids
def get_batch_id_list(module_ids):
    get_batch_ids = MetersphereUtils.get_batch_ids(1, 50,module_ids)
    return get_batch_ids
# def handler_update_name(id):
#     scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
#     data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
#
#     get_sce_data = data.get("data").get("scenarioDefinition")
#     result = json.loads(get_sce_data)
#     result["name"] = "dfl逾期DQ操作1"
#     data["data"]["scenarioDefinition"] = result
#     data["data"]["name"] = "dfl逾期DQ操作1"
#     get_post_data = data["data"]
#     # get_daa=json.dumps(get_post_data)
#     MetersphereUtils.update_scenario_detail(get_post_data)
def fibonacci_handler(result):
    get_name=result["name"]
    # if "copy_" in get_name:
    #     get_name=get_name.replace("copy_", "")
    #     result["name"]=get_name

    hashTree = result["hashTree"]
    if str(hashTree).count("/xxl-job-admin/jobinfo/trigger")>0 and str(hashTree).count("expect_time")>0:
        for i,get_data in enumerate(hashTree):
            if get_data["type"] == "scenario"  and get_data["enable"] == True:
                if str(get_data['name']).count("220925")>0 or str(get_data['name']).count("221025")>0:
                    result["hashTree"][i]["enable"] = False
                    print("处理1时间关闭")

                if str(get_data['name']).count("调整")>0:
                    if len(get_data['hashTree']) ==3 and str(get_data['hashTree']).count("修改系统时间")>0:
                        result["hashTree"][i]["enable"]=False
                        print("处理3下有时间和调整")
                    # elif len(get_data['hashTree']) ==2 :
                    #     get_data['hashTree'][]
                    #     result["hashTree"][i]["enable"]=False
                    #     print("处理3")
                    elif (len(get_data['hashTree']) == 4 or len(get_data['hashTree']) == 5) :
                        if str(get_data['hashTree']).count("/xxl-job-admin/jobinfo/trigger")>0:
                            result["hashTree"][i]["enable"] = False
                            print("处理4只有调整操作")



            #     if str(get_data['hashTree']).count('GID')>0 :
            #         tmp=hashTree[i]
            #         tem_2=str(tmp).replace("GID","THALES")
            #         result["hashTree"][i]=eval(tem_2)
            #         # result["hashTree"][i] = "GID"
            #         # result["hashTree"][i]['id']="5b00d3bd-21de-4992-8d58-a88e9f6ebeef"
            #         # result["hashTree"][i]['referenced']="REF"
            #         break
            # # if get_data['num']==102260:
            # #     result["hashTree"][i]['referenced']="REF"





def handler_process(id):
    scenario_id= MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result=json.loads(get_sce_data)
    #todo
    fibonacci_handler(result)

    data["data"]["scenarioDefinition"]=result
    get_post_data=data["data"]
    # get_daa=json.dumps(get_post_data)
    get_info_udpate=MetersphereUtils.update_scenario_detail(get_post_data)
    print(get_info_udpate)
def handler_process_data(id):
    scenario_id= MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result=json.loads(get_sce_data)
    data["data"]["scenarioDefinition"]=result
    get_name = data["data"]["name"]
    get_name = get_name.replace("copy_", "")
    pattern=r"_[0-9a-z][0-9a-z][0-9a-z][0-9a-z]"
    get_name=re.sub(pattern,"",get_name)

    data["data"]["name"] = get_name
    get_post_data=data["data"]
    # get_daa=json.dumps(get_post_data)
    get_info_udpate=MetersphereUtils.update_scenario_detail(get_post_data)
    print()
if __name__ == '__main__':
    #输入用例id
    module_id=[
  "b2a54dc5-21f0-4aed-970b-037f1ef56cbe",
  "28859d83-4947-4c45-94cb-01f5c41a6006",
  "859a5a9f-29b9-4753-a891-953e62cfc2e8",
  "c3865a04-64fc-4521-8082-6055466f97c3",
  "b8beeb5c-6924-4619-96fb-8a624285aa5c"
]
    get_ids=get_batch_id_list(module_id)
    for get_id in get_ids:
        handler_process(get_id)
    # handler_process("102304")
    # handler_process("100651")