# 复读模块,用于查询和匹配复读
import json
import random
import jieba
import math

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

# print (match ("这只皮靴号码大了。那只号码合适","这只皮靴号码不小，那只更合适"))

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
