# coding: utf-8
# date:   2018.02.28
# author: JoyChou
# desc:   用python解析nginx.conf配置，得到server块及server块的后端IP
# python: 2.7/3.x

import re
import os


class NGINX:

    def __init__(self, conf_path):
        self.conf_path = conf_path
        self.backend = list()  # 保存后端ip和pool name
        self.serverBlock = list()  # 保存解析后端每个server块
        self.servers = list()
        self.tmp_conf = '/tmp/tmp_nginx.conf'
        self.all_conf = '/tmp/nginx.conf'
        self.merge_conf()
        self.parse_backend_ip()
        self.parse_server_block()

    # 将所有include的配置，合并到一个配置文件里
    def merge_conf(self):
        # 切换到self.conf.path的当前目录
        conf_dir = os.path.dirname(self.conf_path)

        # 判断是否是nginx.py的当前目录
        if len(conf_dir) != 0:
            os.chdir(conf_dir)

        include_regex = '^[^#]nclude\s*([^;]*);'

        # 现将include的文件的内容整合一个文件，并且去掉注释行
        fm = open(self.tmp_conf, 'w+')
        with open(self.conf_path, 'r') as f:
            for line in f.readlines():
                r = re.findall(include_regex, line)
                # 如果存在include行
                if len(r) > 0:
                    include_path = r[0]
                    if os.path.exists(include_path):
                        with open(include_path, 'r') as ff:
                            include_con = ff.read()
                            fm.write(include_con)
                else:
                    fm.write(line)
        fm.close()

        fm = open(self.tmp_conf, 'r')
        # 去掉注释行
        with open(self.all_conf, 'w+') as fp:
            for xx in fm.readlines():
                # 判断是否是注释标识符#开头
                if len(re.findall('^\s*#', xx)) == 0:
                    fp.write(xx)
        fm.close()

        # 删除临时配置文件
        if os.path.exists(self.tmp_conf):
            os.remove(self.tmp_conf)

    def parse_backend_ip(self):
        # 获取后端的poolname和对应的ip，放在一个dict的list里
        with open(self.all_conf, 'r') as fp:
            alllines = fp.read()

            # 获取每个upstream块
            regex_1 = 'upstream\s+([^{ ]+)\s*{([^}]*)}'
            upstreams = re.findall(regex_1, alllines)

            for up in upstreams:
                # 获取后端的ip
                regex_2 = 'server\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d{2,5})?)'
                backend = re.findall(regex_2, up[1])
                # 判断是否有后端的ip设置
                if len(backend) > 0:
                    pool_and_ip = {'poolname': up[0], 'ip': ' '.join(backend)}
                    self.backend.append(pool_and_ip)

    def parse_server_block(self):
        flag = False
        serverblock = ''
        num_of_quote = 0

        with open(self.all_conf, 'r') as fp:
            for line in fp.readlines():
                x = line.replace(' ', '')
                if x.startswith('server{'):
                    num_of_quote += 1
                    flag = True
                    serverblock += line
                    continue
                # 发现{，计数加1。发现}，计数减1，直到计数为0
                if flag and '{' in line:
                    num_of_quote += 1

                # 将proxy_pass的别名换成ip
                if flag and 'proxy_pass' in line:
                    r = re.findall('proxy_pass\s+https?://([^;/]*)[^;]*;', line)
                    if len(r) > 0:
                        for pool in self.backend:
                            if r[0] == pool['poolname']:
                                line = line.replace(r[0], pool['ip'])

                if flag and num_of_quote != 0:
                    serverblock += line

                if flag and '}' in line:
                    num_of_quote -= 1

                if flag and num_of_quote == 0:
                    self.serverBlock.append(serverblock)
                    flag = False
                    serverblock = ''
                    num_of_quote = 0

        for singleServer in self.serverBlock:
            port = re.findall('listen\s*((?:\d|\s)*)[^;]*;', singleServer)[0]  # port只有一个

            r = re.findall('server_name\s+([^;]*);', singleServer)  # server_name只有一个

            # 可能存在没有server_name的情况
            if len(r) > 0:
                servername = r[0]
            else:
                continue

            # 判断servername是否有ip，有ip就不存。比如servername 127.0.0.1这样的配置
            if len(re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', servername)) > 0:
                continue

            include = ' ' .join(re.findall('include\s+([^;]*);', singleServer))  # include不止一个
            # location可能不止一个
            locations = re.findall('location\s*[\^~\*=]{0,3}\s*([^{ ]*)\s*\{[^}]*proxy_pass\s+https?://([^;/]*)[^;]*;',
                                   singleServer)

            backend_list = list()
            backend_ip = ''

            # 可能存在多个location
            if len(locations) > 0:
                for location in locations:
                    backend_path = location[0]
                    poolname = location[1]
                    # 如果不是ip的pool name，就取出后端对应的ip
                    if len(re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', poolname)) == 0:
                        for backend in self.backend:
                            if poolname == backend['poolname']:
                                backend_ip = backend['ip']
                                break
                    else:
                        backend_ip = poolname

                    backend_list.append({"backend_path": backend_path, "backend_ip": backend_ip})

            server = {
                        'port': port,
                        'server_name': servername,
                        'include': include,
                        'backend': backend_list
                     }

            self.servers.append(server)


