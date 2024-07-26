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


def get_batch_ids(page_no, page_size):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/api/api/automation/list/{}/{}".format(page_no, page_size)
    post_data = {"filters": {"status": ["Prepare", "Underway", "Completed"]},
                 "orders": [{"name": "name", "type": "asc"}],
                 "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb",
                 "selectThisWeedData": false, "executeStatus": null, "selectDataRange": null, "selectAll": false,
                 "unSelectIds": [], "name": "", "combine": {},
                 "moduleIds": [
  "0ba04d70-e3cf-433c-ab73-158b882d1ea7",
  "4b788772-52be-46b9-aca9-a5d844063693",
  "9657157a-b9c2-4e42-93c1-c6bfe87168b2",
  "0290449f-e19f-4fba-8736-a0af8907a510",
  "8b3e4332-c80c-4dbc-98d7-f299329fcea7"
]
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
    listObject = r.json().get("data").get("scenarioFailureCases")
    if len(listObject) == 0:
        print("没有搜索该报告id")
        sys.exit()
    get_report_id = jsonpath.jsonpath(listObject, "$..reportId")

    return get_report_id
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
