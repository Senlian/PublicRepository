# coding:utf-8
# !usr/bin/python
import socket
import SocketServer

class SocketServerThreading(SocketServer.BaseRequestHandler):
    '''
    # AF_INET,internet进程间通信
    # AF_UNIX，本机进程间通信
    # SOCKET_STREAM,流式套接字，主要用于 TCP 协议
    # SOCKET_DGRAM,数据报套接字，主要用于 UDP 协议
    '''

    # def __init__(self):
    #     self.host = socket.gethostbyname(socket.gethostname())
    #     self.port = 10021
    #     self.addr = (self.host, self.port)
    #     pass
    def setup(self):
        pass

    def handle(self):
        # self.conn = self.request
        self.request.sendall("hello client,I'm  Threading server!")
        flage = True
        while flage:
            data = self.request.recv(1024)
            if data == 'exit':
                flage = False
                print 'exit'
                self.request.sendall('exit server')
            else:
                print data
                self.request.sendall('recv ok!')
        pass

    def finish(self):
        pass


if __name__ == '__main__':
    host = socket.gethostbyname(socket.gethostname())
    port = 10021
    addr = (host, port)
    server_obj = SocketServer.ThreadingTCPServer(addr, SocketServerThreading)
    server_obj.serve_forever()
    pass
