# -*- coding: utf-8 -*-
import re
import urlparse
import uuid
import sys
import md5
import os.path
import time

from lib.sqlmapapiwrapper import SqlmapAPIWrapper
from lib.proxy2 import ProxyRequestHandler, ThreadingHTTPServer
import config

class myproxy(ProxyRequestHandler):

	query_log = {}

	def check_history(self, key):
		try:
			self.query_log[key]
			return True
		except KeyError:
			return False
			
	def q(self, q):
		self.q = q

	def make_sig(self, url):
		'''
		hostname+path+querykey
		'''
		parse = urlparse.urlparse(url)
		return md5.md5(parse.hostname+parse.path+''.join(sorted(urlparse.parse_qs(parse.query).keys()))).hexdigest()

	def save_handler(self, req, req_body, res, res_body):
		#check res.status
		if re.match(config.filter_code, str(res.status)): return
		#check host
		if not len([h for h in config.included_host if req.headers.get('Host', '').endswith(h)]): return
		if len([h for h in config.excluded_host if req.headers.get('Host', '').endswith(h)]): return
		#check fileext
		if len([h for h in config.filter_file if urlparse.urlparse(req.path).path.endswith(h)]): return
		#check query, get must have query string or url-rewrited
		#GET method, have ext and  do not have query string
		if os.path.splitext(req.path)[1] and req.command == 'GET' and not urlparse.urlparse(req.path).query: return

		#prepare request
		req_header_text = "%s %s %s\n%s" % (req.command, req.path, req.request_version, req.headers)

		if req.command == 'GET':
			request = req_header_text + '\n'
			keystr = req.path
		else:
		#POST
			if req_body:
				request = req_header_text + '\n' + str(req_body)
				a = str(req_body)
				#分割post data参数
				b = a.split('&')
				c = []
				for i in b:
					if i.find('=') > 0:
						arr = i.split('=')
						c.append(arr[0])
						keystr = "%s/%s"%(req.path,''.join(sorted(c)))
						
		#修改某些Post请求为空时出错
		#else:
			request = req_header_text + '\n' + str(req_body)
			keystr = req.path
		
		#post请求时把postdata放入检测
		#print req_body

		#avoid same params multi test
		sig = self.make_sig(keystr)
		if self.check_history(sig):
			return

		self.query_log[sig] = True

		fname = str(uuid.uuid4())

		f = open(config.save_path + '/' + fname, 'w')
		f.write(request)
		f.close()
		
		#sqlmap参数请修改config.py的sqlmap_options
		if req_body:
			payload = {'url':req.path, 'data':req_body, 'cookie':req.headers.get('Cookie'), 'agent':req.headers.get('User-Agent')}
		else:
			payload = {'url':req.path, 'cookie':req.headers.get('Cookie'), 'agent':req.headers.get('User-Agent')}
		
		#通过类传参，把payload传入检测队列
		i = SqlmapAPIWrapper(fname,payload)
		if i.scan_start():
			self.q.put((fname,i.taskid,payload,time.time()))
