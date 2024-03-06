import json
import os
import datetime
import random

def Init (UserId) :
    if os.path.exists("user/CatFishsh/"+str(UserId)+".json") == False:
        User = {"LastYER": 2020,
                "LastMON": 1,
                "LastDAY" : 1,
                "LastHUR" : 1,
                "LastMIN" : 1,
                "LastSEC" : 1,
                "NowFish" : 0,
                "NowBall" : 0,
                "NowLevel" : 0,
                "TotleBall": 0,
                "PriceIncrease": 1.0,
                "RateIncrease" : 1.0,
                "MultiplierIncrease" : 1.0,
                "GrowthIncrease" : 1.0}
        with open("user/CatFishsh/"+str(UserId)+".json", 'w', encoding='utf-8') as t:
            json.dump(User, t)

def update (UserId) :
    with open("user/CatFishsh/"+str(UserId)+".json", 'r', encoding='utf-8') as t:
        User = json.load(t)
    curr_time = datetime.datetime.now()
    last_time = datetime.datetime(
        User["LastYER"],
        User["LastMON"],
        User["LastDAY"],
        User["LastHUR"],
        User["LastMIN"],
        User["LastSEC"]
    )
    
    with open("resource/catfishsh.json", 'r', encoding='utf-8') as t:
        catfishsh = json.load(t)
    idx = 0
    nowcatfishsh = ""
    for i in catfishsh:
        idx += 1
        if (idx == User["NowFish"]):
            nowcatfishsh = i

    Productive_Minute = (curr_time - last_time).seconds // 60
    
    User["LastYER"] = curr_time.year
    User["LastMON"] = curr_time.month
    User["LastDAY"] = curr_time.day
    User["LastHUR"] = curr_time.hour
    User["LastMIN"] = curr_time.minute
    User["LastSEC"] = 0
    
    User["NowBall"] += Productive_Minute * int(1 * catfishsh[nowcatfishsh]["Growth"] * User["GrowthIncrease"])
    
    with open("user/CatFishsh/"+str(UserId)+".json", 'w', encoding='utf-8') as t:
        json.dump(User, t)
        
  
def info (UserId) :
    Init (UserId)
    with open("user/CatFishsh/"+str(UserId)+".json", 'r', encoding='utf-8') as t:
        User = json.load(t)
    with open("resource/catfishsh.json", 'r', encoding='utf-8') as t:
        catfishsh = json.load(t)
    if User["NowFish"] == 0:
        txt = "当前毛玉玉: 无\n"
        txt += "当前可种植的毛玉玉:\n"
        idx = 0
        for i in catfishsh:
            idx += 1
            txt += "<" + str(idx) + "> " + i + '\n'
        return txt

    update (UserId)
    with open("user/CatFishsh/"+str(UserId)+".json", 'r', encoding='utf-8') as t:
        User = json.load(t)
    txt = "当前毛玉玉: "
    idx = 0
    nowcatfishsh = ""
    for i in catfishsh:
        idx += 1
        if (idx == User["NowFish"]):
            nowcatfishsh = i
    txt += nowcatfishsh
    txt += "[Lv." +  str(User["NowLevel"]) + "]\n"
    txt += "当前生产速度: " + str(int(1 * catfishsh[nowcatfishsh]["Growth"] * User["GrowthIncrease"])) + "/分\n"
    txt += "当前可收获量: " + str(int(User["NowBall"] * catfishsh[nowcatfishsh]["Price"] * User["PriceIncrease"])) + "\n"
    txt += "下等级可收获量: " + str(int(User["NowBall"] * (1.2 + catfishsh[nowcatfishsh]["Multiplier"] - 1.0) * catfishsh[nowcatfishsh]["Price"] * User["PriceIncrease"])) + "\n"
    txt += "升级成功率: " + str(int(min(max(95 - User["NowLevel"] * 5,30) * catfishsh[nowcatfishsh]["Rate"] * User["RateIncrease"],100))) + "% \n"
    return txt

