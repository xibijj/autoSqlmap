# -*- coding: utf-8 -*-
import requests
import json
import os

import config

class SqlmapAPIWrapper():
	def __init__(self, filename,payload):
		self.url = config.sqlmap_host
		self.taskid = None
		self.filepath = config.save_path + '/' + filename
		#self.options = {'requestFile': self.filepath}
		#传过来的payload跟配置文件的sqlmap参数组合，传给sqlmapapi
		self.options = payload
		self.options.update(config.sqlmap_options)
		self.headers = {'Content-Type': 'application/json'}

	def settaskid(self, taskid):
		#print taskid
		self.taskid = taskid

	def new(self):
		path = '/task/new'
		r = requests.get(self.url + path, headers=self.headers).json()
		if r['success']:
			self.taskid = r['taskid']
		return r['success']

	def delete(self):
		path = '/task/%s/delete' % self.taskid
		#print 'delete' + path
		r = requests.get(self.url + path, headers=self.headers).json()
		self.taskid = None
		return r['success']

	def scan_start(self):
		#调用nuw()得到一个taskid
		self.new()
		path = '/scan/%s/start' % self.taskid
		#print 'scan_start' + path
		#print (self.url + path, json.dumps(self.options), self.headers)
		r = requests.post(self.url + path, data=json.dumps(self.options), headers=self.headers).json()
		return r['success']

	def scan_stop(self):
		path = '/scan/%s/stop' % self.taskid
		#print 'scan_stop' + path
		r = requests.get(self.url + path, headers=self.headers).json()
		return r['success']

	def scan_kill(self):
		path = '/scan/%s/kill' % self.taskid
		r = requests.get(self.url + path, headers=self.headers).json()
		return r['success']

	def scan_status(self):
		path = '/scan/%s/status' % self.taskid
		#print 'scan_status' + path
		r = requests.get(self.url + path, headers=self.headers).json()
		if r['success']:
			return r['status']
		else:
			return None

	def scan_data(self):
		path = '/scan/%s/data' % self.taskid
		#print 'scan_data' + path
		r = requests.get(self.url + path, headers=self.headers).json()
		#print r
		#print r['data']
		if r['success']:
			#print "r['success']"
			return r['data']
		else:
			return None

	def terminal(self):
		return self.scan_status() == 'terminated'

	def vulnerable(self):
		#print "vulnerable()"
		#print len(self.scan_data())
		return len(self.scan_data()) > 0

	def delete_file(self):
		os.remove(self.filepath)

	def clear(self):
		self.scan_stop()
		self.delete_file()

