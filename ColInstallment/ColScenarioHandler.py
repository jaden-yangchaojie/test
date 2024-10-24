import json
import random
import re

import os
import string
import sys


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
host = "http://10.82.95.229:8081"


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
    #         .get("data").get("scenarioDefinition"))
    # get_data = json.loads(data)
    # get_list=[]
    # fibonacci(get_data, get_list)
    return  data
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
    # header = {'Content-Type': m.content_type,'ACCEPT': 'application/json', 'accessKey': accessKey,
    #           'signature': signature.decode('UTF-8'), 'Connection': 'close',
    #           "Workspace": "6852763f-a091-11ed-aa14-0242ac1e0a02"}
    header = {'Content-Type': m.content_type,'accessKey': accessKey,
              'signature': signature.decode('UTF-8'),"Workspace": "6852763f-a091-11ed-aa14-0242ac1e0a02"}
    s.headers.update(header)
    # print(m.to_string())
    # mm=MultipartFormData.to_form_data(data={"request":("blob",json.dumps(post_data),'application/json'),"filename":"blob"}, boundary=boundary)
    # kk={"request":("blob", json.dumps(post_data), 'application/json')}

    req = s.post(url=url,data=m)
    # print(req.json())
    return req

def fibonacci(get_data, dds):

    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
        get_path = get_data["path"]
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

