import re
import requests
import json
import time
import pymysql
from selenium import webdriver
from selenium.webdriver import Edge, EdgeOptions
import traceback
import sys
from selenium.webdriver.common.by import By
import random
from bs4 import BeautifulSoup
import logging
import pymysql
# 日志等级:普通信息,日志事件发生时间及文本内容
from spider.userAgent import user_agent_list

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


class Province:
	def __init__(self):
		self.session = requests.session()
		self.crawl_timestamp = int()

	def fetch_crawler(self):  # 爬取省市信息
		while True:
			self.session.headers.update(
				{
					'user-agent': random.choice(user_agent_list)
				}
			)
			self.crawl_timestamp = int(time.time() * 1000)
			try:
				r = self.session.get(url='https://ncov.dxy.cn/ncovh5/view/pneumonia')
			except requests.exceptions.ChunkedEncodingError:
				continue
			soup = BeautifulSoup(r.content, 'lxml')
			fetch_information = re.search(r'\[(.*)\]', str(soup.find('script', attrs={'id': 'getAreaStat'})))
			if fetch_information:
				self.fetch_parser(fetch_information=fetch_information)
			if not fetch_information:
				time.sleep(3)
				continue
			break
		logger.info('province_information successfully crawled.')

	def fetch_parser(self, fetch_information):
		#字典
		provinces = json.loads(fetch_information.group(0))
		for province in provinces:
			try:
				province.pop('provinceShortName')
				province.pop('comment')
				province.pop('locationId')
				province.pop('statisticsData')
				province.pop('cities')
				province.pop('dangerAreas')
			except KeyError:
				pass
			print(province)
	def fetch_run(self):
		while True:
			self.fetch_crawler()
			time.sleep(60)

if __name__ =="__main__":
	province = Province()
	province.fetch_run()