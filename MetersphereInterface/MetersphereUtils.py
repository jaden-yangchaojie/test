import base64
import json
import string
import sys
import time
import uuid

import jsonpath
import requests
from Crypto.Cipher import AES
from Crypto.Random import random
from requests_toolbelt import MultipartEncoder

accessKey = "7CxLnIMxi4mb72oN"
secretKey = "nGJf58NMzz1xnnb9"
host = "http://k8s-metersph-metersph-a8a69a9569-2563ee3ca1fe1577.elb.us-east-1.amazonaws.com:8000"
projectId = ""
false = False
null = None
true = True


def aesEncrypt(text, secretKey, iv):
    BS = AES.block_size  # 这个等于16
    mode = AES.MODE_CBC

    def pad(s): return s + (BS - len(s) % BS) * \
        chr(BS - len(s) % BS)

    cipher = AES.new(secretKey.encode('UTF-8'), mode, iv.encode('UTF-8'))
    encrypted = cipher.encrypt(pad(text).encode('UTF-8'))
    # 通过aes加密后，再base64加密
    b_encrypted = base64.b64encode(encrypted)
    return b_encrypted


def create(post_data):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)
    url = host + "/api/api/automation/create"

    timeStamp = int(round(time.time() * 1000))
    combox_key = accessKey + '|' + str(uuid.uuid4()) + '|' + str(timeStamp)
    signature = aesEncrypt(combox_key, secretKey, accessKey)
    boundary = '----WebKitFormBoundary' \
               + ''.join(random.sample(string.ascii_letters + string.digits, 16))

    json_data = json.dumps(post_data, ensure_ascii=False)
    print(json_data)
    s = requests.session()
    m = MultipartEncoder(fields={"request": ('blob', json_data, 'application/json'), "filename": "blob"},
                         boundary=boundary)
    header = {'Content-Type': m.content_type, 'accessKey': accessKey,
              'signature': signature.decode('UTF-8'), "Workspace": "6852763f-a091-11ed-aa14-0242ac1e0a02"}
    s.headers.update(header)
    req = s.post(url=url, data=m)
    return req.json()


def update(get_post_data):
    # 使用
    timeStamp = int(round(time.time() * 1000))
    combox_key = accessKey + '|' + str(uuid.uuid4()) + '|' + str(timeStamp)
    signature = aesEncrypt(combox_key, secretKey, accessKey)
    boundary = '----WebKitFormBoundary' \
               + ''.join(random.sample(string.ascii_letters + string.digits, 16))

    url = host + "/api/api/automation/update"
    print(url)
    json_data_dump = json.dumps(get_post_data, ensure_ascii=False)
    s = requests.session()
    m = MultipartEncoder(fields={"request": ('blob', json_data_dump, 'application/json'), "filename": "blob"},
                         boundary=boundary)
    header = {'Content-Type': m.content_type, 'accessKey': accessKey,
              'signature': signature.decode('UTF-8'), "Workspace": "6852763f-a091-11ed-aa14-0242ac1e0a02"}
    s.headers.update(header)
    req = s.post(url=url, data=m)
    return req


def get_scenario_detail_id_by_search_id(id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)
    url = host + "/api/api/automation/list/1/10"
    post_data = {"filters": {"status": ["Prepare", "Underway", "Completed"]},
                 "orders": [{"name": "name", "type": "asc"}], "moduleIds": [],
                 "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                 "selectThisWeedData": false, "executeStatus": null, "selectDataRange": null, "selectAll": false,
                 "unSelectIds": [], "name": "", "combine": {"id": {"operator": "like", "value": str(id)}}
                 }
    pp = json.dumps(post_data)
    r = s.post(url, data=pp)
    listObject = r.json().get("data").get("listObject")
    if len(listObject) == 0:
        print("没有搜索该用例id")
        sys.exit()
    scenario_id = listObject[0]["id"]

    return scenario_id


def get_scenario_detail(scenario_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)
    url = host + "/api/api/automation/scenario-details/{}".format(scenario_id)
    r = s.get(url)
    print("用例名称：" + r.json().get("data").get("name"))
    data = r.json().get("data").get("scenarioDefinition")
    get_data = json.loads(data)
    get_list = []
    fibonacci(get_data, get_list)
    return get_list


