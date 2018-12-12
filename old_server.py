#!/usr/bin/python
#import multiconn-server
import Queue
import socket
from threading import Thread
from socketserver import ThreadingMixIn

class ServerWorker(Thread):

    def __init__(self, host, port, queue):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.queue = queue
        print('[+] New server socket started for ', ip, ":", str(port))

    def run(self):
        while True:
            conn.listen(4)
            (connection, (ip, port)) = conn.accept()
            newthread = ClientListenerThread(ip, port, queue)
            newthread.start()
            print('starting new listener thread')
            threads.append(newthread)
            data = conn.recv(1024).decode()
            print('Server received data: ', data)
            if data == ' check':
                # now we want to put a message in queue of thread connected to client listening socket
                print('put msg in queue')
                self.queue.put('now it is working!')
                print('now we have put string in queue of other thread')
            MESSAGE = input("Multithreaded Python server : Enter Response from Server/Enter exit:")
            if MESSAGE == 'exit':
                break
            conn.send(MESSAGE.encode())  # echo

class ClientListenerThread(Thread):

    def __init__(self, host, port, queue):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.queue = queue
        print('[+] New listener socket started for ', ip, ":", str(port))

    def run(self):
        while True:
            data = self.queue.get()
            # data = connection.recv(1024).decode()
            print('Listener Server got data out of the queue: ', data)
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
queue = Queue.Queue(10)


while True:
    print('now we listen')
    tcpServer.listen(4)
    print("Multithreaded Python server : Waiting for connections from TCP clients...")
    (conn, (ip, port)) = tcpServer.accept()
    newthread = ServerWorker(ip, port, queue)
    newthread.start()
    print('starting new thread')
    threads.append(newthread)

for t in threads:
    t.join()