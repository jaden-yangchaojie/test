import MexScenarioHandler
import MexHandlerProcess
import MexInitData

def handler_process(id):
    scenario_id= MexScenarioHandler.get_scenario_detail_id_by_search_id(id) if id.isdigit() else id
    get_list = MexScenarioHandler.get_scenario_detail(scenario_id)
    get_init_data = MexInitData.init_data(get_list)
    MexHandlerProcess.handler(get_list, get_init_data)

if __name__ == '__main__':
    #输入用例id
    handler_process("bd1f3a6b-4547-4fa6-9121-aa8438af5724")


