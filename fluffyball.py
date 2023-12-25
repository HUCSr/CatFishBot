# 毛球模块

import os
import json
import datetime
import jieba


def init (userID) :
    curr_time = datetime.datetime.now()
    if os.path.exists("user/fluffyball/"+str(userID)+".json") == False:
        User = {"Balls" : 0,
                "LastYER": curr_time.year,
                "LastMON": curr_time.month,
                "LastDAY" : curr_time.day,
                "LastHUR" : curr_time.hour,
                "LastMIN" : curr_time.minute,
                "LastSEC" : curr_time.second,
                "Efficiency" : 0.1
                }
        with open("user/fluffyball/"+str(userID)+".json", 'w', encoding='utf-8') as t:
            json.dump(User, t)
    
    with open("user/fluffyball/"+str(userID)+".json", 'r', encoding='utf-8') as t:
        User = json.load(t)
    if User.get ("Balls") == None:
        User["Balls"] = 0
    if User.get ("LastYER") == None:
        User["LastYER"] = curr_time.year
    if User.get ("LastMON") == None:
        User["LastMON"] = curr_time.month
    if User.get ("LastDAY") == None:
        User["LastDAY"] = curr_time.day
    if User.get ("LastHUR") == None:
        User["LastHUR"] = curr_time.hour
    if User.get ("LastMIN") == None:
        User["LastMIN"] = curr_time.minute
    if User.get ("LastSEC") == None:
        User["LastSEC"] = curr_time.second
    if User.get ("Efficiency") == None:
        User["Efficiency"] = 0.1
    with open("user/fluffyball/"+str(userID)+".json", 'w', encoding='utf-8') as t:
        json.dump(User, t)
        
def update (userID) :
    init (userID)
    with open("user/fluffyball/"+str(userID)+".json", 'r', encoding='utf-8') as t:
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
    
    Productive_Second = (curr_time - last_time).seconds
    
    User["LastYER"] = curr_time.year
    User["LastMON"] = curr_time.month
    User["LastDAY"] = curr_time.day
    User["LastHUR"] = curr_time.hour
    User["LastMIN"] = curr_time.minute
    User["LastSEC"] = curr_time.second
    
    User["Balls"] += Productive_Second * User["Efficiency"]
    
    with open("user/fluffyball/"+str(userID)+".json", 'w', encoding='utf-8') as t:
        json.dump(User, t)
        
def info (userID) :
    update (userID)
    with open("user/fluffyball/"+str(userID)+".json", 'r', encoding='utf-8') as t:
        User = json.load(t)
    return [User["Balls"],User["Efficiency"]]
    