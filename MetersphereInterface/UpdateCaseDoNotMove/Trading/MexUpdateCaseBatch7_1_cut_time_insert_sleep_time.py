import json
import re

from jsonpath import jsonpath

from MetersphereInterface import MetersphereUtils


def only_find(get_data, insert_hash_tree_data):
    if get_data["type"] == "HTTPSamplerProxy" and get_data["enable"] == True:
        # print(get_data["path"])
        # 如果是存款接口不用处理
        if str(get_data["path"]).count("/api/credit/currentSystemTime") > 0:
            print(str(get_data["path"]))
            sub_hashTree = get_data["hashTree"]
            if str(sub_hashTree[0]).count("ConstantTimer"):
                sub_hashTree[0] = insert_hash_tree_data
                get_data["hashTree"] = sub_hashTree
                print("chuli ")
    # if get_data["type"] == "LoopController" and get_data["enable"] == True:
    #     hashTree = get_data["hashTree"]
    #     for subScenario in hashTree:
    #         only_find(subScenario, insert_hash_tree_data)
    if get_data["type"] == "scenario" and get_data["enable"] == True and 'referenced' in get_data and (
            get_data['referenced'] == "Copy" or get_data['referenced'] == 'Created'):
        hashTree = get_data["hashTree"]
        for subScenario in hashTree:
            only_find(subScenario, insert_hash_tree_data)


def fibonacci_handler(result, insert_hash_tree_data):
    hashTree = result["hashTree"]
    only_find(result, insert_hash_tree_data)
    result["hashTree"] = hashTree


def handler_process_data(id, insert_hash_tree_data):
    scenario_id = MetersphereUtils.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    data = MetersphereUtils.get_scenario_detail_all_info(scenario_id)
    get_sce_data = data.get("data").get("scenarioDefinition")
    result = json.loads(get_sce_data)
    # todo
    fibonacci_handler(result, insert_hash_tree_data)

    data["data"]["scenarioDefinition"] = result
    get_post_data = data["data"]
    # get_daa=json.dumps(get_post_data)
    get_info_udpate = MetersphereUtils.update_scenario_detail(get_post_data)
    print(get_info_udpate)