def get_scenario_detail_all_info(scenario_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)
    url = host + "/api/api/automation/scenario-details/{}".format(scenario_id)
    r = s.get(url)
    print("用例名称：" + r.json().get("data").get("name"))
    data = r.json()
    return data


def get_batch_ids(page_no, page_size):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/api/api/automation/list/{}/{}".format(page_no, page_size)
    post_data = {"filters": {"status": ["Prepare", "Underway", "Completed"]},
                 "orders": [{"name": "name", "type": "asc"}], "moduleIds": [],
                 "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                 "selectThisWeedData": false, "executeStatus": null, "selectDataRange": null, "selectAll": false,
                 "unSelectIds": [], "name": "", "combine": {},
                 "moduleIds": ["cab35b7a-0b79-4b59-86bf-ef2cb98a89a5", "215d2b0f-94fe-44a0-9ae5-5a38359dbda2",
                               "1014bc27-e5b0-4fe3-abb8-5d93bc507fdc", "05f88e9a-4581-4095-8149-cc8557ee8262",
                               "095a64ef-3ca7-41ed-857d-27e3b9ea6af6", "db96f904-7441-41b1-bb3e-33af3eeb3e17",
                               "e00c1576-be16-4eb5-b8e1-3785d330ec76", "c83c8e7f-7026-414e-b74a-457c28ba19e2"]
                 }
    pp = json.dumps(post_data)
    r = s.post(url, data=pp)
    listObject = r.json().get("data").get("listObject")
    if len(listObject) == 0:
        print("没有搜索该用例id")
        sys.exit()
    get_ref_id = jsonpath.jsonpath(listObject, "$..refId")

    return get_ref_id


def update_scenario_detail(post_data):
    timeStamp = int(round(time.time() * 1000))
    combox_key = accessKey + '|' + str(uuid.uuid4()) + '|' + str(timeStamp)
    signature = aesEncrypt(combox_key, secretKey, accessKey)
    boundary = '----WebKitFormBoundary' \
               + ''.join(random.sample(string.ascii_letters + string.digits, 16))

    url = host + "/api/api/automation/update"

    json_data = json.dumps(post_data, ensure_ascii=False)
    # print(json_data)
    s = requests.session()
    m = MultipartEncoder(fields={"request": ('blob', json_data, 'application/json'), "filename": "blob"},
                         boundary=boundary)
    header = {'Content-Type': m.content_type, 'accessKey': accessKey,
              'signature': signature.decode('UTF-8'), "Workspace": "6852763f-a091-11ed-aa14-0242ac1e0a02"}
    s.headers.update(header)
    req = s.post(url=url, data=m)
    return req


def fibonacci(get_data, dds):
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
        get_path = get_data["path"]
        get_body = get_data["body"]
        get_dict = {"path": get_path, "body": get_body}

        dds.append(get_dict)
    if get_data["type"] == "JDBCSampler" and get_data["enable"] == True:
        get_sql = get_data["query"]
        if str(get_sql).count(" set ") > 0:
            get_dict = {"path": "update_sql", "update_sql": get_sql}
            dds.append(get_dict)

    elif get_data["type"] == "scenario" and get_data["enable"] == True:
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            fibonacci(subScenario, dds)


def get_scenario_single_detail_all_info(scenario_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)
    url = host + "/api/api/automation/scenario-details/{}".format(scenario_id)
    r = s.get(url)
    print("用例名称：" + r.json().get("data").get("name"))
    data = r.json()
    return data


def get_scenario_list(ids_list):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)
    url = host + "/api/api/automation/get-scenario-list"
    post_data = ids_list
    pp = json.dumps(post_data)
    r = s.post(url, data=pp)
    get_result = r.json().get("data")
    return get_result


def get_scenario_detail_id_by_search_id(id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)
    url = host + "/api/api/automation/list/1/10"
    post_data = {"filters": {"status": ["Prepare", "Underway", "Completed"]},
                 "orders": [{"name": "name", "type": "asc"}], "moduleIds": [],
                 "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                 "selectThisWeedData": false, "executeStatus": null, "selectDataRange": null, "selectAll": false,
                 "unSelectIds": [], "name": "", "combine": {"id": {"operator": "like", "value": str(id)}}
                 }
    pp = json.dumps(post_data)
    r = s.post(url, data=pp)
    listObject = r.json().get("data").get("listObject")
    if len(listObject) == 0:
        print("没有搜索该用例id")
        sys.exit()
    scenario_id = listObject[0]["id"]
    return scenario_id


