import os
import json
import datetime
import jieba
import random
import math

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
        if len (wordCloud) >= 20:
            break
        if filter.get (word) == None:
            wordCloud.append ([word,sorted_wordCloud[word]])
    return wordCloud


def match (message,matching_message) :
    message = list (jieba.cut(message))
    matching_message = list (jieba.cut(matching_message))
    words_list_A = dict.fromkeys(message + matching_message,0)
    words_list_B = dict.fromkeys(message + matching_message,0)
    for words in message:
        words_list_A[words] += 1
    for words in matching_message:
        words_list_B[words] += 1
    cos_numerator = 0
    cos_denominator_A = 0
    cos_denominator_B = 0
    for words in dict.fromkeys(message + matching_message,0):
        cos_numerator += words_list_A[words] * words_list_B[words]
        cos_denominator_A += words_list_A[words] * words_list_A[words]
        cos_denominator_B += words_list_B[words] * words_list_B[words]
    if cos_denominator_A == 0 or cos_denominator_B == 0:
        return 0
    return round (cos_numerator * 100 / (math.sqrt(cos_denominator_A) * math.sqrt(cos_denominator_B)))


def reply (message,reply_acceptance_threshold,reply_acceptance_probability) :
    print ("检测复读中...")
    with open("resource/reply.json", 'r', encoding='utf-8') as t:
        reply = json.load(t)
    for msg in reply:
        if match (msg,message[0]) >= reply_acceptance_threshold:
            if len(message[1]) > 0:
                Image = message[1][0]
            else :
                Image = "NoImage"
            for image in reply[msg]:
                if match (image,Image) >= reply_acceptance_threshold:
                    if random.randint(1, 100) <= reply_acceptance_probability:
                        index = random.randint (0,len(reply[msg][image]) - 1)
                        return reply[msg][image][index]
    return None
