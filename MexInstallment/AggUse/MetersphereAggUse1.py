import json
import math
import random
import re
import time
from ast import literal_eval
from datetime import datetime

from ColInstallment import ColScenarioHandler
from MexInstallment import MetersphereUtils
import jsonpickle

key = 'scenarioDefinition'

time_update = {'resourceId': '597d5108-888a-47d9-4c2b-0c69205483f4', 'num': 100005, 'refType': 'API', 'markStep': False,
               'autoRedirects': False, 'type': 'HTTPSamplerProxy',
               'body': {'valid': True, 'xml': False, 'binary': [], 'raw': '{\n    "time": "@@time@@"\n}',
                        'kvs': [],
                        'json': True, 'kv': False, 'type': 'JSON'}, 'versionName': 'v1.0.0', 'isMockEnvironment': False,
               'path': '/api/admin/system/faketime', 'protocol': 'HTTP', 'environmentId': '', 'enable': True,
               'followRedirects': True, 'versionEnable': True, 'connectTimeout': '150000', 'hashTree': [
        {'jsr223': [], 'resourceId': '0bf5828c-f7fd-4101-af9e-41459f459a65', 'mockEnvironment': False,
         'document': {'type': 'JSON',
                      'data': {'json': [], 'include': False, 'xmlFollowAPI': 'false', 'typeVerification': False,
                               'xml': [], 'jsonFollowAPI': 'false'}, 'enable': True}, 'xpath2': [], 'active': False,
         'index': '1', 'markStep': False, 'jsonPath': [
            {'valid': True, 'expect': 'Success', 'expression': '$.status', 'enable': True,
             'description': '$.status expect: Success', 'type': 'JSON', 'option': 'EQUALS'}], 'type': 'Assertions',
         'isMockEnvironment': False, 'xpathType': 'xml',
         'duration': {'valid': False, 'type': 'Duration', 'value': 0, 'enable': True}, 'regex': [],
         'scenarioAss': False, 'enable': True, 'hashTree': [], 'id': 'f6bc8057-42ac-db4d-7050-020329cd16ce',
         'projectId': '11406dc7-8340-401f-813f-3511a97d3fbb',
         'clazzName': 'io.metersphere.api.dto.definition.request.assertions.MsAssertions'}],
               'id': '9d374320-74ae-4433-bcd4-c69165f86691', 'responseTimeout': '150000', 'headers': [
        {'valid': True, 'file': False, 'enable': True, 'name': 'Content-Type', 'value': 'application/json',
         'urlEncode': False, 'required': True},
        {'valid': False, 'file': False, 'urlEncode': False, 'enable': True, 'required': True}], 'rest': [
        {'valid': False, 'file': False, 'enable': True, 'type': 'text', 'contentType': 'text/plain', 'urlEncode': False,
         'required': False}], 'method': 'POST', 'mockEnvironment': False, 'active': True, 'index': '1', 'url': '',
               'customizeReq': False, 'versionId': 'adee882c-f0bc-4279-8274-d03c6436c9c0', 'referenced': 'Copy',
               'domain': 'http://dfl.qa-test.storicard-qa.com', 'name': '修改系统时间', 'arguments': [
        {'valid': False, 'file': False, 'enable': True, 'type': 'text', 'contentType': 'text/plain', 'urlEncode': False,
         'required': False}], 'projectId': '11406dc7-8340-401f-813f-3511a97d3fbb',
               'clazzName': 'io.metersphere.api.dto.definition.request.sampler.MsHTTPSamplerProxy',
               'doMultipartPost': False}
