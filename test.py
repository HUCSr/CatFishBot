# 第一版
#-*-coding:utf-8-*-
import os
import re
import time
import requests
import bs4
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.pyplot as plt

# 手动写入目标套图的首页地址
download_url = "https://gchat.qpic.cn/qmeetpic/667997494006418337/634999476-2305602614-799B7A0C525C4B877EF4A959F3A7AD97/0"
Photor = requests.get(url=download_url, timeout=20)
Photor.raise_for_status()
PhotoPath = "Temp.jpg"
Photor.raise_for_status()
with open(PhotoPath,'wb') as f:
    f.write(Photor.content)
    f.close()
    print("保存成功")