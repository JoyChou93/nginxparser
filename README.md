# nginxparser

code

``` 
from nginx import NGINX

nginx = NGINX('/usr/local/etc/nginx/nginx.conf')
print(nginx.locations)
```

nginx.conf
``` 
#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;

    server {
        listen       80;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;
        root   /usr/local/var/www/;

        location / {
            index  index.html index.php;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }


        if (!-e $request_filename) {
            rewrite ^(.*)$ /index.php$1 last;
        }

        location ~ [^/]\.php(/|$) {
            fastcgi_pass 127.0.0.1:9000;
            fastcgi_split_path_info ^(.+?.php)(/.*)$; 
            fastcgi_index index.php;
           include        fastcgi_params;
           fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
       }
        
    }

    server {
        listen       81;
        server_name  test.baidu.com;
    }


    include servers/*;
}

```

return

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