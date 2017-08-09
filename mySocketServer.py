# coding:utf-8
# !usr/bin/python
import socket


class SocketServer(object):
    '''
    # AF_INET,internet进程间通信
    # AF_UNIX，本机进程间通信
    # SOCKET_STREAM,流式套接字，主要用于 TCP 协议
    # SOCKET_DGRAM,数据报套接字，主要用于 UDP 协议
    '''

    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 10021
        self.addr = (self.host, self.port)
        self.socket_obj = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        pass

    def socket_server(self):
        self.socket_obj.bind(self.addr)
        self.socket_obj.listen(10)
        conn, addr = self.socket_obj.accept()
        print addr
        print conn.getpeername()
        print self.socket_obj.getsockname()

        while True:
            conn.sendall(conn.recv(1024))
            # print conn.recv(1024)

        pass

    pass


if __name__ == '__main__':
    server_obj = SocketServer()
    server_obj.socket_server()
    pass
