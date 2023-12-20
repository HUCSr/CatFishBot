# -*- coding: utf-8 -*-
import asyncio
import os
import time
import json

import botpy
from botpy import logging, BotAPI
from botpy.ext.command_util import Commands
from botpy.ext.cog_yaml import read
from botpy.message import Message

import command
from threading import Thread

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
_log = logging.get_logger()

@Commands("打卡")
async def sign_in(api: BotAPI, message: Message, params=None):
    # params 是我指令后面的东西
    event = command.sign_in(message.author.id)
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
    event = command.sleep(message.author.id)
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
    event = command.weak_up(message.author.id)
    if event != None:
        if len(event) == 3:
            await message.reply(content="早上好~,你这次睡了 " + str(event[0]) + " 小时 " + str (event[1]) + " 分钟 " + str (event[2]) + " 秒")
        else :
            await message.reply(content="你还没有开始睡觉哦~")
        return True
    else :
        return False

LastMessage = None

class MyClient(botpy.Client):
    async def on_ready(self):
        # 准备好了就会调用
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    # 监听at事件
    async def on_at_message_create(self, message: Message):
        _log.info("[" + message.channel_id + "] " + message.author.username + " > " + message.content)
        if "sleep" in message.content:
            await asyncio.sleep(10)
        handlers = [
            sign_in,
            sleep,
            weak_up,
        ]
        for handler in handlers:
            if await handler(api=self.api, message=message):
                return
        if message.content.find ("毛玉") != -1:
            await message.reply(content="(>ω<)~")

    # 监听普通消息事件
    async def on_message_create(self, message: Message):
        global LastMessage
        _log.info(message.author.username + " > " + message.content)
        if "sleep" in message.content:
            await asyncio.sleep(10)
        ThisMessage = [message.content]
        Image = []
        for file in message.attachments:
            if file.content_type[:5] == "image":
                Image.append (file.url)
        ThisMessage.append (Image)
        if LastMessage != None:
            with open("recource/reply.json", 'r', encoding='utf-8') as t:
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
            with open("recource/reply.json", 'w', encoding='utf-8') as t:
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