def get_scenario_detail_id_by_search_id2(id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)
    url = host + "/api/api/automation/list/1/10"
    post_data = {"filters": {"status": ["Prepare", "Underway", "Completed"]},
                 "orders": [{"name": "name", "type": "asc"}], "moduleIds": [],
                 "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                 "selectThisWeedData": false, "executeStatus": null, "selectDataRange": null, "selectAll": false,
                 "unSelectIds": [], "name": "", "combine": {"id": {"operator": "like", "value": str(id)}}
                 }
    pp = json.dumps(post_data)
    r = s.post(url, data=pp)
    listObject = r.json().get("data").get("listObject")
    if len(listObject) == 0:
        print("没有搜索该用例id")
        sys.exit()
    scenario_id = listObject[0]["id"]
    return scenario_id


def request_http(s, accessKey, secretKey):
    timeStamp = int(round(time.time() * 1000))
    combox_key = accessKey + '|' + str(uuid.uuid4()) + '|' + str(timeStamp)
    signature = aesEncrypt(combox_key, secretKey, accessKey)
    print(signature.decode('UTF-8'))
    header = {'Content-Type': 'application/json', 'ACCEPT': 'application/json', 'accessKey': accessKey,
              'signature': signature.decode('UTF-8'), 'Connection': 'close'}
    s.headers.update(header)
    return s


def get_project_env(project_id="11406dc7-8340-401f-813f-3511a97d3fbb"):
    s = requests.session()

    url = host + "/api/environment/project-env"
    post_data = [project_id]
    pp = json.dumps(post_data)
    r = s.post(url, data=pp)
    listObject = r.json().get("data")
    return listObject


def get_batch_ids(page_no, page_size, module_ids_list):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/api/api/automation/list/{}/{}".format(page_no, page_size)
    post_data = {"filters": {"status": ["Prepare", "Underway", "Completed"]},
                 "orders": [{"name": "num", "type": "desc"}],
                 "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                 "selectThisWeedData": false, "executeStatus": null, "selectDataRange": null, "selectAll": false,
                 "unSelectIds": [], "name": "", "combine": {},
                 "moduleIds": module_ids_list

                 }
    # post_data = {"filters": {"status": ["Prepare", "Underway", "Completed"]},
    #              "orders": [{"name": "name", "type": "asc"}],
    #              "projectId": "4d8ddb12-9d98-4087-8cf7-84d80b9370d9",
    #              "selectThisWeedData": false, "executeStatus": null, "selectDataRange": null, "selectAll": false,
    #              "unSelectIds": [], "name": "", "combine": {},
    #              "moduleIds": module_ids_list
    #              }
    pp = json.dumps(post_data)
    r = s.post(url, data=pp)
    listObject = r.json().get("data").get("listObject")
    if len(listObject) == 0:
        print("没有搜索该用例id")
        sys.exit()
    get_ref_id = jsonpath.jsonpath(listObject, "$..refId")

    return get_ref_id


