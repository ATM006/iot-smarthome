#! /usr/lib/python

from flask import Flask
from flask import request,jsonify
from flask_pymongo import PyMongo
import json

import leds
import sites
import users
import tenants
import events
import devices



app = Flask(__name__) 
app.config['MONGO1_HOST']='127.0.0.1'
app.config['MONGO1_PORT']=27017
app.config['MONGO1_DBNAME']='iot'
mongo = PyMongo(app,config_prefix='MONGO1') 
 
 
@app.route('/') 
def index(): 
	return 'The IoT SPI'


@app.route('/iot/spi/<string:cate>',methods=['GET','POST','PATCH','PUT','DELET'])
def api_cate(cate):
	if request.method == 'GET':
		if cate == 'led':
			res = leds.led_get_all(mongo)

		elif cate == 'sites':
			res = sites.site_get_all(mongo)

		elif cate == 'users':
			res = users.user_get_all(mongo)

		elif cate == 'tenants':
			res = tenants.tenant_get_all(mongo)

		elif cate == 'devices':
			typetoken = request.args.get('type')
			if typetoken == 'all':
				res = devices.device_get_all(mongo)
			else:
				res = devices.device_get_by_sitetoken(mongo, typetoken)

		else:
			res = jsonify({'result':None,'code':403})
		return res
    

	elif request.method == 'POST':
		data = json.loads(request.get_data().decode('utf-8'))
		if cate == 'led':
			res = leds.led_post(mongo,data)

		elif cate == 'sites':
			res = sites.site_post(mongo,data)

		elif cate == 'users':
			res = users.user_post(mongo,data)

		elif cate == 'tenants':
			res = tenants.tenant_post(mongo,data)

		elif cate == 'devices':
			res = devices.device_post(mongo,data)
		else:
			res = jsonify({'result':None,'code':403})

		return res

	elif request.method == 'PATCH':

		return "PATCH\n"

	elif request.method == 'PUT':
		data = json.loads(request.get_data().decode('utf-8'))
		if cate == 'led':
			res = leds.led_put(mongo,data)

		elif cate == 'sites':
			res = sites.site_put(mongo,data)

		elif cate == 'users':
			res = users.user_put(mongo,data)

		elif cate == 'tenants':
			res = tenants.tenant_put(mongo,data)

		elif cate == 'devices':
			res = devices.device_put(mongo,data)
		else:
			res = jsonify({'result':None,'code':403})

		return res
		
	elif request.method == 'DELET':

		return "DELETE\n"
	

@app.route('/iot/spi/<string:cate>/<string:cateid>',methods=['GET','DELETE'])
def api_cate_id(cate,cateid):
	if request.method == 'GET':
		if cate == 'led':
			res = leds.led_get(mongo)

		elif cate == 'sites':
			res = sites.site_get(mongo,cateid)

		elif cate == 'users':
			res = users.user_get(mongo,cateid)

		elif cate == 'tenants':
			res = tenants.tenant_get(mongo,cateid)

		elif cate == 'devices':
			res = devices.device_get(mongo,cateid)
		else:
			res = jsonify({'result':None,'code':403})

		return res
		
	elif request.method == 'DELETE':
		if cate == 'sites':
			res = sites.site_del(mongo,cateid)

		elif cate == 'users':
			res = users.user_del(mongo,cateid)

		elif cate == 'tenants':
			res = tenants.tenant_del(mongo,cateid)

		elif cate == 'devices':
			res = devices.device_del(mongo,cateid)
		else:
			res = jsonify({'result': None, 'code': 403})

		return res


@app.route('/iot/spi/devices/<string:hardwareId>/events/<string:etype>',methods=['POST','GET'])
def api_events(hardwareId,etype):
	if request.method == 'POST':
		data = json.loads(request.get_data().decode('utf-8'))
		#MongoDB
		res = events.event_post(mongo,data,hardwareId,etype)

	elif request.method == 'GET':
		#MongoDB
		res = events.event_get(mongo,hardwareId,etype)
	else:
		res = jsonify({'result': None, 'code': 403})

	return res


if __name__ == '__main__':
	from werkzeug.contrib.fixers import ProxyFix
	app.wsgi_app = ProxyFix(app.wsgi_app)
	app.run()

