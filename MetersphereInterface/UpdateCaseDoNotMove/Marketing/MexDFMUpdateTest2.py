import json
import time

import jsonpath

false = False

lastest_data = "|MK20251008212849||1111001000023717|11110011000045871176"
with open('example.csv', 'w') as file:
    for get_oin in range(1,50000):
    # print(str(get_oin)+lastest_data)
    # lines = ['First line.\n', 'Second line.\n', 'Third line.\n']


        file.writelines(str(get_oin)+lastest_data+"\n")

sss=time.time()
with open('merchant3k1.csv', 'w') as file:
    for get_oin in range(3001,6001):
    # print(str(get_oin)+lastest_data)
    # lines = ['First line.\n', 'Second line.\n', 'Third line.\n']


        file.writelines(str(int(sss))+str(get_oin)+","+str((int)(sss))+str(get_oin)+str("name")+",22222"+"\n")

offline_data="|MK|1111001000024352|11110011000047165528|2025-07-20 00:00:00|MXN|5|STC001"
sss=time.time()
with open('winner_offline_5K00.csv', 'w') as file:
    for get_oin in range(1,5001):
    # print(str(get_oin)+lastest_data)
    # lines = ['First line.\n', 'Second line.\n', 'Third line.\n']
        file.writelines(str(int(202410091643061))+str(get_oin)+str(offline_data)+"\n")

