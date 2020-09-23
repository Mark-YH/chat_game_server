# coding: UTF-8
"""
Created on 2020/9/20

@author: Mark Hsu
"""
import socket
from _thread import *


class Client:
    host = ''
    port = -1
    name = ''
    s = None

    def __init__(self, _host='127.0.0.1', _port=8001, _name="NO NAME"):
        self.host = _host
        self.port = _port
        self.name = _name
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.host, self.port))

            self.s.sendall(str.encode(str(_name)))
            print(bytes.decode(self.s.recv(1024)))
            start_new_thread(self.keep_receiving, ())
        except Exception as e:
            print('Connection error: ' + str(e))
            self.close()

    def send(self, msg):
        if self.s is not None:
            try:
                self.s.sendall(msg)
            except Exception as e:
                print('Sending message error: ' + str(e))
                self.close()
        else:
            print('Null instance error')

    def keep_receiving(self):
        while self.is_valid():
            try:
                reply = self.s.recv(1024)
                if reply:
                    print('\r' + bytes.decode(reply))
            except Exception as e:
                print(e)
                self.close()
                break

    def is_valid(self):
        return self.s is not None

    def close(self):
        if self.s is not None:
            self.s.close()
            self.s = None
        else:
            print('Socket instance is null')

    def __del__(self):
        if self.s is not None:
            self.close()


if __name__ == '__main__':
    name = input("Enter your name: ")
    client = Client('127.0.0.1', 8001, name)

    while client.is_valid():
        msg = input('\r')
        if msg == 'exit':
            break
        elif msg == '':
            pass
        else:
            client.send(str.encode(msg))

    client.close()
