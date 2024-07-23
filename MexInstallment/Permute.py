from itertools import combinations, permutations

def combine():
    get_list=["purchase","payment","refund","DQ","第一期出账","第二期出账","第三期出账"]

    get_arr=list(set(permutations(get_list,len(get_list))))
    ii=0
    for get_one in get_arr:
        get_o=list(get_one)
        getGD=""
        DQ_rule=True
        DQ_rule1=""

        for i, get_one_split in enumerate(get_o):
        # for get_one_split in get_o:
            if get_one_split=="第一期出账":
               getGD =getGD+"第一期出账"
            elif get_one_split=="第二期出账":
                getGD =getGD+"第二期出账"
            elif get_one_split=="第三期出账":
                getGD = getGD + "第三期出账"
            if get_one_split=="DQ" and not getGD.count("第一期出账"):
                DQ_rule=False
                break
            if get_one_split == "DQ" and i<len(get_o)-1 and get_o[i+1]=="DQ" :
                DQ_rule=False
                break
        if DQ_rule==False:
            continue
        if (((getGD=="第一期出账第二期出账第三期出账" and
                not get_o[len(get_o) - 1]==("第三期出账") and
                not get_o[0]==("第一期出账")) and
                get_o[0]=="purchase") and
                not DQ_rule1=="DQDQ"):
            # and get_o[4] == ("第一期出账")
            ii=ii+1
            print(str(get_one) + str(ii))

#
if __name__ == '__main__':
    combine()