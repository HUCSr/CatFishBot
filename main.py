# -*- coding: utf-8 -*-
import asyncio
import os
import time
import json
import random

import botpy
from botpy import logging, BotAPI
from botpy.ext.command_util import Commands
from botpy.ext.cog_yaml import read
from botpy.message import Message

from threading import Thread

import command
import CatFishsh
import daily
import chat
import touhouquestion

###### 变量区

# 上一次的消息
LastMessage = None

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
_log = logging.get_logger()

# reply 触发概率
reply_triggering_probability = test_config["reply_triggering_probability"]
# reply 接受阈值
reply_acceptance_threshold = test_config["reply_acceptance_threshold"]
# reply 接受概率
reply_acceptance_probability = test_config["reply_acceptance_probability"]

#####

@Commands("打卡")
async def sign_in(api: BotAPI, message: Message, params=None):
    # params 是我指令后面的东西
    event = daily.sign_in(message.author.id)
    if event != None:
        if len(event) == 1:
            await message.reply(content="今天你已经打过卡了哦")
        else :
            await message.reply(content="打卡成功,已连续打卡 " + str (event[0]) + " 天, 总共打卡 " + str (event[2]) + " 天")
        return True
    else :
        return False

@Commands("睡觉")
async def sleep(api: BotAPI, message: Message, params=None):
    event = daily.sleep(message.author.id)
    if event != None:
        if event:
            await message.reply(content="晚安~")
        else :
            await message.reply(content="你现在已经在睡梦中了哦~")
        return True
    else :
        return False

@Commands("起床")
async def weak_up(api: BotAPI, message: Message, params=None):
    event = daily.weak_up(message.author.id)
    if event != None:
        if len(event) == 3:
            await message.reply(content="早上好~,你这次睡了 " + str(event[0]) + " 小时 " + str (event[1]) + " 分钟 " + str (event[2]) + " 秒")
        else :
            await message.reply(content="你还没有开始睡觉哦~")
        return True
    else :
        return False

@Commands("词云")
async def word_cloud(api: BotAPI, message: Message, params=None):
    if params[:2] != "过滤":
        event = chat.word_cloud()
        if event != None:
            txt = "聊天中出现次数排名前 "  + str (len (event))+ " 的词是:\n"
            for word in event:
                txt += word[0] + "<" + str (word[1]) + ">\n"
            await message.reply(content=txt)
            return True
        else :
            return False
    else :
        wordList = params[2:].split (' ')
        with open("resource/filterwords.json", 'r', encoding='utf-8') as t:
            filter = json.load(t)
        for word in wordList:
            filter[word] = 1
        with open("resource/filterwords.json", 'w', encoding='utf-8') as t:
            json.dump(filter, t)
        await message.reply(content="添加成功")

@Commands("查看毛玉玉")
async def catfishshInfo(api: BotAPI, message: Message, params=None):
    event = CatFishsh.info(message.author.id)
    if event != None:
        await message.reply(content=event)
        return True
    else :
        return False
@Commands("种植毛玉玉")
async def catfishfishPlant(api: BotAPI, message: Message, params=None):
    if params.isdigit():
        event = CatFishsh.plant(message.author.id,int(params))
        if event != None:
            await message.reply(content=event)
            return True
        else :
            return False
    else:
        await message.reply(content="参数错误")
        return False
    
@Commands("收获毛玉玉")
async def catfishfishHarvest(api: BotAPI, message: Message, params=None):
    event = CatFishsh.harvest(message.author.id)
    if event != None:
        await message.reply(content=event)
        return True
    else :
        return False

@Commands("升级毛玉玉")
async def catfishfishLevelUP(api: BotAPI, message: Message, params=None):
    event = CatFishsh.levelUP(message.author.id)
    if event != None:
        await message.reply(content=event)
        return True
    else :
        return False
    
touhou_question_channel = {}

@Commands("知识问答")
async def touhou_question(api: BotAPI, message: Message, params=None):
    global touhou_question_channel
    if touhou_question_channel.get(message.channel_id) == None:
        touhou_question_channel[message.channel_id] = -1
    if touhou_question_channel[message.channel_id] == -1:
        questionIndex = touhouquestion.query (params)
        if questionIndex == "-1":
            await message.reply(content="未知的问题难度或问题类型")
            return True
        touhou_question_channel[message.channel_id] = int(questionIndex)
        with open("resource/touhouquestion.json", 'r', encoding='utf-8') as t:
            question = json.load(t)
        str = "提问: " +  question[questionIndex]["question"] + "\n"
    
        ch = 'A'
        for options in question[questionIndex]["options"]:
            str += ch + ". " + options + "\n"
            ch = chr(ord(ch) + 1)
        str += "难度: " + question[questionIndex]["difficulty"] + "\n"
        str += "类型: " + question[questionIndex]["class"]
        await message.reply(content=str)
    else :
        await message.reply(content="游戏正在进行中哦~")
        return True

