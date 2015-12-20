# -*- coding: utf-8 -*-
from Queue import Empty
import multiprocessing 
import time
import sys
import platform

from lib.sqlmapapiwrapper import SqlmapAPIWrapper
import config

def with_color(c, s):
	system = platform.system()
	if system == 'Windows':
		return "%s" % s
	else:
		return "\x1b[%dm%s\x1b[0m" % (c, s)
		
def writelog(log,name):
    try:
        fp = open('%s_Sqli_vlu.log'%name,'a')
        fp.write(log+"\n")
        fp.close()
    except:
        return False

class myinjector():
	def run(self):
		while True:
			try:
				(fname,taskid,payload,start_time,hostname) = config.queue.get(timeout=1)
				#print (fname,taskid,payload,start_time)
				
				injector = SqlmapAPIWrapper(fname,payload)
				injector.settaskid(taskid)
	
				#当sqlmapapi检测结束后...
				if not injector.terminal():
					if time.time()-start_time>config.sqlmap_tasktimeout:
						injector.clear()
						continue
					config.queue.put((fname,taskid,payload,start_time,hostname))
					time.sleep(5)
					continue

				if injector.vulnerable():
					print with_color(32, "#%s [VulUrl] %s"%(time.strftime("%H:%M:%S"),payload['url']))
					print with_color(32, "#%s [Exploit] sqlmap -r %s -v 3 --level 3"%(time.strftime("%H:%M:%S"), config.save_path + '/' + fname))
					vlu_str = "#%s [VulUrl] %s \n#%s [Exploit] sqlmap -r %s -v 3 --level 3"%(time.strftime("%H:%M:%S"),payload['url'],time.strftime("%H:%M:%S"), config.save_path + '/' + fname)
					writelog(vlu_str,"%s_%s"%(hostname,time.strftime("%Y-%m-%d")))
					sys.stdout.flush()
					injector.delete()
				else:
					injector.clear()
					
			except Empty:
				time.sleep(3)
				pass
			except KeyboardInterrupt:
				return
			#except:
			#	continue
