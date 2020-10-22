# coding: UTF-8
"""
Created on 2020/9/20

@author: Mark Hsu
"""
import socket
from _thread import *
from time import sleep
from game_1a2b import Game


class Server:
    host = '127.0.0.1'
    port = 8001
    conns = {}  # conn : username
    player_list = []  # connections
    turn = 0
    playing = ''
    game = None

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

    def game_start(self, conn):
        self.player_list.clear()
        self.player_list.append(conn)
        self.game = Game()
        self.broadcast(msg='User ' + self.conns[conn] + ' starts a game')
        self.broadcast(msg='Enter {join 1a2b} to join the game')
        print('Answer is', self.game.ans)

    def game_guess(self, conn, guess):
        result = self.game.guess(guess[1:len(guess) - 1])
        print(guess[1:len(guess) - 1])
        self.broadcast(msg=self.conns[conn] + ' guessed [' + guess[1:len(guess) - 1] + '] and the result is: ')
        self.broadcast(msg=result + '\r\n')
        if result == 'BINGO':
            self.broadcast(msg='Congrats! The winner is: ' + self.conns[conn])
            self.turn = 0
            self.player_list.clear()
            self.game = None
            self.playing = ''
        elif len(result) != 4:
            self.broadcast(msg='Oops. Try again! ' + self.conns[self.player_list[self.turn]])
        else:
            self.turn += 1
            self.turn %= len(self.player_list)
            self.broadcast(msg='Now is ' + self.conns[self.player_list[self.turn]] + "'s turn")

    def connection_thread(self, conn):
        while True:
            try:
                data = conn.recv(4096)
                if data:
                    message = bytes.decode(data)
                    if message == '{play 1a2b}' and self.playing != '1a2b':
                        self.playing = '1a2b'
                        if message[10] == '-':
                            digit = int(message[11])
                        self.game_start(conn, digit)
                        print('Game start')
                    elif message == '{join 1a2b}' and self.playing == '1a2b':
                        if conn not in self.player_list:
                            self.player_list.append(conn)
                            self.broadcast(msg=self.conns[conn] + ' joined the game')
                        print(len(self.player_list))
                    elif self.playing == '1a2b' and self.player_list[self.turn] == conn and \
                            message[0] == '{' and message[-1] == '}':
                        self.game_guess(conn, message)
                    else:
                        self.broadcast(conn, message)
                else:
                    self.conns.pop(conn)
                    conn.close()
                    break
            except socket.error:
                # connection closed by client side
                self.conns.pop(conn)
                conn.close()
                break

    def broadcast(self, conn=None, msg=''):
        if conn:
            message = self.conns[conn] + ": " + msg
        else:
            message = "Server broadcast: " + msg
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