if __name__ == '__main__':
    # 输入用例id

    module_ids = [
  "b2a54dc5-21f0-4aed-970b-037f1ef56cbe",
  "28859d83-4947-4c45-94cb-01f5c41a6006",
  "859a5a9f-29b9-4753-a891-953e62cfc2e8",
  "c3865a04-64fc-4521-8082-6055466f97c3"
]
    # 第3期
    #     module_ids=[
    #   "eeb26f37-182b-41ee-bc19-3e30ab5b05cc"
    # ]

    get_ids = MetersphereUtils.get_batch_ids(1, 50, module_ids)
    # get_ids = ["e4de14f4-4675-4c78-a177-3b6bec48ea5b"]
    for get_id in get_ids:
        handler_process_data(get_id, {'resourceId': 'c527034c-de55-491a-90a9-1d24e713d906', 'mockEnvironment': False,
                                      'scriptLanguage': 'beanshell', 'num': '', 'active': True, 'index': '1',
                                      'markStep': False, 'type': 'JSR223PreProcessor', 'isMockEnvironment': False,
                                      'script': 'import org.apache.jmeter.config.Arguments;\n\n// 可到http://10.82.74.159:8081/#/project/env，编辑对应的项目环境——> 通用配置， 查看环境变量定义的值。\nint systemUpdateTime = ${systemUpdateTime};\nThread.sleep(systemUpdateTime);',
                                      'jsrEnable': True, 'enable': True, 'name': 'JSR223PreProcessor', 'hashTree': [],
                                      'shellProcessor': {'filename': '', 'cacheKey': '', 'runningVersion': False,
                                                         'scriptLanguage': '', 'name': 'JSR223PreProcessor',
                                                         'searchableTokens': ['TestElement.enabled', 'true',
                                                                              'TestElement.name', 'JSR223PreProcessor',
                                                                              'cacheKey', 'false',
                                                                              'TestElement.test_class',
                                                                              'JSR223PreProcessor',
                                                                              'TestElement.gui_class',
                                                                              'org.apache.jmeter.testbeans.gui.TestBeanGUI',
                                                                              'scriptLanguage', 'beanshell', 'script',
                                                                              'import org.apache.jmeter.config.Arguments;\n\n// 可到http://10.82.74.159:8081/#/project/env，编辑对应的项目环境——> 通用配置， 查看环境变量定义的值。\nint systemUpdateTime = ${systemUpdateTime};\nThread.sleep(systemUpdateTime);'],
                                                         'comment': '', 'propMap': {
                                              'TestElement.test_class': {'stringValue': 'JSR223PreProcessor',
                                                                         'runningVersion': False, 'intValue': 0,
                                                                         'name': 'TestElement.test_class',
                                                                         'floatValue': 0,
                                                                         'objectValue': 'JSR223PreProcessor',
                                                                         'booleanValue': False, 'doubleValue': 0,
                                                                         'value': 'JSR223PreProcessor', 'longValue': 0},
                                              'cacheKey': {'stringValue': 'false', 'runningVersion': False,
                                                           'intValue': 0, 'name': 'cacheKey', 'floatValue': 0,
                                                           'booleanValue': False, 'objectValue': False,
                                                           'doubleValue': 0, 'value': False, 'longValue': 0},
                                              'TestElement.enabled': {'stringValue': 'true', 'runningVersion': False,
                                                                      'intValue': 0, 'name': 'TestElement.enabled',
                                                                      'floatValue': 0, 'booleanValue': True,
                                                                      'objectValue': True, 'doubleValue': 0,
                                                                      'value': True, 'longValue': 0},
                                              'TestElement.name': {'stringValue': 'JSR223PreProcessor',
                                                                   'runningVersion': False, 'intValue': 0,
                                                                   'name': 'TestElement.name', 'floatValue': 0,
                                                                   'objectValue': 'JSR223PreProcessor',
                                                                   'booleanValue': False, 'doubleValue': 0,
                                                                   'value': 'JSR223PreProcessor', 'longValue': 0},
                                              'scriptLanguage': {'stringValue': 'beanshell', 'runningVersion': False,
                                                                 'intValue': 0, 'name': 'scriptLanguage',
                                                                 'floatValue': 0, 'objectValue': 'beanshell',
                                                                 'booleanValue': False, 'doubleValue': 0,
                                                                 'value': 'beanshell', 'longValue': 0},
                                              'TestElement.gui_class': {
                                                  'stringValue': 'org.apache.jmeter.testbeans.gui.TestBeanGUI',
                                                  'runningVersion': False, 'intValue': 0,
                                                  'name': 'TestElement.gui_class', 'floatValue': 0,
                                                  'objectValue': 'org.apache.jmeter.testbeans.gui.TestBeanGUI',
                                                  'booleanValue': False, 'doubleValue': 0,
                                                  'value': 'org.apache.jmeter.testbeans.gui.TestBeanGUI',
                                                  'longValue': 0}, 'script': {
                                                  'stringValue': 'import org.apache.jmeter.config.Arguments;\n\n// 可到http://10.82.74.159:8081/#/project/env，编辑对应的项目环境——> 通用配置， 查看环境变量定义的值。\nint systemUpdateTime = ${systemUpdateTime};\nThread.sleep(systemUpdateTime);',
                                                  'runningVersion': False, 'intValue': 0, 'name': 'script',
                                                  'floatValue': 0,
                                                  'objectValue': 'import org.apache.jmeter.config.Arguments;\n\n// 可到http://10.82.74.159:8081/#/project/env，编辑对应的项目环境——> 通用配置， 查看环境变量定义的值。\nint systemUpdateTime = ${systemUpdateTime};\nThread.sleep(systemUpdateTime);',
                                                  'booleanValue': False, 'doubleValue': 0,
                                                  'value': 'import org.apache.jmeter.config.Arguments;\n\n// 可到http://10.82.74.159:8081/#/project/env，编辑对应的项目环境——> 通用配置， 查看环境变量定义的值。\nint systemUpdateTime = ${systemUpdateTime};\nThread.sleep(systemUpdateTime);',
                                                  'longValue': 0}}, 'threadContext': {'samplingStarted': False,
                                                                                      'startNextThreadLoop': False,
                                                                                      'recording': False,
                                                                                      'restartNextLoop': False,
                                                                                      'threadNum': 0,
                                                                                      'testLogicalAction': 'CONTINUE',
                                                                                      'samplerContext': {},
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
                                                                                          'remote_hosts': '127.0.0.1'}},
                                                         'parameters': '', 'script': '', 'enabled': True},
                                      'id': '1532598f-8a67-430a-a0b5-8d9b5e5d99e9',
                                      'projectId': '11406dc7-8340-401f-813f-3511a97d3fbb',
                                      'clazzName': 'io.metersphere.api.dto.definition.request.processors.pre.MsJSR223PreProcessor'})
