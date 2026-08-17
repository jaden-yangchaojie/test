import json
import re

ssss = [{'jsr223': [], 'resourceId': '6d46b246-7859-4f78-a242-ff1a82982a5d', 'mockEnvironment': False,
         'document': {'type': 'JSON',
                      'data': {'json': [], 'include': False, 'xmlFollowAPI': 'false', 'typeVerification': False,
                               'xml': [], 'jsonFollowAPI': 'false'}, 'enable': True}, 'xpath2': [], 'active': False,
         'index': '1', 'markStep': False, 'jsonPath': [
        {'valid': True, 'description': '$.message expect: ', 'expression': '$.message', 'type': 'JSON', 'enable': True,
         'option': 'EQUALS'}, {'valid': True, 'expect': 'Success', 'expression': '$.status', 'enable': True,
                               'description': '$.status expect: Success', 'type': 'JSON', 'option': 'EQUALS'},
        {'valid': True, 'expect': '${param_activityType}', 'expression': '$.data.campaigns[0].campaignType',
         'enable': True, 'description': '$.data.campaigns[0].campaignType EQUALS: ${param_activityType}',
         'type': 'JSON', 'option': 'EQUALS'}], 'type': 'Assertions', 'isMockEnvironment': False, 'xpathType': 'xml',
         'duration': {'valid': False, 'type': 'Duration', 'value': 0, 'enable': True}, 'regex': [
        {'assumeSuccess': False, 'valid': True, 'expression': '.*${cashbackIntervalAccountLimitActivityNo}.*',
         'enable': True, 'subject': 'Response Data',
         'description': 'Response Data contains: ${cashbackIntervalAccountLimitActivityNo}', 'testType': 2, 'label': '',
         'type': 'Regex'}], 'scenarioAss': False, 'enable': True, 'hashTree': [],
         'id': 'd88d4d8f-b526-9975-d0d4-cc97d330f79e', 'projectId': '11406dc7-8340-401f-813f-3511a97d3fbb',
         'clazzName': 'io.metersphere.api.dto.definition.request.assertions.MsAssertions'}]
# [a-zA-Z]+}
pattern = r'\$\{cash[a-zA-Z]+\}'
get_find = re.findall(pattern, str(ssss))
print(get_find)

from collections import Counter

arr = ["a", "b", "a", 3, 3, 3, 4, 4, 4, 4]
freq = Counter(arr)
[freq.keys()]
print(freq)

params = {
    "cashbackRule": {
        "type": "percent",
        "calAlg": {
            "param": "1.0",
            "rules": [
            ]
        }
    }
}
get_pas=json.dumps(params)
print(json.dumps(get_pas))