time_assert = {'resourceId': 'ff3f9433-573b-173b-5d07-706bcfcb2ce9', 'num': 100019, 'refType': 'API', 'markStep': False,
               'autoRedirects': False, 'type': 'HTTPSamplerProxy',
               'body': {'valid': False, 'xml': False, 'binary': [], 'raw': '', 'kvs': [], 'json': True, 'kv': False,
                        'type': 'JSON'}, 'versionName': 'v1.0.0', 'isMockEnvironment': False,
               'path': '/api/credit/currentSystemTime', 'protocol': 'HTTP', 'environmentId': '', 'enable': True,
               'followRedirects': True, 'versionEnable': True, 'connectTimeout': '150000', 'hashTree': [
        {'resourceId': '1cce44a8-c314-45c4-8b1c-5b6a62b44ab8', 'mockEnvironment': False, 'scriptLanguage': 'beanshell',
         'num': '', 'active': True, 'index': '1', 'markStep': False, 'type': 'JSR223PreProcessor',
         'isMockEnvironment': False,
         'script': 'import org.apache.jmeter.config.Arguments;\n\n// 可到http://10.82.74.159:8081/#/project/env，编辑对应的项目环境——> 通用配置， 查看环境变量定义的值。\nint systemUpdateTime = ${systemUpdateTime};\nThread.sleep(systemUpdateTime);',
         'jsrEnable': True, 'enable': True, 'name': 'JSR223PreProcessor', 'hashTree': [],
         'shellProcessor': {'filename': '', 'cacheKey': '', 'runningVersion': False, 'scriptLanguage': '',
                            'name': 'JSR223PreProcessor',
                            'searchableTokens': ['TestElement.enabled', 'true', 'TestElement.name',
                                                 'JSR223PreProcessor', 'cacheKey', 'false', 'TestElement.test_class',
                                                 'JSR223PreProcessor', 'TestElement.gui_class',
                                                 'org.apache.jmeter.testbeans.gui.TestBeanGUI', 'scriptLanguage',
                                                 'beanshell', 'script',
                                                 'import org.apache.jmeter.config.Arguments;\n\n// 可到http://10.82.74.159:8081/#/project/env，编辑对应的项目环境——> 通用配置， 查看环境变量定义的值。\nint systemUpdateTime = ${systemUpdateTime};\nThread.sleep(systemUpdateTime);'],
                            'comment': '', 'propMap': {
                 'TestElement.test_class': {'stringValue': 'JSR223PreProcessor', 'runningVersion': False, 'intValue': 0,
                                            'name': 'TestElement.test_class', 'floatValue': 0,
                                            'objectValue': 'JSR223PreProcessor', 'booleanValue': False,
                                            'doubleValue': 0, 'value': 'JSR223PreProcessor', 'longValue': 0},
                 'cacheKey': {'stringValue': 'false', 'runningVersion': False, 'intValue': 0, 'name': 'cacheKey',
                              'floatValue': 0, 'booleanValue': False, 'objectValue': False, 'doubleValue': 0,
                              'value': False, 'longValue': 0},
                 'TestElement.enabled': {'stringValue': 'true', 'runningVersion': False, 'intValue': 0,
                                         'name': 'TestElement.enabled', 'floatValue': 0, 'booleanValue': True,
                                         'objectValue': True, 'doubleValue': 0, 'value': True, 'longValue': 0},
                 'TestElement.name': {'stringValue': 'JSR223PreProcessor', 'runningVersion': False, 'intValue': 0,
                                      'name': 'TestElement.name', 'floatValue': 0, 'objectValue': 'JSR223PreProcessor',
                                      'booleanValue': False, 'doubleValue': 0, 'value': 'JSR223PreProcessor',
                                      'longValue': 0},
                 'scriptLanguage': {'stringValue': 'beanshell', 'runningVersion': False, 'intValue': 0,
                                    'name': 'scriptLanguage', 'floatValue': 0, 'objectValue': 'beanshell',
                                    'booleanValue': False, 'doubleValue': 0, 'value': 'beanshell', 'longValue': 0},
                 'TestElement.gui_class': {'stringValue': 'org.apache.jmeter.testbeans.gui.TestBeanGUI',
                                           'runningVersion': False, 'intValue': 0, 'name': 'TestElement.gui_class',
                                           'floatValue': 0,
                                           'objectValue': 'org.apache.jmeter.testbeans.gui.TestBeanGUI',
                                           'booleanValue': False, 'doubleValue': 0,
                                           'value': 'org.apache.jmeter.testbeans.gui.TestBeanGUI', 'longValue': 0},
                 'script': {
                     'stringValue': 'import org.apache.jmeter.config.Arguments;\n\n// 可到http://10.82.74.159:8081/#/project/env，编辑对应的项目环境——> 通用配置， 查看环境变量定义的值。\nint systemUpdateTime = ${systemUpdateTime};\nThread.sleep(systemUpdateTime);',
                     'runningVersion': False, 'intValue': 0, 'name': 'script', 'floatValue': 0,
                     'objectValue': 'import org.apache.jmeter.config.Arguments;\n\n// 可到http://10.82.74.159:8081/#/project/env，编辑对应的项目环境——> 通用配置， 查看环境变量定义的值。\nint systemUpdateTime = ${systemUpdateTime};\nThread.sleep(systemUpdateTime);',
                     'booleanValue': False, 'doubleValue': 0,
                     'value': 'import org.apache.jmeter.config.Arguments;\n\n// 可到http://10.82.74.159:8081/#/project/env，编辑对应的项目环境——> 通用配置， 查看环境变量定义的值。\nint systemUpdateTime = ${systemUpdateTime};\nThread.sleep(systemUpdateTime);',
                     'longValue': 0}}, 'threadContext': {'samplingStarted': False, 'startNextThreadLoop': False,
                                                         'recording': False, 'restartNextLoop': False, 'threadNum': 0,
                                                         'testLogicalAction': 'CONTINUE', 'samplerContext': {},
                                                         'properties': {
                                                             'jdbc.config.jdbc.driver.class': 'com.mysql.jdbc.Driver|org.postgresql.Driver|oracle.jdbc.OracleDriver|com.ingres.jdbc.IngresDriver|com.microsoft.sqlserver.jdbc.SQLServerDriver|com.microsoft.jdbc.sqlserver.SQLServerDriver|org.apache.derby.jdbc.ClientDriver|org.hsqldb.jdbc.JDBCDriver|com.ibm.db2.jcc.DB2Driver|org.apache.derby.jdbc.ClientDriver|org.h2.Driver|org.firebirdsql.jdbc.FBDriver|org.mariadb.jdbc.Driver|org.sqlite.JDBC|net.sourceforge.jtds.jdbc.Driver|com.exasol.jdbc.EXADriver',
                                                             'beanshell.server.file': '../extras/startup.bsh',
                                                             'htmlParser.className': 'org.apache.jmeter.protocol.http.parser.LagartoBasedHtmlParser',
                                                             'jmeter.reportgenerator.apdex_satisfied_threshold': '500',
                                                             'htmlParser.types': 'text/html application/xhtml+xml application/xml text/xml',
                                                             'cookies': 'cookies',
                                                             'classfinder.functions.contain': '.functions.',
                                                             'wmlParser.className': 'org.apache.jmeter.protocol.http.parser.RegexpHTMLParser',
                                                             'classfinder.functions.notContain': '.gui.',
                                                             'system.properties': 'system.properties',
                                                             'jdbc.config.check.query': 'select 1 from INFORMATION_SCHEMA.SYSTEM_USERS|select 1 from dual|select 1 from sysibm.sysdummy1|select 1|select 1 from rdb$database',
                                                             'cssParser.types': 'text/css',
                                                             'sampleresult.default.encoding': 'UTF-8',
                                                             'summariser.name': 'summary',
                                                             'gui.quick_6': 'JSR223PostProcessor',
                                                             'wmlParser.types': 'text/vnd.wap.wml',
                                                             'gui.quick_5': 'TestActionGui',
                                                             'view.results.tree.renderers_order': '.RenderAsText,.RenderAsRegexp,.RenderAsBoundaryExtractor,.RenderAsCssJQuery,.RenderAsXPath,org.apache.jmeter.extractor.json.render.RenderAsJsonRenderer,.RenderAsHTML,.RenderAsHTMLFormatted,.RenderAsHTMLWithEmbedded,.RenderAsDocument,.RenderAsJSON,.RenderAsXML',
                                                             'gui.quick_8': 'DebugSampler',
                                                             'csvdataset.file.encoding_list': 'UTF-8|UTF-16|ISO-8859-15|US-ASCII',
                                                             'user.properties': 'user.properties',
                                                             'gui.quick_7': 'JSR223PreProcessor',
                                                             'upgrade_properties': '/bin/upgrade.properties',
                                                             'cssParser.className': 'org.apache.jmeter.protocol.http.parser.CssParser',
                                                             'jmeter.reportgenerator.apdex_tolerated_threshold': '1500',
                                                             'gui.quick_9': 'ViewResultsFullVisualizer',
                                                             'sampleresult.timestamp.start': 'true',
                                                             'not_in_menu': 'org.apache.jmeter.protocol.mongodb.sampler.MongoScriptSampler,org.apache.jmeter.protocol.mongodb.config.MongoSourceElement,org.apache.jmeter.timers.BSFTimer,org.apache.jmeter.modifiers.BSFPreProcessor,org.apache.jmeter.extractor.BSFPostProcessor,org.apache.jmeter.assertions.BSFAssertion,org.apache.jmeter.visualizers.BSFListener,org.apache.jmeter.protocol.java.sampler.BSFSampler,org.apache.jmeter.protocol.http.control.gui.SoapSamplerGui',
                                                             'gui.quick_0': 'ThreadGroupGui',
                                                             'gui.quick_2': 'RegexExtractorGui',
                                                             'gui.quick_1': 'HttpTestSampleGui',
                                                             'gui.quick_4': 'ConstantTimerGui',
                                                             'HTTPResponse.parsers': 'htmlParser wmlParser cssParser',
                                                             'gui.quick_3': 'AssertionGui',
                                                             'remote_hosts': '127.0.0.1'}}, 'parameters': '',
                            'script': '', 'enabled': True}, 'id': '1532598f-8a67-430a-a0b5-8d9b5e5d99e9',
         'projectId': '11406dc7-8340-401f-813f-3511a97d3fbb',
         'clazzName': 'io.metersphere.api.dto.definition.request.processors.pre.MsJSR223PreProcessor'},
        {'jsr223': [], 'resourceId': 'ea594a82-dc9c-4090-83d7-1fb19fbaae1b', 'mockEnvironment': False,
         'document': {'type': 'JSON',
                      'data': {'json': [], 'include': False, 'xmlFollowAPI': 'false', 'typeVerification': False,
                               'xml': [], 'jsonFollowAPI': 'false'}, 'enable': True}, 'xpath2': [], 'active': False,
         'index': '2', 'markStep': False, 'jsonPath': [
            {'valid': True, 'expect': '@@time@@', 'expression': '$.data.currentSystemTime', 'enable': True,
             'description': '$.data.currentSystemTime CONTAINS: @@time@@', 'type': 'JSON', 'option': 'CONTAINS'}],
         'type': 'Assertions', 'isMockEnvironment': False, 'xpathType': 'xml',
         'duration': {'valid': False, 'type': 'Duration', 'value': 0, 'enable': True}, 'regex': [],
         'scenarioAss': False, 'enable': True, 'hashTree': [], 'id': '5d98d0f7-245f-4bdd-4545-d59ae573c315',
         'projectId': '11406dc7-8340-401f-813f-3511a97d3fbb',
         'clazzName': 'io.metersphere.api.dto.definition.request.assertions.MsAssertions'}],
               'id': '9862d874-bd3e-4b3b-8b7d-583776263709', 'responseTimeout': '150000', 'headers': [
        {'valid': True, 'file': False, 'enable': True, 'name': 'Content-Type', 'value': 'application/json',
         'urlEncode': False, 'required': True},
        {'valid': False, 'file': False, 'urlEncode': False, 'enable': True, 'required': True}], 'rest': [
        {'valid': False, 'file': False, 'enable': True, 'type': 'text', 'contentType': 'text/plain', 'urlEncode': False,
         'required': False}], 'method': 'GET', 'mockEnvironment': False, 'active': True, 'index': '2', 'url': '',
               'customizeReq': False, 'versionId': 'adee882c-f0bc-4279-8274-d03c6436c9c0', 'referenced': 'Copy',
               'domain': 'http://dfl.qa-test.storicard-qa.com', 'name': '查询系统时间', 'arguments': [
        {'valid': True, 'file': False, 'enable': True, 'name': 't', 'type': 'text', 'value': '1677822209382',
         'contentType': 'text/plain', 'urlEncode': False, 'required': True},
        {'valid': False, 'min': 0, 'file': False, 'max': 0, 'enable': True, 'type': 'text', 'contentType': 'text/plain',
         'urlEncode': False, 'required': False}], 'projectId': '11406dc7-8340-401f-813f-3511a97d3fbb',
               'clazzName': 'io.metersphere.api.dto.definition.request.sampler.MsHTTPSamplerProxy',
               'doMultipartPost': False}

