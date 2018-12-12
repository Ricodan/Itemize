#!/usr/bin/python
#import multiconn-server

import socket
from threading import Thread
from socketserver import ThreadingMixIn

class ClientThread(Thread):

    def __init__(self, host, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print('[+] New server socket started for ', ip, ":", str(port))

    def run(self):
        while True:
            data = conn.recv(1024).decode()
            print('Server received data: ', data)
            MESSAGE = input("Multithreaded Python server : Enter Response from Server/Enter exit:")
            if MESSAGE == 'exit':
                break
            conn.send(MESSAGE.encode())  # echo

# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '127.0.0.1'
TCP_PORT = 2004
BUFFER_SIZE = 1024  # Usually 1024, but we need quick response

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    print('now we listen')
    tcpServer.listen(4)
    print("Multithreaded Python server : Waiting for connections from TCP clients...")
    (conn, (ip, port)) = tcpServer.accept()
    newthread = ClientThread(ip, port)
    newthread.start()
    print('starting new thread')
    threads.append(newthread)

for t in threads:
    t.join()