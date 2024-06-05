import json

import ColScenarioHandler

def handler_update_name(id):
    scenario_id = ColScenarioHandler.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = ColScenarioHandler.get_scenario_detail_all_info(scenario_id)

    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    result["name"] = "dfl逾期DQ操作1"
    data["data"]["scenarioDefinition"] = result
    data["data"]["name"] = "dfl逾期DQ操作1"
    get_post_data = data["data"]
    # get_daa=json.dumps(get_post_data)
    ColScenarioHandler.update_scenario_detail(get_post_data)
def fibonacci(get_data, dds):

    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
        get_path = get_data["path"]
        if get_path=="/backoffice/dfl/credit/statement/settled":
            for get_p in get_data["hashTree"]:
                if get_p["clazzName"]=="io.metersphere.api.dto.definition.request.assertions.MsAssertions":
                    get_p["jsonPath"]= [
                                            {
                                              'valid': True,
                                              'expect': '20221027',
                                              'expression': '$.data.statementDate',
                                              'enable': True,
                                              'description': '$.data.statementDate REGEX: 20221027',
                                              'type': 'JSON',
                                              'option': 'REGEX'
                                            }]

        get_body = get_data["body"]
        get_dict = {"path": get_path, "body": get_body}

        dds.append(get_dict)
    if get_data["type"]=="JDBCSampler" and get_data["enable"] == True:
        get_sql = get_data["query"]
        if str(get_sql).count(" set ")>0:
            get_dict = {"path":"update_sql","update_sql":  get_sql}
            dds.append(get_dict)

    elif get_data["type"] == "scenario" and get_data["enable"] == True:
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            fibonacci(subScenario, dds)

def handler_process(id):
    scenario_id= ColScenarioHandler.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = ColScenarioHandler.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result=json.loads(get_sce_data)
    get_list = []
    fibonacci(result, get_list)

    data["data"]["scenarioDefinition"]=result
    get_post_data=data["data"]
    # get_daa=json.dumps(get_post_data)
    ColScenarioHandler.update_scenario_detail(get_post_data)

def get_batch_id():
    print(ColScenarioHandler.get_batch_ids(1,10))
if __name__ == '__main__':
    #输入用例id
    get_batch_id()
    # handler_process("102252")
    # handler_process("102304")
    # handler_process("100651")