from nginx import NGINX

nginx = NGINX('/usr/local/etc/nginx/nginx.conf')
print nginx.locations