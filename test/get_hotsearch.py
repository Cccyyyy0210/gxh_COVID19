# encoding=utf8
import requests
import json
import time
import pymysql
from selenium import webdriver
from selenium.webdriver import Edge, EdgeOptions
import traceback
import sys

from selenium.webdriver.common.by import By

from userAgent import user_agent_list
import random
from bs4 import BeautifulSoup

def get_hotsearch():
	url1 = "http://www.nhc.gov.cn/xcs/yhfc/list_gzbd.shtml"
	headers = {
		'user-agent': random.choice(user_agent_list)
	}
	browser=webdriver.Edge()
	browser.get(url1)
	html=browser.find_element(By.CLASS_NAME,"zxxx_list").text.encode("utf-8").decode("utf-8")
	print(html)
	browser.close()
if __name__ =="__main__":
	get_hotsearch()