@Commands("选")
async def touhou_answer(api: BotAPI, message: Message, params=None):
    global touhou_question_channel
    if touhou_question_channel.get(message.channel_id) == None:
        touhou_question_channel[message.channel_id] = -1
    if touhou_question_channel[message.channel_id] == -1:
        await message.reply(content="这里没有要回答的问题哦~")
        return True
    else :
        
        questionIndex = str(touhou_question_channel[message.channel_id])
        if len (params) != 1:
            return True
        if ord(params[0]) < ord('A') or ord(params[0]) > ord('Z'):
            return True
        else :
            with open("resource/touhouquestion.json", 'r', encoding='utf-8') as t:
                question = json.load(t)
            if ord(params[0]) - ord ('A') + 1 > len(question[questionIndex]["options"]) :
                return True
            if ord(params[0]) - ord ('A') == question[questionIndex]["answer"] :
                await message.reply(content="<@!" + str (message.author.id) + "> " + " 回答正确\n" + question[questionIndex]["description"])
            else :
                await message.reply(content="<@!" + str (message.author.id) + "> " + " 回答错误\n" + question[questionIndex]["description"])
            touhou_question_channel[message.channel_id] = -1
            return True

class MyClient(botpy.Client):
    async def on_ready(self):
        # 准备好了就会调用
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    # 监听at事件
    async def on_at_message_create(self, message: Message):
        if message.content == None:
            message.content = ""
        _log.info("[" + message.channel_id + "] " + message.author.username + " > " + message.content)
        if "sleep" in message.content:
            await asyncio.sleep(10)
        handlers = [
            sign_in,
            sleep,
            weak_up,
            word_cloud,
            touhou_question,
            touhou_answer,
            catfishshInfo,
            catfishfishPlant,
            catfishfishHarvest,
            catfishfishLevelUP,
        ]
        for handler in handlers:
            if await handler(api=self.api, message=message):
                return
        # if message.content.find ("毛玉") != -1:
        #     await message.reply(content="(>ω<)~")
        
        ThisMessage = [message.content]
        Image = []
        for file in message.attachments:
            if file.content_type[:5] == "image":
                Image.append (file.url)
        ThisMessage.append (Image)
                
        event = chat.reply (ThisMessage,test_config["reply_acceptance_threshold"]//2,min((test_config["reply_acceptance_probability"] * 3) // 2,100))
        
        if message.content[0] != '/' and event != None:
            if event[0] != '':
                await message.reply(content=event[0])
            for Image in event[1]:
                await message.reply(image=Image)

    # 监听普通消息事件
    async def on_message_create(self, message: Message):
        global LastMessage

        if message.content == None:
            message.content = ""

        _log.info(message.author.username + " > " + message.content)
        
        # if "sleep" in message.content:
        #     await asyncio.sleep(10)
            
        if not ("<@!2269423776287172301>" in message.content):
            ThisMessage = [message.content]
            Image = []
            for file in message.attachments:
                if file.content_type[:5] == "image":
                    Image.append (file.url)
            ThisMessage.append (Image)
            # 有 reply_triggering_probability% 概率触发复读
            
            if random.randint(1,100) <= test_config["reply_triggering_probability"]:
                event = chat.reply (ThisMessage,test_config["reply_acceptance_threshold"],test_config["reply_acceptance_probability"])
                if event != None:
                    if event[0] != '':
                        await message.reply(content=event[0])
                    for Image in event[1]:
                        print (Image)
                        await message.reply(image="gchat.qpic.cn/qmeetpic/667997494006418337/634999476-2817895720-DF87BDE3395D0DD6A128918F13891355/0")
            
            # 存储复读消息
            
            if LastMessage != None:
                with open("resource/reply.json", 'r', encoding='utf-8') as t:
                    reply = json.load(t)
                if reply.get (LastMessage[0]) == None:
                    reply[LastMessage[0]] = {}
                if len(LastMessage[1]) > 0:
                    if reply[LastMessage[0]].get(LastMessage[1][0]) == None:
                        reply[LastMessage[0]][LastMessage[1][0]] = []
                    reply[LastMessage[0]][LastMessage[1][0]].append (ThisMessage)
                else :
                    if reply[LastMessage[0]].get("NoImage") == None:
                        reply[LastMessage[0]]["NoImage"] = []
                    reply[LastMessage[0]]["NoImage"].append (ThisMessage)
                with open("resource/reply.json", 'w', encoding='utf-8') as t:
                    json.dump(reply, t)
            LastMessage = ThisMessage
        
    async def test (self) :
        await self.api.post_message(channel_id="634999476", content="测试")

if __name__ == "__main__":
    
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True
    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents.none()
    intents.public_guild_messages=True
    intents.guild_messages=True
    client = MyClient(intents=intents)
    # timer.start()
    client.run(appid=test_config["appid"], secret=test_config["secret"])