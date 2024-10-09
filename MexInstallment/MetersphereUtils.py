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


def get_scenario_detail_all_info(scenario_id):
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


def request_http(s, accessKey, secretKey):
    timeStamp = int(round(time.time() * 1000))
    combox_key = accessKey + '|' + str(uuid.uuid4()) + '|' + str(timeStamp)
    signature = aesEncrypt(combox_key, secretKey, accessKey)
    print(signature.decode('UTF-8'))
    header = {'Content-Type': 'application/json', 'ACCEPT': 'application/json', 'accessKey': accessKey,
              'signature': signature.decode('UTF-8'), 'Connection': 'close'}
    s.headers.update(header)
    return s


def get_batch_ids(page_no, page_size,module_ids_list):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/api/api/automation/list/{}/{}".format(page_no, page_size)
    post_data = {"filters": {"status": ["Prepare", "Underway", "Completed"]},
                 "orders": [{"name": "name", "type": "asc"}],
                 "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                 "selectThisWeedData": false, "executeStatus": null, "selectDataRange": null, "selectAll": false,
                 "unSelectIds": [], "name": "", "combine": {},
                 "moduleIds":module_ids_list
                 }
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
def get_test_plan_report_db_sce_failure_cases_and_unrun_cases_report_ids3(get_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/test/plan/report/db/{}".format(get_id)

    r = s.get(url)
    get_data=r.json().get("data")
    # scenarioAllCases
    listObject = get_data.get("scenarioFailureCases")
    listObject2 = get_data.get('unExecuteScenarios')
    for get_one in listObject2:
        listObject.append(get_one)
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
def rerun_report_single_plan_test(all_report_id,id,sub_report_id,user_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/test/plan/rerun"
    post_data ={"type": "TEST_PLAN", "reportId": all_report_id, "scenarios": [
        {"id": id, "reportId": sub_report_id,
         "userId": user_id}], "cases": [], "performanceCases": []}
    print(post_data)
    pp = json.dumps(post_data)
    r = s.post(url, data=pp)

    return r.json()

def rerun_report_mul_plan_test(all_report_id,scenarios_list):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/track/test/plan/rerun"
    post_data ={"type": "TEST_PLAN", "reportId": all_report_id, "scenarios": scenarios_list, "cases": [], "performanceCases": []}
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


if __name__ == '__main__':
    get_list = test_plan_scenario_list(1, 20, "160575b1-1439-4e84-80fa-5c0751b42170")
    print(get_list)
    for get_one in get_list:
        get_result = test_plan_order_update(get_one["id"], "440385cc-a3a4-4f4b-af2d-fa2673bd51f5",
                                            "160575b1-1439-4e84-80fa-5c0751b42170")
        print(get_result)
