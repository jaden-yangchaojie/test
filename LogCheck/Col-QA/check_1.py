import time
from time import sleep
#

import subprocess
# 执行一个Linux命令
def execute_command(cmd):
    # 使用subprocess.run来执行命令
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    # 返回命令的输出和错误信息
    return result.stdout, result.stderr

if __name__ == '__main__':
    import subprocess

    # obj = subprocess.Popen(["/Users/ycj/pytest/pytest/.venv/bin/python"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    #                        universal_newlines=True)
    # obj.stdin.write("kubectl get pods\n")
    # obj.stdin.write('print(2) \n')
    # out, err = obj.communicate()
    # print(out)
    import subprocess

    p1 = subprocess.Popen(['df', '-Th'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', 'data'], stdin=p1.stdout, stdout=subprocess.PIPE)
    out, err = p2.communicate()
    print(out)

    # cmd = ()
    # output, error = execute_command(cmd)
    # for get_one in output.split("\n"):
    #     if get_one.count("trading-")>0 or get_one.count("statement-")>0 or get_one.count("viewx-")>0:
    #         try:
    #             get_one = get_one.split(" ")[0]
    #             print(get_one)
    #             # get_gramm=str.format('kubectl -n colombia exec -it {} grep "Excep" logs/run/common-error.log|grep 2022',get_one)
    #             # print (get_gramm)
    #             # get_info=subprocess.check_output( get_gramm,shell=True)
    #             # with open(get_one+str(int(time.time()))+'.txt', 'w') as file:
    #             #     file.write(get_info.decode("utf-8"))
    #             #     file.close()
    #             # statement ->credit-view
    #             if get_one.count("statement-")>0:
    #                 get_gramm = str.format(
    #                     'kubectl -n colombia exec -it {} grep "ERROR" logs/credit-view/common-error.log', get_one)
    #                 print(get_gramm)
    #                 # get_info = subprocess.run(["kubectl","-n","colombia","exec","-it",get_one, "grep" ,"ERROR","logs/credit-view/common-error.log"])
    #                 get_info = subprocess.getoutput()
    #                 with open(get_one+".credit-view" + str(int(time.time())) + '.txt', 'w') as file:
    #                     file.write(get_info.decode("utf-8"))
    #                     file.close()
    #         except Exception:
    #             print("正常报错")



