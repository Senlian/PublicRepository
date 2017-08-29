#!/usr/bin/env python
# -*-coding:utf-8-*-
import os
import shutil
import re
from optparse import OptionParser

import sys


class RedisDeploy():
    def __init__(self, redis_dir, start_port):
        self.redis_dir = redis_dir
        self.start_port = start_port
        self.cluster_dir = os.path.join(self.redis_dir, 'cluster')
        self.redis_rb = os.path.join(self.redis_dir, 'redis-trib.rb')
        self.redis_conf = os.path.join(self.redis_dir, 'redis.windows.conf')
        self.redis_conf_list = []
        self.redis_app = os.path.join(self.redis_dir, 'redis-server.exe')
        pass

    def modification_conf(self, str_conf, str_port):
        if os.path.isfile(str_conf):
            self.redis_conf_list.append(str_conf)
            # return
        # [ERR] Node 127.0.0.1:7000 is not configured as a cluster node.
        # 以上报错需要修改一下几项才能解决，修改完成后需要重启节点
        f = open(str_conf, 'w')
        # 修改端口号配置
        content = open(self.redis_conf, 'r').read()
        # port 7001
        content = re.sub(re.compile('port(\s+)6379'), 'port %s' % str_port, content)
        print 'Replace "port 6379" as "port %s"' % str_port
        # print content
        # cluster-enabled yes
        content = re.sub(re.compile('#\s+cluster\-enabled\s+yes'), 'cluster-enabled yes', content)
        # dbfilename dump.rdb
        content = re.sub(re.compile('\s+dbfilename\s+dump\.rdb'), ('\ndbfilename redis_%s.rdb' % (str_port)), content)
        print content
        # cluster-config-file nodes-6379.conf
        # 注意node.conf不能带路径，否则服务起不来。
        nodes_conf = ('cluster-config-file nodes_%s.conf' % (str_port))
        content = re.sub(re.compile('#\s+cluster\-config\-file\s+nodes\-\d+\.conf'), nodes_conf, content)
        # appendonly yes
        content = re.sub(re.compile('\s+appendonly\s+(yes|no)'), '\nappendonly yes', content)
        # logfile ""
        content = re.sub(re.compile('logfile[\s" ]+'), '\nlogfile "./log/redis_%s_log.log"\n' % str_port, content)
        f.write(content)

        f.close()

        self.redis_conf_list.append(str_conf)

    def deploy(self):
        os.chdir(self.redis_dir)
        self.cluster_dir = os.path.join(os.getcwd(), 'cluster')
        if not os.path.isfile(self.redis_rb):
            print 'Not found %s.' % self.redis_rb
            return
        if not os.path.exists(self.cluster_dir):
            print 'make dir %s.' % self.cluster_dir
            os.makedirs(self.cluster_dir)
        os.chdir(self.cluster_dir)
        shutil.copy(self.redis_rb, self.cluster_dir)
        print 'Copy %s to %s' % (self.redis_rb, self.cluster_dir)

        for port in range(self.start_port, self.start_port + 3):
            print 'port=', port
            str_port = str(port)
            port_dir = os.path.join(self.cluster_dir, str_port)
            port_log_dir = os.path.join(self.cluster_dir, str_port, 'log')
            if not os.path.exists(port_dir):
                print 'make dir %s.' % port_dir
                os.makedirs(port_dir)
            if not os.path.exists(port_log_dir):
                print 'make dir %s.' % port_log_dir
                os.makedirs(port_log_dir)
            shutil.copy(self.redis_app, port_dir)
            str_conf = os.path.join(port_dir, 'redis.%s.conf' % str_port)
            if os.path.isfile(self.redis_conf):
                print 'Have redis config, %s.' % self.redis_conf
                self.modification_conf(str_conf, str_port)
            else:
                print 'Not found redis config,%s.' % self.redis_conf

    def start_nodes(self):
        pwd = os.getcwd()
        os.chdir(self.redis_dir)
        for redis_conf in self.redis_conf_list:
            server_name = os.path.splitext(os.path.basename(redis_conf))[0].replace('.', '')
            os.chdir(os.path.dirname(redis_conf))
            # 以下报错表示服务已经存在
            # commond line is,redis-server.exe --service-install "C:\Program Files\Redis\cluster\7001\redis.7001.conf" --service-name redis7001
            # [2292] 22 Aug 15:32:27.245 # HandleServiceCommands: system error caught. error code=1073, message = CreateService failed: unknown error
            cmd = 'redis-server.exe --service-install "%s" --service-name %s' % (redis_conf, server_name)
            self.shell_cmd(cmd)
            print 'server_name=', server_name
            cmd = 'net start "%s"' % server_name
            self.shell_cmd(cmd)
        os.chdir(pwd)

    def start_cluster(self):
        pwd = os.getcwd()
        os.chdir(self.cluster_dir)
        # cmd = '''ruby redis-trib.rb create --replicas 1 127.0.0.1:{0} 127.0.0.1:{1} 127.0.0.1:{2} 127.0.0.1:{3} 127.0.0.1:{4} 127.0.0.1:{5}'''.format(
        #         self.start_port, self.start_port + 1, self.start_port + 2, self.start_port + 3, self.start_port + 4,
        #                          self.start_port + 5)
        cmd = '''ruby redis-trib.rb create --replicas 0 127.0.0.1:{0} 127.0.0.1:{1} 127.0.0.1:{2}'''.format(
                self.start_port, self.start_port + 1, self.start_port + 2)
        print self.shell_cmd(cmd)
        os.chdir(pwd)

    def get_redis_server(self):
        temp = os.popen("net start").read()
        server_list = re.findall(r'(redis(\d+))', temp)
        return server_list

    def shutdown_nodes(self):
        pwd = os.getcwd()
        os.chdir(self.redis_dir)
        for server_name, port in self.get_redis_server():
            redis_conf = os.path.join(self.cluster_dir, port, 'redis.%s.conf' % port)
            cmd = 'net stop "%s"' % server_name
            self.shell_cmd(cmd)
            cmd = 'redis-server.exe --service-uninstall "%s" --service-name %s' % (redis_conf, server_name)
            self.shell_cmd(cmd)
        os.chdir(pwd)

    def shutdown_cluster(self):
        os.chdir(self.redis_dir)
        cmd = 'redis-server --service-uninstall'
        self.shell_cmd(cmd)
        self.shutdown_nodes()

    def shell_cmd(self, commond):
        print "commond line is,%s" % commond
        rst = os.system(commond)
        return rst


if __name__ == '__main__':
    redis_dir = r'C:\Program Files\Redis'
    start_port = 7800
    redis = RedisDeploy(redis_dir, start_port)
    # redis.get_redis_server()
    # redis.shutdown_cluster()
    # redis.shutdown_nodes()
    redis.deploy()
    redis.start_nodes()
    # redis.start_cluster()
    # redis.shutdown_cluster()
