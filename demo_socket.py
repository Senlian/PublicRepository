# coding:utf-8
# !usr/bin/env python
import socket


class socketServer(object):
    def __init__(self):
        # AF_INET,internet进程间通信
        # AF_UNIX，本机进程间通信
        # SOCKET_STREAM（流式套接字，主要用于 TCP 协议）
        # SOCKET_DGRAM（数据报套接字，主要用于 UDP 协议
        self.skt_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print socket.gethostbyname(socket.gethostname())
        self.skt_obj.bind((socket.gethostbyname(socket.gethostname()), 9001,))
        self.skt_obj.listen(10)
        # self.skt_obj.connect((socket.gethostbyname(socket.gethostname()), 9001,))
        conn,addr = self.skt_obj.accept()
        data = conn.recv(1024)
        conn.sendall(data)
        conn.close()
        self.skt_obj.close()
    pass


if __name__ == '__main__':
    obj = socketServer()
    pass
