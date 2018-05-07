#!/usr/bin/python3.5

from flask import Flask
from flask import request,jsonify
from flask_pymongo import PyMongo
import json,uuid,datetime

exp = '{\
"createdDate": "",\
"createdBy": "",\
"token":"",\
"name":"",\
"description":"",\
"metadata": {}\
}'


def site_get_all(mongo):
	sites = mongo.db.sites
	s = sites.find()
	out = []
	for item in s:
		item.pop("_id")
		print(item)
		out.append(item)
	
	return jsonify({'result':out})


def site_get(mongo,token):
	sites = mongo.db.sites
	ex = json.loads(exp)
	res = sites.find_one({"token" : token})
	if res == None:
		return jsonify({'result': ex})
	else:
		res.pop("_id")
		print(res)
		return jsonify({'result':res})
	#return "site test"

def site_post(mongo,data):
	sites = mongo.db.sites
	date = datetime.datetime.now()
	ex = json.loads(exp)
	token =data["token"]
	if token == '':
		ex["createdDate"] = date.strftime("%Y-%m-%d %H:%M:%S")
		ex["createdBy"] = "admin"
		ex["token"] = str(uuid.uuid1())
		ex["name"] = data["name"]
		ex["description"] = data["description"]
		ex["metadata"] = data["metadata"]
	else:
		#return '{"site":"exist"}'
		return jsonify({'result':ex})
	print(ex)
	sites.insert(ex)
	ex.pop("_id")
	return jsonify({'result':ex})

#更新站点操作
def site_put(mongo,data):
	sites = mongo.db.sites
	ex = json.loads(exp)
	date = datetime.datetime.now()
	#ex = json.loads(exp)
	token = data["token"]
	res = sites.find_one({"token" : token})
	if res != None:
		sites.remove({"token" : token})
		res["createdDate"] = date.strftime("%Y-%m-%d %H:%M:%S")
		res["createdBy"] = "admin"
		#res["token"] = str(uuid.uuid1())
		res["name"] = data["name"]
		res["description"] = data["description"]
		res["metadata"] = data["metadata"]
		print(res)
		sites.insert(res)
		res.pop("_id")
		return jsonify({'result': res})
	else:
		return jsonify({'result': ex})



def site_del(mongo,token):
	sites = mongo.db.sites
	ex = json.loads(exp)
	res = sites.find_one({"token" : token})
	if res == None:
		return jsonify({'result': ex})
	else:
		sites.remove({"token" : token})
		res.pop("_id")
		print(res)
		return jsonify({'result':res})