def fibonacci(get_data, dds):
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
        if get_data["path"] == "/api/admin/system/faketime":
            get_raw = json.loads(get_data["body"]["raw"])
            if str(get_raw["time"]).count("__timeShift") > 0:
                print()
            else:
                dds.append(get_raw["time"])
        get_data['referenced'] = 'Copy'
    elif get_data["type"] == "scenario" and get_data["enable"] == True:
        hashTree = get_data["hashTree"]
        get_data['referenced']='Copy'
        for subScenario in hashTree:
            fibonacci(subScenario, dds)
def fibonacci_replace(get_data, test_id):

    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
        if get_data["path"] == "/api/admin/system/faketime":
            get_raw = json.loads(get_data["body"]["raw"])
            if str(get_raw["time"]).count("__timeShift") > 0:
                print()
        elif get_data["path"] == "/api/dflRegister":
            # get_data['arguments']
            # get_data['script']
            # get_data['body']
            # get_data['hashTree']
            get_data_tmp=(str(get_data).replace("userName", "userName" + str(test_id)))
            get_data = literal_eval(get_data_tmp)

        elif get_data["path"] == ("/api/dflLogin/") :
            get_data_tmp = (str(get_data).replace("userName", "userName" + str(test_id)))
            get_data = literal_eval(get_data_tmp)
        elif get_data["path"] == ("/api/contract"):
            get_data_tmp = (str(get_data).replace("userName", "userName" + str(test_id))
                                .replace("userId", "userId" + str(test_id))
                                .replace("accountId", "accountId" + str(test_id))
                                .replace("cardId", "cardId" + str(test_id))
                                .replace("pomeloUserId", "pomeloUserId" + str(test_id))
                                .replace("pomeloCardId", "pomeloCardId" + str(test_id))
                                .replace("customerId", "customerId" + str(test_id))
                                .replace("contractId", "contractId" + str(test_id))
                                .replace("productCode", "productCode" + str(test_id))
                                )
            get_data = literal_eval(get_data_tmp)
        elif get_data["path"] == ("/api/addContract"):
            get_data_tmp = (str(get_data).replace("userName", "userName" + str(test_id))
                            .replace("userId", "userId" + str(test_id))
                            .replace("accountId", "accountId" + str(test_id))
                            .replace("cardId", "cardId" + str(test_id))
                            .replace("pomeloUserId", "pomeloUserId" + str(test_id))
                            .replace("pomeloCardId", "pomeloCardId" + str(test_id))
                            .replace("customerId", "customerId" + str(test_id))
                            .replace("contractId", "contractId" + str(test_id))
                            .replace("productCode", "productCode" + str(test_id))
                            )
            get_data = literal_eval(get_data_tmp)
        elif get_data["path"] == ("/backoffice/dfl/credit/statement/unsettled"):
            get_data_tmp = (str(get_data).replace("${accountId}", "${accountId" + str(test_id)+"}")
                            )
            get_data = literal_eval(get_data_tmp)


    if get_data["type"]=="JDBCSampler" and get_data["enable"] == True:
        print()

    elif get_data["type"] == "scenario" and get_data["enable"] == True:
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            fibonacci_replace(subScenario, test_id)

