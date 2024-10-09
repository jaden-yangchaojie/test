import ColScenarioHandler
import HandlerProcess
import InitData

def handler_process(id):
    scenario_id= ColScenarioHandler.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    get_list = ColScenarioHandler.get_scenario_detail(scenario_id)
    get_init_data = InitData.init_data(get_list)
    HandlerProcess.handler(get_list, get_init_data)

if __name__ == '__main__':
    #输入用例id,必须是哥伦比亚相关
    handler_process("fa981a71-eeb9-40d7-b67a-e4fcb5f886a4")
    # handler_process("100651")

