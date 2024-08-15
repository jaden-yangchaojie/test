import time
import subprocess
# 执行一个Linux命令,如果出现returned non-zero exit status 1，是没有捞取到数据
if __name__ == '__main__':

    cmd = ("kubectl -n colombia get pods")
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, error = result.stdout, result.stderr
    for get_one in output.split("\n"):
        if get_one.count("trading-")>0 or get_one.count("statement-")>0 or get_one.count("viewx-")>0:
            try:
                get_one = get_one.split(" ")[0]
                print(get_one)
                get_gramm=str.format('kubectl -n colombia exec -it {} grep "Excep" logs/run/common-error.log|grep 2022',get_one)
                print (get_gramm)
                get_info=subprocess.check_output( get_gramm,shell=True)
                with open(get_one+str(int(time.time()))+'.txt', 'w') as file:
                    file.write(get_info.decode("utf-8"))
                    file.close()
                # statement ->credit-view
                if get_one.count("statement-")>0:
                    get_gramm = str.format(
                        'kubectl -n colombia exec -it {} grep "ERROR" logs/credit-view/common-error.log', get_one)
                    print(get_gramm)
                    get_info = subprocess.check_output(get_gramm,shell=True,universal_newlines=True)
                    with open(get_one+".credit-view" + str(int(time.time())) + '.txt', 'w') as file:
                        file.write(get_info)
                        file.close()
            except Exception as e:
                print(str(e))
            finally:
                print("")