def fibonacci1(get_data, get_time_line_dict,test_id):
    if get_time_line_dict=={}:
        get_time_line_dict.update({"2099-01-01 00:00:00":[]})
        for get_one_hash_tree in get_data["hashTree"]:
            if get_one_hash_tree["type"] == "scenario" and get_one_hash_tree["enable"] == True:
                get_time_line_dict["2099-01-01 00:00:00"].append(get_one_hash_tree)
            elif get_one_hash_tree["type"] == "HTTPSamplerProxy" and get_one_hash_tree["enable"] == True:
                get_time_line_dict["2099-01-01 00:00:00"].append(get_one_hash_tree)
        return
    get_cur_day = ""
    for get_one_hash_tree in get_data["hashTree"]:
        if get_one_hash_tree["type"] == "scenario" and get_one_hash_tree["enable"] == True:
            hashTree = get_one_hash_tree["hashTree"]
            get_one_hash_tree['referenced']='Copy'
            get_one_hash_tree['name']=get_one_hash_tree['name']+"_"+str(test_id)
            #时间
            if str(hashTree).count("/api/admin/system/faketime") > 0:
                if str(hashTree[0]).count("__timeShift") > 0:
                    print()
                else:
                    # print(hashTree[0]["name"])
                    # if hashTree[0]["name"]=="交易查询":
                    #   print()
                    #出在这个问题可能时间没按规则来
                    get_raw = json.loads(hashTree[0]["body"]["raw"])
                    get_cur_day = get_raw["time"]
                get_data_tmp = (str(get_one_hash_tree).replace("${accountId}", "${accountId" + str(test_id) + "}"))
                get_data_dict = literal_eval(get_data_tmp)
                get_time_line_dict[get_cur_day].append(get_data_dict)
                # get_time_line_dict[get_cur_day].append(get_one_hash_tree)
            elif str(hashTree).count("/api/addContract")>0:
                get_tmp_str__hash_tree=str(get_one_hash_tree)
                get_data_tmp = (get_tmp_str__hash_tree.replace("userName", "userName" + str(test_id))
                                .replace("userId", "userId" + str(test_id))
                                .replace("accountId", "accountId" + str(test_id))
                                .replace("cardId", "cardId" + str(test_id))
                                .replace("pomeloUserId", "pomeloUserId" + str(test_id))
                                .replace("pomeloCardId", "pomeloCardId" + str(test_id))
                                .replace("customerId", "customerId" + str(test_id))
                                .replace("contractId", "contractId" + str(test_id))
                                .replace("productCode", "productCode" + str(test_id))
                                )

                get_data_tmp=(get_data_tmp.replace("subproductCode"+str(test_id),"subproductCode")
                              .replace("productCode"+str(test_id)+"\":", "productCode\":")
                              )

                get_data_dict = literal_eval(get_data_tmp)
                #特殊处理
                get_data_dict['hashTree'][1]['hashTree'][2]["arguments"][0]["name"]="accountId"
                get_time_line_dict[get_cur_day].append(get_data_dict)

            elif str(hashTree).count("/transactions/authorizations") > 0 or str(hashTree).count("/backoffice/dfl-ng/credit/authorizations/posting") > 0:
                get_data_tmp = (str(get_one_hash_tree).replace("userName", "userName" + str(test_id))
                                .replace("userId", "userId" + str(test_id))
                                .replace("${accountId}", "${accountId" + str(test_id)+"}")
                                .replace("cardId", "cardId" + str(test_id))
                                .replace("pomeloUserId", "pomeloUserId" + str(test_id))
                                .replace("pomeloCardId", "pomeloCardId" + str(test_id))
                                .replace("customerId", "customerId" + str(test_id))
                                .replace("contractId", "contractId" + str(test_id))
                                .replace("productCode", "productCode" + str(test_id))
                                )
                get_data_dict = literal_eval(get_data_tmp)
                get_time_line_dict[get_cur_day].append(get_data_dict)
            else:
                get_data_tmp = (str(get_one_hash_tree).replace("${accountId}", "${accountId" + str(test_id) + "}")
                                )
                get_data_dict = literal_eval(get_data_tmp)
                get_time_line_dict[get_cur_day].append(get_data_dict)
        elif get_one_hash_tree["type"] == "HTTPSamplerProxy" and get_one_hash_tree["enable"] == True:
            get_one_hash_tree['name'] = get_one_hash_tree['name'] + "_" + str(test_id)
            if str(get_one_hash_tree).count("/api/admin/system/faketime"):
                if str(get_one_hash_tree).count("__timeShift") > 0:
                    print()
                else:
                    get_raw = json.loads(get_one_hash_tree["body"]["raw"])
                    get_cur_day = get_raw["time"]

                get_time_line_dict[get_cur_day].append(get_one_hash_tree)
            elif str(get_one_hash_tree).count("/transactions/authorizations") > 0 or str(get_one_hash_tree).count("/backoffice/dfl-ng/credit/authorizations/posting") > 0:
                get_data_tmp = (str(get_one_hash_tree).replace("userName", "userName" + str(test_id))
                                .replace("userId", "userId" + str(test_id))
                                .replace("accountId", "accountId" + str(test_id))
                                .replace("cardId", "cardId" + str(test_id))
                                .replace("pomeloUserId", "pomeloUserId" + str(test_id))
                                .replace("pomeloCardId", "pomeloCardId" + str(test_id))
                                .replace("customerId", "customerId" + str(test_id))
                                .replace("contractId", "contractId" + str(test_id))
                                .replace("productCode", "productCode" + str(test_id)))

                get_data_dict = literal_eval(get_data_tmp)
                get_time_line_dict[get_cur_day].append(get_data_dict)
            else:
                get_time_line_dict[get_cur_day].append(get_one_hash_tree)
        elif str(get_one_hash_tree).count("/v1.0/credit/installments/apply")>0:
            get_data_tmp = (str(get_one_hash_tree)
                            .replace("${accountId}", "${accountId" + str(test_id) + "}")
                            .replace("installment_id", "installment_id" + str(test_id))
                            )
            get_data_dict = literal_eval(get_data_tmp)
            get_time_line_dict[get_cur_day].append(get_data_dict)
        else:
            if str(get_one_hash_tree).count("${installment_id}")>0:
                print()
            get_data_tmp = (str(get_one_hash_tree)
                            .replace("${accountId}", "${accountId" + str(test_id) + "}")
                            # .replace("${installmentId}","${installmentId" + str(test_id) + "}")
                            .replace("${installment_id}", "${installment_id" + str(test_id) + "}")
                            # .replace("installment_id", "installment_id" + str(test_id) )
                            )

            get_data_dict = literal_eval(get_data_tmp)
            get_time_line_dict[get_cur_day].append(get_data_dict)

