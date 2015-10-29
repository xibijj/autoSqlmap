# -*- coding: utf-8 -*-
import multiprocessing
import sys,time
import requests

from lib.proxy2 import ProxyRequestHandler, ThreadingHTTPServer

import config
import myproxy
import myinjector

def banner():
	print '''
         ,8.       ,8.          8 888888888o.   `8.`8888.      ,8' 
        ,888.     ,888.         8 8888    `88.   `8.`8888.    ,8'  
       .`8888.   .`8888.        8 8888     `88    `8.`8888.  ,8'   
      ,8.`8888. ,8.`8888.       8 8888     ,88     `8.`8888.,8'    
     ,8'8.`8888,8^8.`8888.      8 8888.   ,88'      `8.`88888'     
    ,8' `8.`8888' `8.`8888.     8 888888888P'       .88.`8888.     
   ,8'   `8.`88'   `8.`8888.    8 8888`8b          .8'`8.`8888.    
  ,8'     `8.`'     `8.`8888.   8 8888 `8b.       .8'  `8.`8888.   
 ,8'       `8        `8.`8888.  8 8888   `8b.    .8'    `8.`8888.  
,8'         `         `8.`8888. 8 8888     `88. .8'      `8.`8888. 

    simple http(s) proxy with python based sqlmapapi wrapper
    Author: Mr.x (http://blog.163.com/x_rm/)
'''

def TestSqlmapAPI():
	try:
		requests.get(config.sqlmap_host, timeout=3)
		return True
	except:
		return False

def RunProxy(q):
	server_address = ('', config.proxy_port)

	HandlerClass = myproxy.myproxy
	ServerClass = ThreadingHTTPServer
	protocol="HTTP/1.1"

	HandlerClass.protocol_version = protocol
	HandlerClass.q = (q)
	httpd = ServerClass(server_address, HandlerClass)

	sa = httpd.socket.getsockname()
	print "Serving HTTP Proxy on", sa[0], "port", sa[1], "..."
	httpd.serve_forever()

if __name__ == '__main__':
	banner()
	if not TestSqlmapAPI():
		print "Please start sqlmapapi first! [%s]" %config.sqlmap_host
		sys.exit(0)
	config.queue = multiprocessing.Queue()
	q = config.queue
	#把multiprocessing.Queue()以型参方式传递给myproxy.myproxy
	p = multiprocessing.Process(target=RunProxy, args=(q,))
	p.start()

	myinjector.myinjector().run()