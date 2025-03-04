

def DQBucketAccordingDays(dqDays) :
    if (dqDays <=0) :
        return -1
    if (dqDays >=1 and dqDays <=14) :
        return 0
    if (dqDays >=15 and dqDays <=29) :
        return 1
    if (dqDays >=30 and dqDays <=59) :
        return 2
    if (dqDays >=60 and dqDays <=89) :
        return 3
    if (dqDays >=90 and dqDays <=179) :
        return 4
    return 5

def DQReasonAccordingDays(dqDays) :
    if (dqDays <=0) :
        return ""
    if (dqDays >=1 and dqDays <=14) :
        return "DQ1-14"
    if (dqDays >=15 and dqDays <=29) :
        return "DQ15-29"
    if (dqDays >=30 and dqDays <=59) :
        return "DQ30-59"
    if (dqDays >=60 and dqDays <=89) :
        return "DQ60-89"
    if (dqDays >=90 and dqDays <=179) :
        return "DQ90-179"
    return "DQ180\\+"
    