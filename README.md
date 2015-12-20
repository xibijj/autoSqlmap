#autoSqlmap

###
未解决问题：
不能自定义指定ip地址做为监听地址,算是坑吧!(求大神指点)
目前解决办法：
需要修改python目录下/lib/SocketServer.py第402行 def __init__ 
*新添加：
```
if len(server_address[0]) ==0:
   self.address_family = 2
```

###

autoSqlmap is a simple http(s) proxy with python based sqlmapapi wrapper.

When HTTP traffic goes through the proxy, it will auto launch sqlmap to test sqli vulnerability.

##Requirement
* python2
* sqlmap
* requests

##Usage
modify configurations in config.py, default config is for http://testphp.vulnweb.com/

sqlmap options please refer to `sqlmap_options_list.txt`

start sqlmap api

```
python sqlmapapi.py -s
```

start autoSqlmap

```
python run.py 2>/dev/null
```

go to http://testphp.vulnweb.com/ for test

##Enable HTTPS intercept
To intercept HTTPS connections, generate private keys and a private CA certificate:

```
./setup_https_intercept.sh
```

Through the proxy, you can access http://proxy2.test/ and install the CA certificate in the browsers.

(from proxy2)

##Contact
http://blog.163.com/x_rm/

coolxia [AT] foxmail.com

##Reference
* https://github.com/zt2/sqli-hunter
* https://github.com/manning23/MSpider
* https://github.com/inaz2/proxy2
* http://drops.wooyun.org/tips/6653
