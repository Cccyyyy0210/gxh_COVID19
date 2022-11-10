# coding=gbk
import re

import requests
import json
import time
import pymysql
from selenium.webdriver import Edge, EdgeOptions
import traceback
import sys
from userAgent import user_agent_list
import random
import utils
from bs4 import BeautifulSoup
import lxml


def test():
	url1 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
	url2 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
	headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
	}
	r1 = requests.get(url1, headers)
	r2 = requests.get(url2, headers)
	json1 = json.loads(r1.text)
	data1=json1["data"]
	mudanjiang=r',{"name":"牡丹江","adcode":"231000","date":"2022/11/09","today":{"confirm":0,"confirmCuts":0,"isUpdated":true,"wzz_add":"0","local_confirm_add":0},"total":'
	#mudanjiang = r',{\"name\":\"牡丹江\",\"adcode\":\"231000\",\"date\":\"2022/11/09\",\"today\":{\"confirm\":0,\"confirmCuts\":0,\"isUpdated\":true,\"wzz_add\":\"0\",\"local_confirm_add\":0},\"total\":"}'
	data1 = data1.replace(mudanjiang, r']}]}]}')
	#data1[129032]
	js1=json.loads(data1)
	print(js1)
	with open('data1.json','w')as f:
		json.dump(js1,f)
	print('成功')





if __name__ == "__main__":
	test()
