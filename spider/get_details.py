# coding=gbk
#��ȡ�¹�����ʵʱ����1109
import random
import traceback
import pymysql
import requests
import json
import time

from userAgent import user_agent_list


def get_conn():
	# ��������
	conn = pymysql.connect(host="localhost",
	                       user="root",
	                       password="root",
	                       db="covid19",
	                       charset="utf8")
	# �����α�
	cursor = conn.cursor()  # ִ����Ϸ��صĽ����Ĭ����Ԫ����ʾ
	return conn, cursor


def close_conn(conn, cursor):
	cursor.close()
	conn.close()
def get_details():
	url1 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
	headers = {
		'user-agent': random.choice(user_agent_list)
	}
	r1 = requests.get(url1, headers)

	# json�ַ���ת�ֵ�
	res1 = json.loads(r1.text)
	data1 = res1["data"]
	mudanjiang = r',{"name":"ĵ����","adcode":"231000","date":"2022/11/09","today":{"confirm":0,"confirmCuts":0,"isUpdated":true,"wzz_add":"0","local_confirm_add":0},"total":'
	data1 = data1.replace(mudanjiang, r']}]}]}')
	data_all1 = json.loads(data1)
	# ������ϸ����
	details = []
	update_time = data_all1["lastUpdateTime"]
	data_country = data_all1["areaTree"]  # list 25������
	data_province = data_country[0]["children"]  # �й���ʡ
	for pro_infos in data_province:
		province = pro_infos["name"]  # ʡ��
		for city_infos in pro_infos["children"]:
			city = city_infos["name"]
			confirm = city_infos["total"]["confirm"]
			confirm_add = city_infos["today"]["confirm"]
			heal = city_infos["total"]["heal"]
			dead = city_infos["total"]["dead"]
			details.append([update_time, province, city, confirm, confirm_add, heal, dead])
	return details
# ����ʵʱ����������Ϣdetails
def update_details():
	cursor = None
	conn = None
	try:
		li = get_details() # 1�ǵ�����ϸ����
		conn, cursor = get_conn()
		sql = "insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)"
		sql_query = "select %s=(select update_time from details order by id desc limit 1)"  # �Աȵ�ǰ���ʱ���
		# �Աȵ�ǰ���ʱ���
		cursor.execute(sql_query, li[0][0])
		if not cursor.fetchone()[0]:
			print(f"{time.asctime()}��ʼ��������")
			for item in li:
				cursor.execute(sql, item)
			conn.commit()
			print(f"{time.asctime()}���µ���������")
		else:
			print(f"{time.asctime()}�����������ݣ�")
	except:
		traceback.print_exc()
	finally:
		cursor.close()
		conn.close()
if __name__ =="__main__":
	update_details()