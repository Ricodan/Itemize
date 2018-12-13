#!/usr/bin/env python3

import socket
import multi_thread
import queue

import sys

ClientId = dict(id1=2004, id2=2010, id3=2016)

import types
import client_service_conn


HOST = '127.0.0.1'
#PORT = 2004
BUFFER_SIZE = 1024
threads = []
active_queue = queue.Queue(10)
passive_queue = queue.Queue(10)

def print_confirm_passive(queue):
    print('ITEMIZE CLIENT: Passive thread working')
    # check if passive client socket can read out msgs from active server socket
    data = new_passive_thread.recv(1024).decode()
    print(data)


#host, port = sys.argv[1], int(sys.argv[2])
PORT = ClientId[sys.argv[1]]
tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientA.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpClientA.connect((HOST, PORT))

# should we really create a new thread for the active client socket or should it rather run in the main thread??
#new_active_thread = multi_thread.activeSocket(tcpClientA.getsockname()[1], active_queue, print_confirm)
new_passive_thread = multi_thread.passive_client_socket(tcpClientA.getsockname()[1]+1, passive_queue)
#new_active_thread.start()
new_passive_thread.start()
print('ITEMIZE CLIENT started passive thread')
#threads.append(new_active_thread)
threads.append(new_passive_thread)

#from the previous code
msg = 'FROM ITEMIZE CLIENT: check if active client socket can communicate with passive server socket'
tcpClientA.send(msg.encode())


data = types.SimpleNamespace(
            recv_total=0,
            sent_msgs=0,
            outb=b"",
            add=False,
            delete=False,
            list=None,
            cont=False,
            show=False,
            show_all=False
        )
while True:
    client_service_conn.service_connection(tcpClientA, data)


for t in threads:
        t.join()
