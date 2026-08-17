import json
import re

from jsonpath import jsonpath

from MetersphereInterface import MetersphereUtils


def fibonacci_handler(result):
    hashTree = result["hashTree"]

    for i, get_data in enumerate(hashTree):
        if hashTree[i]["enable"] == True:
            if str(get_data).count("/v1.0/debit/marketing/activity/task/query") > 0:
                # if str(get_data).count("direct")>0:
                print("++++++++++++")
            # get_list=jsonpath(get_data, "$..jsonPath")
        #     # print(len(get_list))
        #     if len(get_list)>0:
        #         for get_one in get_list:
        #             if len(get_one)>0:
        #                 print(len(get_one))

        # break


def handler_process(id):
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    # todo
    fibonacci_handler(result)


if __name__ == '__main__':
    # 输入用例id
    module_id = [
  "5f3f42eb-8c8c-4b4e-b66f-91357f7e83a3",
  "f936491c-fc02-4d25-a157-f6426302e3a5",
  # "21e4ccfe-f501-4b9c-88d5-d2e24d80f994",
  # "dd4348f3-30e9-44c2-b37f-1a89a7a6d553",
  # "33dbe073-d3fe-48b8-927a-276f3db3abeb",
  # "d53a0be3-d077-44c3-a096-4d4530e60d8b",
  # "3ed95422-6e47-4558-a066-8973fdca9971",
  # "f0aadacd-a99e-4b60-8f55-dae8451f0937",
  # "361e6f85-ac53-4b85-ab91-3c9ad6e1f8a8"
]
    for i in range(1, 4):
        get_batch_ids = MetersphereUtils.get_batch_ids(i, 50, module_id)
        # get_ids=get_batch_id_list(module_id)
        # get_ids=["145d4555-24e7-43a8-b1f6-960bf63e0729"]
        for get_id in get_batch_ids:
            handler_process(get_id)
    # handler_process("102304")
    # handler_process("100651")
