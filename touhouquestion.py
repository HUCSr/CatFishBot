import os
import json
import datetime
import jieba
import random

def query (Class) :
    with open("resource/touhouquestion.json", 'r', encoding='utf-8') as t:
        question = json.load(t)
    questions = []
    questionIndex = 0
    if Class == "":
        lens = len(question)
        questionIndex = str(random.randint(0 , lens - 1))
    else :
        for idx in question:
            if question[idx]["difficulty"] == Class or question[idx]["class"] == Class :
                questions.append (idx)
        lens = len(questions)
        if lens == 0:
            return -1
        questionIndex = questions[random.randint(0 , lens - 1)]
    
    return questionIndex