def single_result(id):
    ######
    hash_tree_list = []
    # 3655a904-6b4c-4afb-99a3-a4a41bbf6a35
    hash_tree_1 = MetersphereUtils.get_scenario_list([id])[0]
    hash_tree_1 = json.loads(hash_tree_1["scenarioDefinition"])
    get_name=str(hash_tree_1["name"])
    test_name= (get_name if len(get_name)<10 else get_name[0:10]+"_"+str(hash_tree_1["num"]))
    print("请求：" + test_name)
    get_time_line_array = []
    get_time_line_dict = {}

    fibonacci(hash_tree_1, get_time_line_array)
    for get_time_day in get_time_line_array:
        get_time_line_dict[get_time_day] = []
    # fibonacci_replace(hash_tree_1, hash_tree_1["num"])

    fibonacci1(hash_tree_1, get_time_line_dict, hash_tree_1["num"])

    return  get_time_line_dict,test_name

def split_num(get_ids,num):
    # split_array = [[get_ids[i], get_ids[i + 1] if i+1<len(get_ids) else  get_ids[i] ] for i in range(0, len(get_ids), 2)]
    split_array = []

    step = num
    for i in range(0, len(get_ids), step):
        if i + step > len(get_ids):
            tmp = []
            mod_data=int(math.fmod(i+1, step))
            if mod_data == 2:
                for k in range(i, len(get_ids)):
                    tmp.append(get_ids[k])
                split_array.append(tmp)
            elif mod_data == 1:
                for k in range(i, len(get_ids)):
                    tmp.append(get_ids[k])
                split_array.append(tmp)
        else:
            tmp = []
            for k in range(i, i + step):
                tmp.append(get_ids[k])
            split_array.append(tmp)
    return split_array
