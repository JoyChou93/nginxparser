# nginxparser

## 功能

用python解析nginx配置，获取server块以及server块每个location的后端ip。

## 安装

`wget https://raw.githubusercontent.com/JoyChou93/nginxparser/master/nginx.py`

## 使用

调用代码

``` 
from nginx import NGINX

nginx = NGINX('nginx.conf')
print(nginx.servers)
```


结果

``` 
[{
	'include': 'fastcgi_params',
	'backend': [],
	'port': '80',
	'server_name': 'localhost'
}, {
	'include': '',
	'backend': [{
		'backend_path': '/test',
		'backend_ip': '10.10.10.10:8080 10.10.10.11:8080'
	}],
	'port': '81',
	'server_name': 'test.baidu.com'
}]
```