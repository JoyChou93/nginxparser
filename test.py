from nginx import NGINX

nginx = NGINX('nginx.conf')
print(nginx.servers)