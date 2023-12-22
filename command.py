import os
import json
import datetime
import jieba

# 打卡模块
def sign_in(userID) :
    if os.path.exists("user/signin/"+str(userID)+".json") == False:
        User = {"LastYear": 2020,
                "LastMonth": 1,
                "LastDay" : 1,
                "TotleDays": 0,
                "Combo": 0,
                "LoseCombo" : 0}
        with open("user/signin/"+str(userID)+".json", 'w', encoding='utf-8') as t:
            json.dump(User, t)
    with open("user/signin/"+str(userID)+".json", 'r', encoding='utf-8') as t:
        User = json.load(t)
        
    curr_time = datetime.datetime.now()
    if str(User["LastYear"]) == str(curr_time.year) and \
       str(User["LastMonth"]) == str(curr_time.month) and \
       str(User["LastDay"]) == str(curr_time.day):
           return [-1]
    else :
        pre_time = curr_time - datetime.timedelta(days=1)
        last_time = datetime.datetime(int(User["LastYear"]),
                                      int(User["LastMonth"]),
                                      int(User["LastDay"]))
        if pre_time.year == last_time.year and \
            pre_time.month == last_time.month and \
            pre_time.day == last_time.day:
            User["Combo"] += 1
        else:
            if User["LastYear"] == 2020:
                User["Combo"] += 1
            else:
                User["Combo"] = 0
                User["LoseCombo"] += 1
        User["LastYear"] = curr_time.year
        User["LastMonth"] = curr_time.month
        User["LastDay"] = curr_time.day
        User["TotleDays"] += 1
        with open("user/signin/"+str(userID)+".json", 'w', encoding='utf-8') as t:
            json.dump(User, t)
        return [User["Combo"],User["LoseCombo"],User["TotleDays"]]

# 睡觉模块
def sleep (userID) :
    if os.path.exists("user/sleep/"+str(userID)+".json") == False:
        User = {"LastYear": 2020,
                "LastMonth": 1,
                "LastDay" : 1,
                "LastHour" : 1,
                "LastMinute" : 1,
                "LastSecond" : 1,
                "TotleMinutes": 0,
                "TotleTimes": 0,
                "InSleep" : 0}
        with open("user/sleep/"+str(userID)+".json", 'w', encoding='utf-8') as t:
            json.dump(User, t)
    with open("user/sleep/"+str(userID)+".json", 'r', encoding='utf-8') as t:
        User = json.load(t)
    if User["InSleep"] == 1:
        return False
    else:
        curr_time = datetime.datetime.now()
        User["InSleep"] = 1
        User["TotleTimes"] += 1
        User["LastYear"] = curr_time.year
        User["LastMonth"] = curr_time.month
        User["LastDay"] = curr_time.day
        User["LastHour"] = curr_time.hour
        User["LastMinute"] = curr_time.minute
        User["LastSecond"] = curr_time.second
        with open("user/sleep/"+str(userID)+".json", 'w', encoding='utf-8') as t:
            json.dump(User, t)
        return True

# 起床模块
def weak_up (userID) :
    if os.path.exists("user/sleep/"+str(userID)+".json") == False:
        User = {"LastYear": 2020,
                "LastMonth": 1,
                "LastDay" : 1,
                "LastHour" : 1,
                "LastMinute" : 1,
                "LastSecond" : 1,
                "TotleMinutes": 0,
                "TotleTimes": 0,
                "InSleep" : 0}
        with open("user/sleep/"+str(userID)+".json", 'w', encoding='utf-8') as t:
            json.dump(User, t)
    with open("user/sleep/"+str(userID)+".json", 'r', encoding='utf-8') as t:
        User = json.load(t)
    if User["InSleep"] == 0:
        return [-1]
    else:
        curr_time = datetime.datetime.now()
        sleep_time = datetime.datetime(
            User["LastYear"],
            User["LastMonth"],
            User["LastDay"],
            User["LastHour"],
            User["LastMinute"],
            User["LastSecond"]
        )
        User["InSleep"] = 0
        Sleep_Second = (curr_time - sleep_time).seconds
        User["TotleMinutes"] += Sleep_Second
        Sleep_Minute = int(Sleep_Second/60)
        Sleep_Second = Sleep_Second % 60
        Sleep_Hour = int(Sleep_Minute/60)
        Sleep_Minute = Sleep_Minute % 60
        with open("user/sleep/"+str(userID)+".json", 'w', encoding='utf-8') as t:
            json.dump(User, t)
        return [Sleep_Hour,Sleep_Minute,Sleep_Second]
    
# 词云模块
def word_cloud () :
    wordCloud = {}
    with open("resource/reply.json", 'r', encoding='utf-8') as t:
        reply = json.load(t)
    with open("resource/filterwords.json", 'r', encoding='utf-8') as t:
        filter = json.load(t)
    for msg in reply:
        message = list (jieba.cut(msg))
        for word in message:
            if wordCloud.get (word) == None:
                wordCloud[word] = 0
            wordCloud[word] += 1
    sorted_wordCloud = dict(sorted(wordCloud.items(), key=lambda x: -x[1]))
    wordCloud = []
    for word in sorted_wordCloud:
        if len (wordCloud) >= 10:
            break
        if filter.get (word) == None:
            wordCloud.append ([word,sorted_wordCloud[word]])
    return wordCloud