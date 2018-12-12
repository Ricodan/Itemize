#!/usr/bin/python
#import multiconn-server

import threading
import socket
import types
import service_connection

welcome = "Welcome to Itemize!\nFunctions:\ncreate_new_list()\nedit_list()\nshow_lists()\nPress 'm' at any time to return to this menu"

HOST = '127.0.0.1'
TCP_PORT = 2005

class active_server_socket( threading.Thread):
    #another queue thatwill link to the user intreface
    def __init__(self, sock, port, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.port = port
        self.sock= sock

    def run(self):
        print('created active socket')
        # this one is just writing
        msg = 'sending msg from active socket'
        self.sock.send(msg.encode())
        recv_data = self.sock.recv(1024).decode()
        print(recv_data)

class passive_client_socket(threading.Thread):
    def __init__(self, port, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.port = port
        tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        while not connected:
            try:
                tcpClientA.connect((HOST, TCP_PORT))
                connected = True
            except Exception as e:
                pass  # Do nothing, just try again
        #self.function = function
        self.sock = tcpClientA

    def run(self):
            while True:
                recv_data = self.sock.recv(1024).decode()
                print(recv_data)

class passive_server_socket(threading.Thread):
    def __init__(self, sock, client_port, server_port, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.port = client_port
        self.sock = sock
        #self.function = function

    def run(self):
            print('created passive socket')
            data = types.SimpleNamespace(addr=self.port, inb=b"", outb=welcome.encode(), show=False, sent_msg=0,
                                         set_name_fst=False, delete=False, set_name=False, edit=False, list=None,
                                         add=False)
            while True:
                service_connection.service_connection(self.sock, data)

# class server_worker() that will start off an active and a passive socket/threads at the server worker node

class server_worker(threading.Thread):
    def __init__(self, sock, port, queue1, queue2, queue3, function):
        threading.Thread.__init__(self)
        self.server_queue = queue1
        self.active_thread_queue = queue2
        self.passive_thread_queue = queue3
        self.port = port
        self.function = function
        self.sock = sock


    def run(self):
            print('now we run the function in server worker thread')
            # create a socket that listens
            tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tcpServer.bind((HOST, TCP_PORT))
            tcpServer.listen()
            print('server worker listening')
            conn, addr = tcpServer.accept()
            # start active and passive sockets at server worker node
            self.function(conn, self.sock, self.port, self.active_thread_queue, self.passive_thread_queue)
            # server worker node should try to read out messeges from the queue it shares with main server node
            while True:
                msg = self.server_queue.get()
                print(msg)
                #msg = 'now server worker talk to server node'

                #self.server_queue.put(msg)

