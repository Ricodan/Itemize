#!/usr/bin/env python3
import socket
import queue
import server_worker
import multi_thread
import threading
import json

class server_worker(threading.Thread):
    def __init__(self, port, queue, function):
        threading.Thread.__init__(self)
        self.queue = queue
        self.port = port
        self.function = function


    def run(self):
            # depending on the output you put something on the queeu or you don't
            self.function(self.port)


HOST = '127.0.0.1'
TCP_PORT = 2004
BUFFER_SIZE = 1024

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((HOST, TCP_PORT))
threads = []
s_to_sw = queue.Queue(10)
sw_to_s = queue.Queue(10)


# def hello_active(queue):
#     print('Created active server socket')
#     # check if active server socket can write to passive client socket
#     msg = 'now active server socket is talking to passive client socket'
#     data =


def hello_passive(queue):
    print('Created passive server socket')
    # check if passive server socket can read out msgs from active client socket
    msg = queue.get()
    print(msg)

                            #s_to_sw #sw_to_s
def create_active_passive(conn, sock, port, s_to_sw, sw_to_s):
    print("Now we are trying to create the two sockets at server worker node")
    active_thread = multi_thread.active_server_socket(conn, TCP_PORT+3, s_to_sw)
    passive_thread = multi_thread.passive_server_socket(sock, port, TCP_PORT+2, sw_to_s)
    active_thread.start()
    passive_thread.start()
    threads.append(active_thread)
    threads.append(passive_thread)

while True:
    print("ITEMIZE SERVER: Now we listen")
    tcpServer.listen(4)

    (conn, (ip, port)) = tcpServer.accept()
    print("ITEMIZE SERVER port:", port)
    # we create a new server worker thread with an import function
    newThread = multi_thread.server_worker(conn, port, s_to_sw, sw_to_s, create_active_passive)
    print('ITEMIZE SERVER: created new thread in server')
    newThread.start()
    threads.append(newThread)
    s_to_sw.put('ITEMIZE SERVER now i talk to server worker')
    # get msg from server worker
    print('A')
    msg = sw_to_s.get()
    print('PRINTING WHAT WE GET FROM SERVER WORKER')
    print(msg)
    s_to_sw.put(msg)

for t in threads:
        t.join()