if __name__ == '__main__':
    ########获取
    get_ids=MetersphereUtils.get_batch_ids(1,50)

    # 使用列表式进行拆分
    split_array=split_num(get_ids,3)

    print(split_array)
    for get_two in split_array:
        hash_tree_list=[]
        test_name_mix=""
        get_two=list(set(get_two))
        for get_id in get_two:
            get_time_line_dict,test_name=single_result(get_id)
            test_name_mix=test_name_mix+test_name+"_&&_"
            hash_tree_list.append(get_time_line_dict)

        #####组合
        get_time_line_dict_data_all={}
        for get_time_line_dict_data_one in hash_tree_list:
            for get_key in get_time_line_dict_data_one.keys():
                if get_key in get_time_line_dict_data_all.keys():
                    get_list = get_time_line_dict_data_one[get_key]
                    for get_list_one in get_list:
                        get_time_line_dict_data_all[get_key].append(get_list_one)
                else:
                    get_time_line_dict_data_all.update({get_key: get_time_line_dict_data_one[get_key]})
        #排序
        get_time_line_dict_data_all_keys = sorted(get_time_line_dict_data_all.keys())
        hash_tree_list_all = []
        for get_key in get_time_line_dict_data_all_keys:
            for get_one in get_time_line_dict_data_all[get_key]:
                hash_tree_list_all.append(get_one)

        #创建场景
        test_name_mix=test_name_mix+str(int(time.time()))
        print(test_name_mix)
        interface_payload={"principal": "admin", "apiScenarioModuleId": "139570c2-9c3f-4531-a29c-2d2688fc5ab7",
         "modulePath": "/墨西哥和哥伦比亚分期融合/墨西哥交易分期", "name": test_name_mix, "follows": ["jaden.yang"],
         "projectId": "11406dc7-8340-401f-813f-3511a97d3fbb", "id": "1021c11e", "status": "Underway", "level": "P0",
         "bodyFileRequestIds": [], "scenarioFileIds": []}
        data=MetersphereUtils.create(interface_payload)

        get_sce_data = data.get("data").get("scenarioDefinition")
        result = json.loads(get_sce_data)
        # update("scenarioDefinition", hash_tree_1)
        ########优化
        set_time=""
        hash_tree_list_all_opt=[]
        for get_one in hash_tree_list_all:
            if str(get_one).count("/api/admin/system/faketime") > 0 and str(get_one).count("__timeShift")<=0:

                hashTree = get_one["hashTree"]
                get_raw = json.loads(hashTree[0]["body"]["raw"])
                get_cur_day = get_raw["time"]
                if set_time =="" :
                    set_time=get_cur_day
                    hash_tree_list_all_opt.append(get_one)
                elif  set_time==get_cur_day:
                    print()
                else:
                    set_time=get_cur_day
                    hash_tree_list_all_opt.append(get_one)
            elif str(get_one).count("__timeShift") > 0:
                print()
            else:
                hash_tree_list_all_opt.append(get_one)

        # todo
        result["hashTree"] = hash_tree_list_all_opt

        data["data"]["scenarioDefinition"] = result
        # data["data"]["scenarioDefinition"] = json.dumps(result, ensure_ascii=False)
        get_post_data = data["data"]
        get_update_info = MetersphereUtils.update(get_post_data)
        print("*************")
        print(get_update_info)
        # print("******设置运行环境***qa-test-dfl-new-eks d2723bd0-7959-4c8f-b4ca-864469a6dc20  *** qa-dfl-new-eks bcef5257-6909-4be8-974c-7238889e26bf")


