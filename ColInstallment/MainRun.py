import ColScenarioHandler
import HandlerProcess
import InitData

def handler_process(id):
    scenario_id= ColScenarioHandler.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    get_list = ColScenarioHandler.get_scenario_detail(scenario_id)
    get_init_data = InitData.init_data(get_list)
    HandlerProcess.handler(get_list, get_init_data)

if __name__ == '__main__':
    #输入用例id
    handler_process("f9447bb5-5b1c-4e86-8c77-4483201073af")
    # handler_process("100651")

