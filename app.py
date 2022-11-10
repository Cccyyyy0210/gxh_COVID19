from flask import Flask
from flask import render_template
from flask import jsonify
from jieba.analyse import extract_tags
import string

import spider.utils
from spider import utils

app = Flask(__name__)


# ��ҳ
@app.route('/')
def index():
	return render_template('main.html')


# �������ݿ��ӻ�����
@app.route('/main')
def main():
	return render_template('main.html')


# �ۼ��������� �ۼ�ȷ�� �ۼ����� �ۼ����� �ۼ�����
@app.route('/c1')
def get_c1_data():
	data = spider.utils.get_c1_data()
	return jsonify({"confirm": data[0],"suspect":data[1],"heal": data[2], "dead": data[3]})


# ���ظ�ʡ����
@app.route('/c2')
def get_c2_data():
	#data = spider.utils.get_c2_data()
	res = []
	for tup in spider.utils.get_c2_data():
		res.append({"name": tup[0], "value": int(tup[1])})
	return jsonify({"data": res})


# �ۼ�����
@app.route("/l1")
def get_l1_data():
	data = spider.utils.get_l1_data()
	day, confirm, confirm_add, heal, dead = [], [], [], [], []
	for a, b, c, d, e in data:  # �ܶ�����ί��վǰ7�춼��û�����ݵģ����԰�ǰ7�쿳����
		day.append(a.strftime("%m-%d"))  # a��datatime����
		confirm.append(b)
		confirm_add.append(c)
		heal.append(d)
		dead.append(e)
	return jsonify({"day": day, "confirm": confirm, "confirm_add": confirm_add, "heal": heal, "dead": dead})


# ����ȷ�Ｐ ��֢״
@app.route("/l2")
def get_l2_data():
	data = spider.utils.get_l2_data()
	day, nowConfirm, noInfectH5 = [], [], []
	for a, b, c in data:
		day.append(a.strftime("%m-%d"))  # a��datatime����
		nowConfirm.append(b)
		noInfectH5.append(c)
	return jsonify({"day": day, "nowConfirm": nowConfirm, "noInfectH5": noInfectH5})


# ����ȷ����е���top5
@app.route("/r1")
def get_r1_data():
	data = spider.utils.get_r1_data()
	city = []
	confirm = []
	for k, v in data:
		city.append(k)
		confirm.append(int(v))
	return jsonify({"city": city, "confirm": confirm})


# ����ͼ
@app.route("/r2")
def get_r2_data():
	data = spider.utils.get_r2_data()
	d = []
	for i in data:
		k = i[0].rstrip(string.digits)  # �Ƴ���������
		v = i[0][len(k):]  # ��ȡ��������
		ks = extract_tags(k)  # ʹ��jieba ��ȡ�ؼ���
		for j in ks:
			if not j.isdigit():
				d.append({"name": j, "value": v})
	return jsonify({"kws": d})


# ʱ��
@app.route('/time')
def gettime():
	return spider.utils.get_time()


# ajax
@app.route('/ajax', methods=["get", "post"])
def ajax():
	return '10000'


if __name__ == '__main__':
	app.run()