def get_test_plan_report_db_sce_failure_cases_report_ids(get_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/test/plan/report/db/{}".format(get_id)

    r = s.get(url)
    # scenarioAllCases
    listObject = r.json().get("data").get("scenarioFailureCases")
    if len(listObject) == 0:
        print("没有搜索该报告id")
        sys.exit()
    get_report_id = jsonpath.jsonpath(listObject, "$..reportId")

    return get_report_id


def get_test_plan_report_db_sce_failure_cases_report_ids2(get_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/test/plan/report/db/{}".format(get_id)

    r = s.get(url)
    # scenarioAllCases
    listObject = r.json().get("data").get("scenarioFailureCases")
    if len(listObject) == 0:
        print("没有搜索该报告id")
        sys.exit()

    return listObject


def get_test_plan_report_db_sce_failure_cases_report_ids3(get_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/test/plan/report/db/{}".format(get_id)

    r = s.get(url)
    # scenarioAllCases
    listObject = r.json().get("data").get("scenarioFailureCases")

    if len(listObject) == 0:
        print("没有搜索失败报告id")
        sys.exit()

    return listObject


def get_test_plan_report_db_sce_failure_cases_and_unrun_cases_report_ids3(get_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/test/plan/report/db/{}".format(get_id)

    r = s.get(url)
    get_data = r.json().get("data")
    # scenarioAllCases
    listObject = get_data.get("scenarioFailureCases")
    listObject2 = get_data.get('unExecuteScenarios')
    for get_one in listObject2:
        listObject.append(get_one)
    if len(listObject) == 0:
        print("没有搜索该报告id")


    return listObject


def get_test_plan_report_db_sce_failure_cases_and_unrun_and_success_cases_report_ids4(get_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/test/plan/report/db/{}".format(get_id)

    r = s.get(url)
    get_data = r.json().get("data")
    # scenarioAllCases
    listObject = get_data.get('scenarioAllCases')
    # listObject2 = get_data.get('unExecuteScenarios')
    # for get_one in listObject2:
    #     listObject.append(get_one)
    listObjectId = jsonpath.jsonpath(listObject, "$..reportId")
    if len(listObjectId) == 0:
        print("没有搜索该报告id")
        sys.exit()

    return listObjectId


def get_test_plan_report_db_sce_failure_cases_and_unrun_and_success_cases_report_ids5(get_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/test/plan/report/db/{}".format(get_id)

    r = s.get(url)
    get_data = r.json().get("data")
    # scenarioAllCases
    listObject = get_data.get('scenarioAllCases')

    list_case_report_ids = jsonpath.jsonpath(listObject, "$..reportId")
    list_case_case_ids = jsonpath.jsonpath(listObject, "$..caseId")
    if len(list_case_report_ids) == 0:
        print("没有搜索该报告id")
        sys.exit()

    return list_case_report_ids, list_case_case_ids


def get_test_plan_report_db_sce_failure_cases_and_unrun_and_success_cases_report_ids6(get_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/test/plan/report/db/{}".format(get_id)

    r = s.get(url)
    get_data = r.json().get("data")
    # scenarioAllCases
    listObject = get_data.get('scenarioAllCases')

    list_case_report_ids = jsonpath.jsonpath(listObject, "$..reportId")
    list_case_case_ids = jsonpath.jsonpath(listObject, "$..caseId")
    modulePaths = jsonpath.jsonpath(listObject, "$..modulePath")
    if len(list_case_report_ids) == 0:
        print("没有搜索该报告id")
        sys.exit()

    return list_case_report_ids, list_case_case_ids, modulePaths


def get_test_plan_report_db_sce_failure_cases_and_unrun_and_success_cases_report_ids7(get_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/test/plan/report/db/{}".format(get_id)

    r = s.get(url)
    get_data = r.json().get("data")
    # scenarioAllCases
    listObject = get_data.get('scenarioAllCases')

    if len(listObject) == 0:
        print("没有搜索该报告id")
        sys.exit()

    return listObject


def get_test_plan_report_running_report_test_ids(get_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/api/api/scenario/report/get/{}".format(get_id)

    r = s.get(url)
    # scenarioAllCases
    content = r.json().get("data").get("content")
    steps = json.loads(content)

    get_step_all = jsonpath.jsonpath(steps, "$..totalStatus")
    return get_step_all


def get_test_plan_report_all_running_detail_info(userId="admin"):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/task/center/list/1/20"
    post_data = {"triggerMode": "", "executionStatus": "RUNNING", "executor": userId,
                 "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb", "userId": "admin", "activeName": "SCENARIO"}
    pp = json.dumps(post_data)
    r = s.post(url, data=pp)

    get_result = r.json()
    list_object = get_result.get("data").get("listObject")
    if len(list(list_object)) == 0:
        print("没有在跑的用例")
        return False

    get_ids = jsonpath.jsonpath(list_object, "$..id")
    get_name = jsonpath.jsonpath(list_object, "$..name")

    dict_data = {}
    for i, get_one in enumerate(get_ids):
        dict_data[get_one] = get_name[i]
    return dict_data


def rerun_report_single_plan_test(all_report_id, id, sub_report_id, user_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/test/plan/rerun"
    post_data = {"type": "TEST_PLAN", "reportId": all_report_id, "scenarios": [
        {"id": id, "reportId": sub_report_id,
         "userId": user_id}], "cases": [], "performanceCases": []}
    print(post_data)
    pp = json.dumps(post_data)
    r = s.post(url, data=pp)

    return r.json()


def stop_report_single_plan_test(all_report_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/api/api/automation/stop/{}".format(all_report_id)

    r = s.get(url)
    return r.json()


def rerun_report_mul_plan_test(all_report_id, scenarios_list):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/test/plan/rerun"
    post_data = {"type": "TEST_PLAN", "reportId": all_report_id, "scenarios": scenarios_list, "cases": [],
                 "performanceCases": []}
    print(post_data)
    pp = json.dumps(post_data)
    r = s.post(url, data=pp)

    return r.json()


def get_test_plan_report_id_get_content(get_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/api/api/scenario/report/get/{}".format(get_id)

    r = s.get(url)
    get_result = r.json().get("data")

    return get_result


def test_plan_scenario_list(page_no, page_size, plan_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/test/plan/scenario/case/list/{}/{}".format(page_no, page_size)
    post_data = {"planId": plan_id}

    pp = json.dumps(post_data)
    r = s.post(url, data=pp)
    listObject = r.json().get("data").get("listObject")
    return listObject


def test_plan_scenario_list1(page_no, page_size, plan_id, priorit_list):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/test/plan/scenario/case/list/{}/{}".format(page_no, page_size)
    post_data = {"components": [{"key": "name", "name": "MsTableSearchInput", "label": "commons.name",
                                 "operator": {"value": "like", "options": [
                                     {"label": "commons.adv_search.operators.like", "value": "like"},
                                     {"label": "commons.adv_search.operators.not_like", "value": "not like"}]}},
                                {"key": "status", "name": "MsTableSearchSelect", "label": "commons.status",
                                 "operator": {"options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                                                          {"label": "commons.adv_search.operators.not_in",
                                                           "value": "not in"}]},
                                 "options": [{"value": "Prepare", "label": "test_track.plan.plan_status_prepare"},
                                             {"value": "Underway", "label": "test_track.plan.plan_status_running"},
                                             {"value": "Completed", "label": "test_track.plan.plan_status_completed"}],
                                 "props": {"multiple": true}},
                                {"key": "createTime", "name": "MsTableSearchDateTimePicker",
                                 "label": "commons.create_time", "operator": {
                                    "options": [{"label": "commons.adv_search.operators.between", "value": "between"},
                                                {"label": "commons.adv_search.operators.gt", "value": "gt"},
                                                {"label": "commons.adv_search.operators.lt", "value": "lt"}]}},
                                {"key": "updateTime", "name": "MsTableSearchDateTimePicker",
                                 "label": "commons.update_time", "operator": {
                                    "options": [{"label": "commons.adv_search.operators.between", "value": "between"},
                                                {"label": "commons.adv_search.operators.gt", "value": "gt"},
                                                {"label": "commons.adv_search.operators.lt", "value": "lt"}]}}],
                 "selectAll": false, "unSelectIds": [], "moduleIds": [],
                 "planId": plan_id, "name": "", "filters": {"level": priorit_list}}
    print(json.dumps(post_data))
    pp = json.dumps(post_data)
    r = s.post(url, data=pp)
    get_result = r.json()
    listObject = get_result.get("data").get("listObject")
    item_count = get_result.get("data").get('itemCount')
    page_count = get_result.get("data").get('pageCount')

    return listObject, item_count, page_count


def test_plan_scenario_case_relevance(case_ids, plan_id="63ae9097-5cf1-46fa-b596-574dcb67a43b",
                                      project_id='11406dc7-8340-401f-813f-3511a97d3fbb',
                                      env_id="d2723bd0-7959-4c8f-b4ca-864469a6dc20"):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/test/plan/scenario/case/relevance"
    # project_id->env_id
    env_map = {project_id: env_id}
    # mapping->{case_id:project_id,case_id:project_id}
    mapping = {}
    for case_id in case_ids:
        mapping[case_id] = [project_id]

    post_data = {"planId": plan_id,
                 "mapping": mapping,
                 "envMap": env_map,
                 "environmentType": "JSON", "envGroupId": "", "ids": case_ids,
                 "condition": {"components": [{"key": "name", "name": "MsTableSearchInput", "label": "commons.name",
                                               "operator": {"value": "like", "options": [
                                                   {"label": "commons.adv_search.operators.like", "value": "like"},
                                                   {"label": "commons.adv_search.operators.not_like",
                                                    "value": "not like"}]}},
                                              {"key": "priority", "name": "MsTableSearchSelect",
                                               "label": "test_track.case.priority", "operator": {"options": [
                                                  {"label": "commons.adv_search.operators.in", "value": "in"},
                                                  {"label": "commons.adv_search.operators.not_in", "value": "not in"}]},
                                               "options": [{"label": "P0", "value": "P0"},
                                                           {"label": "P1", "value": "P1"},
                                                           {"label": "P2", "value": "P2"},
                                                           {"label": "P3", "value": "P3"}],
                                               "props": {"multiple": true}},
                                              {"key": "tags", "name": "MsTableSearchInput", "label": "commons.tag",
                                               "operator": {"value": "like", "options": [
                                                   {"label": "commons.adv_search.operators.like", "value": "like"},
                                                   {"label": "commons.adv_search.operators.not_like",
                                                    "value": "not like"}]}},
                                              {"key": "lastResult", "name": "MsTableSearchSelect",
                                               "label": "test_track.plan_view.execute_result", "operator": {"options": [
                                                  {"label": "commons.adv_search.operators.in", "value": "in"},
                                                  {"label": "commons.adv_search.operators.not_in", "value": "not in"}]},
                                               "options": [{"text": "Pending", "value": "PENDING"},
                                                           {"text": "Running", "value": "RUNNING"},
                                                           {"text": "Rerunning", "value": "RERUNNING"},
                                                           {"text": "Success", "value": "SUCCESS"},
                                                           {"text": "Error", "value": "ERROR"},
                                                           {"text": "FakeError", "value": "FAKE_ERROR"},
                                                           {"text": "Stopped", "value": "STOPPED"}],
                                               "props": {"multiple": true}},
                                              {"key": "createTime", "name": "MsTableSearchDateTimePicker",
                                               "label": "commons.create_time", "operator": {"options": [
                                                  {"label": "commons.adv_search.operators.between", "value": "between"},
                                                  {"label": "commons.adv_search.operators.gt", "value": "gt"},
                                                  {"label": "commons.adv_search.operators.lt", "value": "lt"}]}},
                                              {"key": "updateTime", "name": "MsTableSearchDateTimePicker",
                                               "label": "commons.update_time", "operator": {"options": [
                                                  {"label": "commons.adv_search.operators.between", "value": "between"},
                                                  {"label": "commons.adv_search.operators.gt", "value": "gt"},
                                                  {"label": "commons.adv_search.operators.lt", "value": "lt"}]}},
                                              {"key": "creator", "name": "MsTableSearchSelect",
                                               "label": "api_test.creator", "operator": {"options": [
                                                  {"label": "commons.adv_search.operators.in", "value": "in"},
                                                  {"label": "commons.adv_search.operators.not_in", "value": "not in"},
                                                  {"label": "commons.adv_search.operators.current_user",
                                                   "value": "current user"}]},
                                               "options": {"url": "/user/project/member/list", "labelKey": "name",
                                                           "valueKey": "id"}, "props": {"multiple": true}},
                                              {"key": "status", "name": "MsTableSearchSelect",
                                               "label": "commons.status", "operator": {"options": [
                                                  {"label": "commons.adv_search.operators.in", "value": "in"},
                                                  {"label": "commons.adv_search.operators.not_in", "value": "not in"}]},
                                               "options": [
                                                   {"value": "Prepare", "label": "test_track.plan.plan_status_prepare"},
                                                   {"value": "Underway",
                                                    "label": "test_track.plan.plan_status_running"},
                                                   {"value": "Completed",
                                                    "label": "test_track.plan.plan_status_completed"}],
                                               "props": {"multiple": true}}],
                               "filters": {"status": ["Prepare", "Underway", "Completed"]}, "moduleIds": [],
                               "projectId": project_id,
                               "planId": plan_id, "stepTotal": "testPlan",
                               "selectAll": false, "unSelectIds": []}}

    pp = json.dumps(post_data)

    r = s.post(url, data=pp)

    return r.json()


def test_plan_scenario_case_batch_delete(case_ids, plan_id="63ae9097-5cf1-46fa-b596-574dcb67a43b",
                                         project_id='11406dc7-8340-401f-813f-3511a97d3fbb'):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/test/plan/scenario/case/batch/delete"
    post_data = \
        {"ids": case_ids,
         "projectId": project_id, "condition": {"components": [
            {"key": "name", "name": "MsTableSearchInput", "label": "commons.name", "operator": {"value": "like",
                                                                                                "options": [{
                                                                                                    "label": "commons.adv_search.operators.like",
                                                                                                    "value": "like"},
                                                                                                    {
                                                                                                        "label": "commons.adv_search.operators.not_like",
                                                                                                        "value": "not like"}]}},
            {"key": "status", "name": "MsTableSearchSelect", "label": "commons.status", "operator": {
                "options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                            {"label": "commons.adv_search.operators.not_in", "value": "not in"}]},
             "options": [{"value": "Prepare", "label": "test_track.plan.plan_status_prepare"},
                         {"value": "Underway", "label": "test_track.plan.plan_status_running"},
                         {"value": "Completed", "label": "test_track.plan.plan_status_completed"}],
             "props": {"multiple": true}},
            {"key": "createTime", "name": "MsTableSearchDateTimePicker", "label": "commons.create_time", "operator": {
                "options": [{"label": "commons.adv_search.operators.between", "value": "between"},
                            {"label": "commons.adv_search.operators.gt", "value": "gt"},
                            {"label": "commons.adv_search.operators.lt", "value": "lt"}]}},
            {"key": "updateTime", "name": "MsTableSearchDateTimePicker", "label": "commons.update_time", "operator": {
                "options": [{"label": "commons.adv_search.operators.between", "value": "between"},
                            {"label": "commons.adv_search.operators.gt", "value": "gt"},
                            {"label": "commons.adv_search.operators.lt", "value": "lt"}]}}], "selectAll": false,
            "unSelectIds": [], "moduleIds": [],
            "planId": plan_id},
         "planId": plan_id}
    pp = json.dumps(post_data)
    r = s.post(url, data=pp)
    print(json.dumps(post_data))

    return r.json()


# todo
def set_domain():
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "api/automation/set-domain"
    # post_data = {"planId": plan_id}
    #
    # pp = json.dumps(post_data)
    # r = s.post(url, data=pp)
    # listObject = r.json().get("data").get("listObject")
    # return listObject


def test_plan_order_update(moveId, targetId, groupId):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/test/plan/scenario/case/edit/order"
    post_data = {"moveId": moveId, "moveMode": "AFTER", "targetId": targetId, "groupId": groupId}
    pp = json.dumps(post_data)
    r = s.post(url, data=pp)

    return r.json()


def operating_log_get_source(sourceId="54eb3c5d-dd11-4342-bc20-e2af5cd9a3a6"):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/api/operating/log/get/source/1/10"
    post_data = {"sourceId": sourceId, "modules": ["接口自动化", "Api automation", "接口自動化", "API_AUTOMATION"]}
    pp = json.dumps(post_data)
    r = s.post(url, data=pp)

    return r.json()
def operating_log_get_source_pageNo(sourceId="54eb3c5d-dd11-4342-bc20-e2af5cd9a3a6",pageNo=1):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/api/operating/log/get/source/{}/10".format(pageNo)
    post_data = {"sourceId": sourceId, "modules": ["接口自动化", "Api automation", "接口自動化", "API_AUTOMATION"]}
    pp = json.dumps(post_data)
    r = s.post(url, data=pp)

    return r.json()
def report_step_id(step_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/api/api/scenario/report/get/step/detail/{}".format(step_id)

    r = s.get(url)
    get_step_id_result = r.json().get("data")

    return get_step_id_result


def add_module(level, parentId, name, projectId="11406dc7-8340-401f-813f-3511a97d3fbb"):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/api/api/automation/module/add"
    # level=1不用写parentId，我们一般写level2、3
    post_data = ""
    if level == 1:
        post_data = {"level": level, "type": "add", "name": name, "label": name, "projectId": projectId}
    else:
        post_data = {"level": level, "type": "add", "parentId": parentId, "name": name, "label": name,
                     "projectId": projectId}
    pp = json.dumps(post_data)
    r = s.post(url, data=pp)

    return r.json()


def module_list(projectId="11406dc7-8340-401f-813f-3511a97d3fbb"):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/api/api/automation/module/list/" + projectId

    post_data = {}
    pp = json.dumps(post_data)
    r = s.post(url, data=pp)

    return r.json()


def get_test_plan_report_list(project_id,search_name,page_no, page_size):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/test/plan/report/list/{}/{}".format(page_no, page_size)

    post_data = {"components": [{"key": "name", "name": "MsTableSearchInput", "label": "commons.name",
                                 "operator": {"value": "like", "options": [
                                     {"label": "commons.adv_search.operators.like", "value": "like"},
                                     {"label": "commons.adv_search.operators.not_like", "value": "not like"}]}},
                                {"key": "testPlanName", "name": "MsTableSearchInput",
                                 "label": "test_track.report.list.test_plan", "operator": {
                                    "options": [{"label": "commons.adv_search.operators.like", "value": "like"},
                                                {"label": "commons.adv_search.operators.not_like",
                                                 "value": "not like"}]}},
                                {"key": "creator", "name": "MsTableSearchSelect", "label": "api_test.creator",
                                 "operator": {"options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                                                          {"label": "commons.adv_search.operators.not_in",
                                                           "value": "not in"},
                                                          {"label": "commons.adv_search.operators.current_user",
                                                           "value": "current user"}]},
                                 "options": {"url": "/user/project/member/list", "labelKey": "name", "valueKey": "id"},
                                 "props": {"multiple": true}},
                                {"key": "createTime", "name": "MsTableSearchDateTimePicker",
                                 "label": "commons.create_time", "operator": {
                                    "options": [{"label": "commons.adv_search.operators.between", "value": "between"},
                                                {"label": "commons.adv_search.operators.gt", "value": "gt"},
                                                {"label": "commons.adv_search.operators.lt", "value": "lt"}]}},
                                {"key": "triggerMode", "name": "MsTableSearchSelect",
                                 "label": "test_track.report.list.trigger_mode", "operator": {
                                    "options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                                                {"label": "commons.adv_search.operators.not_in", "value": "not in"}]},
                                 "options": [{"label": "test_track.report.trigger_mode.manual", "value": "manual"},
                                             {"label": "commons.trigger_mode.schedule", "value": "SCHEDULE"},
                                             {"label": "commons.trigger_mode.api", "value": "API"},
                                             {"label": "api_test.automation.batch_execute", "value": "BATCH"}],
                                 "props": {"multiple": true}},
                                {"key": "status", "name": "MsTableSearchSelect", "label": "test_track.plan.plan_status",
                                 "operator": {"options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                                                          {"label": "commons.adv_search.operators.not_in",
                                                           "value": "not in"}]},
                                 "options": [{"label": "Starting", "value": "Starting"},
                                             {"label": "Running", "value": "Underway"},
                                             {"label": "Completed", "value": "Completed"}],
                                 "props": {"multiple": true}}], "selectAll": false, "unSelectIds": [],
                 "orders": [{"name": "create_time", "type": "desc"}],
                 "projectId": project_id,
                 "name": search_name}
    pp = json.dumps(post_data)
    r = s.post(url, data=pp)

    # scenarioAllCases
    listObject =r.json().get("data").get("listObject")

    if len(listObject) == 0:
        print("没有搜索该报告id")
        sys.exit()

    return listObject


if __name__ == '__main__':
    get_list = test_plan_scenario_list(1, 20, "160575b1-1439-4e84-80fa-5c0751b42170")
    print(get_list)
    for get_one in get_list:
        get_result = test_plan_order_update(get_one["id"], "440385cc-a3a4-4f4b-af2d-fa2673bd51f5",
                                            "160575b1-1439-4e84-80fa-5c0751b42170")
        print(get_result)
