# nginxparser

``` 
from nginx import NGINX

nginx = NGINX('/usr/local/etc/nginx/nginx.conf')
print(nginx.locations)
```

返回

``` 
[{
	'backend': [],
	'include': 'fastcgi_params',
	'server_name': 'localhost',
	'port': '80'
}, {
	'backend': [],
	'include': '',
	'server_name': 'test.baidu.com',
	'port': '81'
}]
```