import json
import random
import re

import os
import string
import sys

import jsonpath
import requests
from Crypto.Cipher import AES
import json
import time
import base64
import uuid

from multipartformdata.Multipart import MultipartFormData
from requests_toolbelt import MultipartEncoder

# gNeedCheck = True

accessKey = "7CxLnIMxi4mb72oN"
secretKey = "nGJf58NMzz1xnnb9"
host = "http://metersphere.storicard-qa.com:8000"
projectId=""

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


def request_http(s, accessKey, secretKey):
    timeStamp = int(round(time.time() * 1000))
    combox_key = accessKey + '|' + str(uuid.uuid4()) + '|' + str(timeStamp)
    signature = aesEncrypt(combox_key, secretKey, accessKey)
    print(signature.decode('UTF-8'))
    header = {'Content-Type': 'application/json', 'ACCEPT': 'application/json', 'accessKey': accessKey,
              'signature': signature.decode('UTF-8'), 'Connection': 'close'}
    s.headers.update(header)
    return s
false=False
null=None
true=True
def get_scenario_detail_id_by_search_id(id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)
    url = host + "/api/api/automation/list/1/10"
    post_data={"filters":{"status":["Prepare","Underway","Completed"]},
               "orders":[{"name":"name","type":"asc"}],"moduleIds":[],
               "projectId":"11406dc7-8340-401f-813f-3511a97d3fbb",
               "selectThisWeedData":false,"executeStatus":null,"selectDataRange":null,"selectAll":false,
               "unSelectIds":[],"name":"","combine":{"id":{"operator":"like","value":str(id)}}
               }
    pp=json.dumps(post_data)
    r = s.post(url,data=pp)
    listObject=r.json().get("data").get("listObject")
    if len(listObject)==0:
        print("没有搜索该用例id")
        sys.exit()
    scenario_id=listObject[0]["id"]
    return scenario_id


def get_scenario_detail(scenario_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)
    url = host + "/api/api/automation/scenario-details/{}".format(scenario_id)
    r = s.get(url)
    print("用例名称："+r.json().get("data").get("name"))
    data = r.json().get("data").get("scenarioDefinition")
    get_data = json.loads(data)
    get_list=[]
    fibonacci(get_data, get_list)
    return  get_list
def get_scenario_detail_all_info(scenario_id):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)
    url = host + "/api/api/automation/scenario-details/{}".format(scenario_id)
    r = s.get(url)
    print("用例名称："+r.json().get("data").get("name"))
    data = r.json()
    return  data
def get_batch_ids(page_no,page_size):
    s = requests.session()
    s = request_http(s, accessKey, secretKey)

    url = host + "/api/api/automation/list/{}/{}".format(page_no,page_size)
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
    get_ref_id=jsonpath.jsonpath(listObject,"$..refId")

    return  get_ref_id
def update_scenario_detail(post_data):

    timeStamp = int(round(time.time() * 1000))
    combox_key = accessKey + '|' + str(uuid.uuid4()) + '|' + str(timeStamp)
    signature = aesEncrypt(combox_key, secretKey, accessKey)
    boundary = '----WebKitFormBoundary' \
               + ''.join(random.sample(string.ascii_letters + string.digits, 16))

    url = host + "/api/api/automation/update"

    json_data=json.dumps(post_data,ensure_ascii=False)
    print(json_data)
    s=requests.session()
    m = MultipartEncoder(fields={"request":('blob',json_data,'application/json'),"filename":"blob"}, boundary=boundary)
    header = {'Content-Type': m.content_type,'accessKey': accessKey,
              'signature': signature.decode('UTF-8'),"Workspace": "6852763f-a091-11ed-aa14-0242ac1e0a02"}
    s.headers.update(header)
    req = s.post(url=url,data=m)
    return req

def fibonacci(get_data, dds):

    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
        get_path = get_data["path"]
        get_body = get_data["body"]
        hashTree=get_data["hashTree"]
        get_dict={}
        if hashTree[0]["type"]=='JSR223PostProcessor':
            get_dict = {"path": get_path, "body": get_body,"type":'JSR223PostProcessor',"script":hashTree[0]["script"]}
        else:
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
    elif get_data["type"] == "LoopController" and get_data["enable"] == True:
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            fibonacci(subScenario, dds)

