# coding:utf-8
# !usr/bin/python
import socket



class SocketClient(object):
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 10021
        self.addr = (self.host, self.port)
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pass

    def socket_client(self):
        self.socket_obj.connect(self.addr)
        while True:
            str = raw_input('input:')
            self.socket_obj.sendall(str)
            print self.socket_obj.recv(1024)
            print self.socket_obj.getpeername()
            print self.socket_obj.getsockname()
            print self.socket_obj.fileno()

        pass

    pass


if __name__ == '__main__':
    client_obj = SocketClient()
    client_obj.socket_client()
    pass
