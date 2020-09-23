# coding: UTF-8
"""
Created on 2020/9/19

@author: Mark Hsu
"""
import socket
from _thread import *
from time import sleep


class Server:
    host = '127.0.0.1'
    port = 8001
    conns = {}

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((self.host, self.port))
            self.s.listen(10)
            print("Server is listening now")
            start_new_thread(self.display_info, ())
            self.connection_accept()
        except socket.error as e:
            print('Bind error: ' + str(e))

    def connection_accept(self):
        while True:
            conn, addr = self.s.accept()
            print("Connected by address: ", addr[0], ":", addr[1])
            username = bytes.decode(conn.recv(128))
            self.conns.update({conn: username})

            for c in self.conns.keys():
                if conn == c:
                    welcome_msg = "Hello, " + username + "\nOnline: " + str(self.conns.__len__())
                    conn.sendall(str.encode(welcome_msg))
                else:
                    c.sendall(str.encode(username + " is joined\tOnline: " + str(self.conns.__len__())))

            start_new_thread(self.connection_thread, (conn,))

    def connection_thread(self, conn):
        while True:
            try:
                data = conn.recv(4096)
                if data:
                    self.broadcast(conn, bytes.decode(data))
                else:
                    self.conns.pop(conn)
                    conn.close()
                    break
            except socket.error:
                # connection closed by client side
                self.conns.pop(conn)
                conn.close()
                break

    def broadcast(self, conn, msg):
        message = self.conns[conn] + ": " + msg
        print(message)
        try:
            for conn in self.conns.keys():
                conn.sendall(str.encode(message))
        except socket.error as e:
            print(e)

    def display_info(self):
        while True:
            info = 'Online: ' + str(self.conns.__len__())
            if len(self.conns) > 0:
                info += "\tUser: "
                for name in self.conns.values():
                    info += name + ", "
                info = info[:-2]
            print(info)
            sleep(5)

    def __del__(self):
        if self.conns:
            for c in self.conns:
                c.close()
        if self.s is not None:
            self.s.close()


if __name__ == '__main__':
    server = Server()
