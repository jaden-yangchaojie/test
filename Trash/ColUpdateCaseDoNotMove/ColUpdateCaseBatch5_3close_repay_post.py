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
                            if str(get_sub_data['name']).count("xxljob账单日分期") > 0 or str(get_sub_data['name']).count("账单日分期本金入账")>0:
                                result["hashTree"][i]["hashTree"][k]["enable"] = False
                                print("处理1下有时间和调整,处理时间下的处理入账关闭09-25")

                elif str(get_data).count("2022-10-25 ") > 0 and str(get_data['hashTree']).count("/xxl-job-admin/jobinfo/trigger")>0:
                    # result["hashTree"][i]["hashTree"][2]["enable"] = False
                        for k, get_sub_data in enumerate(get_data['hashTree']):
                            if str(get_sub_data['name']).count("xxljob账单日分期") > 0 or str(get_sub_data['name']).count("账单日分期本金入账")>0:
                                result["hashTree"][i]["hashTree"][k]["enable"] = False
                                print("处理1下有时间和调整处理时间下的处理入账关闭10-25")

                elif str(get_data).count("2022-11-25 ")>0 and str(get_data['hashTree']).count("/xxl-job-admin/jobinfo/trigger")>0:
                    # result["hashTree"][i]["hashTree"][2]["enable"] = False
                        for k, get_sub_data in enumerate(get_data['hashTree']):
                            if str(get_sub_data['name']).count("xxljob账单日分期") > 0 or str(get_sub_data['name']).count("账单日分期本金入账")>0:
                                result["hashTree"][i]["hashTree"][k]["enable"] = False
                                print("处理1下有时间和调整，处理时间下的处理入账关闭1125")

                elif str(get_data).count("2022-12-25 ")>0 and str(get_data['hashTree']).count("/xxl-job-admin/jobinfo/trigger")>0:
                    # result["hashTree"][i]["hashTree"][2]["enable"] = False
                        for k, get_sub_data in enumerate(get_data['hashTree']):
                            if str(get_sub_data['name']).count("xxljob账单日分期") > 0 or str(get_sub_data['name']).count("账单日分期本金入账")>0:
                                result["hashTree"][i]["hashTree"][k]["enable"] = False
                                print("处理1下有时间和调整处理时间下的处理入账关闭1225")

                elif ((str(get_data['name']).count("xxljob账单日分期")>0 or str(get_data['name']).count("修改过写死")>0 or str(get_data['name']).count("账单日分期本金入账")>0 )) and str(get_data['hashTree']).count("/xxl-job-admin/jobinfo/trigger")>0 and str(get_data['name']).count("customerId")==0:
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
  "e00c1576-be16-4eb5-b8e1-3785d330ec76"
]
    get_ids=get_batch_id_list(module_id)
    for get_id in get_ids:
        handler_process(get_id)
    # handler_process("102304")
    # handler_process("100651")