import json
import re

from jsonpath import jsonpath

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
    for i, get_data in enumerate(hashTree):
        if str(get_data).count("authorizations")>0 or str(get_data).count("transaction")>0:

            get_list=jsonpath(get_data, "$..jsonPath")
            # print(len(get_list))
            if len(get_list)>0:
                for get_one in get_list:
                    if len(get_one)>0:
                        print(len(get_one))

            # break


def handler_process(id):
    scenario_id= MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result=json.loads(get_sce_data)
    #todo
    fibonacci_handler(result)



if __name__ == '__main__':
    #输入用例id
    module_id=[
  "e169ce21-2d1a-44d9-a501-16b6db059a67"
]
    get_ids=get_batch_id_list(module_id)
    for get_id in get_ids:
        handler_process(get_id)
    # handler_process("102304")
    # handler_process("100651")