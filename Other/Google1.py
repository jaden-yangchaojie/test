import requests


# def request_http(s, accessKey, secretKey):
#     timeStamp = int(round(time.time() * 1000))
#     combox_key = accessKey + '|' + str(uuid.uuid4()) + '|' + str(timeStamp)
#     signature = aesEncrypt(combox_key, secretKey, accessKey)
#     print(signature.decode('UTF-8'))
#     header = {'Content-Type': 'application/json', 'ACCEPT': 'application/json', 'accessKey': accessKey,
#               'signature': signature.decode('UTF-8'), 'Connection': 'close'}
#     s.headers.update(header)
#     return s

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
