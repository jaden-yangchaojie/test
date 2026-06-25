for i in range(0,21):
    print(str(i))
#

#
# get_list1=[]
# get_list2=[]
# with open("返现集成测试new新链路&提现集成测试new新链路/testignore1", 'r') as file:
#     get_read = file.readline()
#     while get_read:
#         get_read = file.readline()
#         get_list1.append(get_read)
# with open("返现集成测试new新链路&提现集成测试new新链路/testignore2", 'r') as file:
#     get_read = file.readline()
#     while get_read:
#         get_read = file.readline()
#         get_list2.append(get_read)
#
# get_list_diff=list(set(get_list1)-set(get_list2))
# # print(get_list_diff)
# for get_one in get_list_diff:
#     if str(get_one).count("/v1.0/debit")==0 and str(get_one).count("/v1.0/loan/")==0 and str(get_one).count("collaterals")==0:
#         print(get_one.replace("\n",""))