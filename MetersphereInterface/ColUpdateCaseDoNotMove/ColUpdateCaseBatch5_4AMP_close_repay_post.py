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

def fibonacci_handler(result):
    hashTree = result["hashTree"]
    if str(hashTree).count("/xxl-job-admin/jobinfo/trigger")>0 and str(hashTree).count("expect_time")>0:
        for i,get_data in enumerate(hashTree):
            if get_data["type"] == "scenario"  and get_data["enable"] == True:

                if str(get_data).count("2022-09-25 ") > 0 and str(get_data['hashTree']).count("/xxl-job-admin/jobinfo/trigger")>0:
                        for k, get_sub_data in enumerate(get_data['hashTree']):
                            if str(get_sub_data['name']).count("xxljob账单日分期本金入账") > 0:
                                result["hashTree"][i]["hashTree"][k]["enable"] = False
                                print("处理1下有时间和调整,处理时间下的处理入账关闭09-25")

                elif str(get_data).count("2022-10-25 ") > 0 and str(get_data['hashTree']).count("/xxl-job-admin/jobinfo/trigger")>0:
                    # result["hashTree"][i]["hashTree"][2]["enable"] = False
                        for k, get_sub_data in enumerate(get_data['hashTree']):
                            if str(get_sub_data['name']).count("xxljob账单日分期本金入账") > 0:
                                result["hashTree"][i]["hashTree"][k]["enable"] = False
                                print("处理1下有时间和调整处理时间下的处理入账关闭10-25")

                elif str(get_data).count("2022-11-25 ")>0 and str(get_data['hashTree']).count("/xxl-job-admin/jobinfo/trigger")>0:
                    # result["hashTree"][i]["hashTree"][2]["enable"] = False
                        for k, get_sub_data in enumerate(get_data['hashTree']):
                            if str(get_sub_data['name']).count("xxljob账单日分期本金入账") > 0:
                                result["hashTree"][i]["hashTree"][k]["enable"] = False
                                print("处理1下有时间和调整，处理时间下的处理入账关闭1125")

                elif str(get_data).count("2022-12-25 ")>0 and str(get_data['hashTree']).count("/xxl-job-admin/jobinfo/trigger")>0:
                    # result["hashTree"][i]["hashTree"][2]["enable"] = False
                        for k, get_sub_data in enumerate(get_data['hashTree']):
                            if str(get_sub_data['name']).count("xxljob账单日分期本金入账") > 0:
                                result["hashTree"][i]["hashTree"][k]["enable"] = False
                                print("处理1下有时间和调整处理时间下的处理入账关闭1225")

                elif str(get_data['name']).count("xxljob账单日分期本金入账")>0  and str(get_data['hashTree']).count("/xxl-job-admin/jobinfo/trigger")>0 and str(get_data['name']).count("customerId")==0:
                    result["hashTree"][i]["enable"] = False
                    print("处理单个处理入账")







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

if __name__ == '__main__':
    #输入用例id
    module_id=[
  "541f6421-56e1-40c2-9e59-24b60e9720d3",
  "b0e877f8-2ba1-499c-a922-8b4a71b3c941",
  "f3cfd270-efbe-4bb3-b2c3-93e1d9ccf86b",
  "52de5366-ac7b-403d-87c9-05b55c9c8269",
  "2bc2a96c-b1fa-41a9-9b98-10f4efdeb59f",
  "e3a1cf0e-6fa5-4a7c-99f8-a3a20a511955",
  "5fa612fc-8912-44d1-9129-7c2aa40fb245",
  "6fa25ba7-b90e-46be-8b3b-6db6f23ffde9"
]
    get_ids=get_batch_id_list(module_id)
    for get_id in get_ids:
        handler_process(get_id)
    # handler_process("102304")
    # handler_process("100651")