def plant (UserId,FishId) :
    Init (UserId)
    with open("user/CatFishsh/"+str(UserId)+".json", 'r', encoding='utf-8') as t:
        User = json.load(t)
    if User["NowFish"] != 0:
        return "当前已经有毛玉玉在生长中"
    with open("resource/catfishsh.json", 'r', encoding='utf-8') as t:
        catfishsh = json.load(t)
    if (FishId <=0 or FishId > len(catfishsh)):
        return "毛玉玉编号出错"
    curr_time = datetime.datetime.now()
    User["LastYER"] = curr_time.year
    User["LastMON"] = curr_time.month
    User["LastDAY"] = curr_time.day
    User["LastHUR"] = curr_time.hour
    User["LastMIN"] = curr_time.minute
    User["LastSEC"] = 0
    User["NowFish"] = FishId
    User["NowBall"] = 0
    User["NowLevel"] = 1
    with open("user/CatFishsh/"+str(UserId)+".json", 'w', encoding='utf-8') as t:
        json.dump(User, t)
    return "种植成功"

def harvest (UserId):
    Init (UserId)
    with open("user/CatFishsh/"+str(UserId)+".json", 'r', encoding='utf-8') as t:
        User = json.load(t)
    if User["NowFish"] == 0:
        return "当前没有毛玉玉在生长中哦"
    with open("resource/catfishsh.json", 'r', encoding='utf-8') as t:
        catfishsh = json.load(t)
    update (UserId)
    with open("user/CatFishsh/"+str(UserId)+".json", 'r', encoding='utf-8') as t:
        User = json.load(t)
    idx = 0
    nowcatfishsh = ""
    for i in catfishsh:
        idx += 1
        if (idx == User["NowFish"]):
            nowcatfishsh = i
    User["NowFish"] = 0
    User["TotleBall"] += int(User["NowBall"] * catfishsh[nowcatfishsh]["Price"] * User["PriceIncrease"])
    with open("user/CatFishsh/"+str(UserId)+".json", 'w', encoding='utf-8') as t:
        json.dump(User, t)
    return "收获成功,总共收获了 " + str(int(User["NowBall"] * catfishsh[nowcatfishsh]["Price"] * User["PriceIncrease"])) + " 个毛球,当前总共有 " + str(User["TotleBall"]) + " 个毛球"

def levelUP (UserId) :
    Init (UserId)
    with open("user/CatFishsh/"+str(UserId)+".json", 'r', encoding='utf-8') as t:
        User = json.load(t)
    if User["NowFish"] == 0:
        return "当前没有毛玉玉在生长中哦"
    with open("resource/catfishsh.json", 'r', encoding='utf-8') as t:
        catfishsh = json.load(t)
    update (UserId)
    idx = 0
    nowcatfishsh = ""
    for i in catfishsh:
        idx += 1
        if (idx == User["NowFish"]):
            nowcatfishsh = i
    Rate = int(min(max(95 - User["NowLevel"] * 5,30) * catfishsh[nowcatfishsh]["Rate"] * User["RateIncrease"],100))
    if random.randint(0, 100) <= Rate:
        User["NowLevel"] += 1
        User["NowBall"] = int(User["NowBall"] * (1.2 + catfishsh[nowcatfishsh]["Multiplier"] - 1.0) * catfishsh[nowcatfishsh]["Price"] * User["PriceIncrease"])
        with open("user/CatFishsh/"+str(UserId)+".json", 'w', encoding='utf-8') as t:
            json.dump(User, t)
        return "升级成功"
    else :
        User["NowFish"] = 0
        User["TotleBall"] += int(User["NowBall"] * 0.1)
        with open("user/CatFishsh/"+str(UserId)+".json", 'w', encoding='utf-8') as t:
            json.dump(User, t)
        return "升级失败,收获了 " + str(int(User["NowBall"] * 0.1)) + " 个毛球,当前总共有 " + str(User["TotleBall"]) + " 个毛球"

def test () :
    x = 1
    if x == 0 :
        return levelUP (112)
    