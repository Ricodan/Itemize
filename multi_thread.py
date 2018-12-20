#!/usr/bin/python
#import multiconn-server

import threading
import socket
import types
import service_connection
import json

welcome = "Welcome to Itemize!\nFunctions:\ncreate_new_list()\nedit_list()\nshow_lists()\nPress 'm' at any time to return to this menu"

HOST = '127.0.0.1'
TCP_PORT = 2005

class active_server_socket( threading.Thread):
    #another queue thatwill link to the user intreface
    def __init__(self, sock, port, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.port = port
        self.sock = sock

    def run(self):
        print('created active socket')
        # this one is just writing
        msg = 'From: Active Server Socket: sending msg from active socket'
        self.sock.send(msg.encode())
        #recv_data = self.sock.recv(1024).decode()
        #print(recv_data)
        while True:
            dict = self.queue.get()
            print('ACTIVE SERVER IS SENDING: ', dict)
            data = json.dumps(dict).encode()
            self.sock.send(data)

class passive_client_socket(threading.Thread):
    def __init__(self, port, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.port = port
        tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpClientA.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connected = False
        while not connected:
            try:
                tcpClientA.connect((HOST, self.port))
                connected = True
            except Exception as e:
                pass  # Do nothing, just try again
        #self.function = function
        self.sock = tcpClientA

    def run(self):
                print('PASSIVE CLIENT SOCKET: created passive client socket')
                recv_data = self.sock.recv(1024)
                #recv_data = json.loads(recv_data)
                print("CLIENT IS RECEIVING UPDATE ON A LIST")
                print(recv_data)

class passive_server_socket(threading.Thread):
    def __init__(self, sock, client_port, server_port, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.port = client_port
        self.sock = sock
        #self.function = function

    def run(self):

            print('PASSIVE SERVER SOCKET: created passive socket')
            recv_data = self.sock.recv(1024).decode()
            print(recv_data)

            print('created passive socket')
            data = types.SimpleNamespace(addr=self.port, inb=b"", outb=welcome.encode(), show=False, sent_msg=0,
                                         set_name_fst=False, delete=False, set_name=False, edit=False, list=None,
                                         add=False, push_to_s=False)
            while True:
                service_connection.service_connection(self.sock, data, self.queue)


# class server_worker() that will start off an active and a passive socket/threads at the server worker node

class server_worker(threading.Thread):
    def __init__(self, sock, port, s_to_sw, sw_to_s, function):
        threading.Thread.__init__(self)
        self.s_to_sw = s_to_sw
        self.sw_to_s = sw_to_s
        self.port = port
        self.function = function
        self.sock = sock


    def run(self):
            print('SERVER WORKER: now we run the function in server worker thread')
            # create a socket that listens
            tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            print("MULTITHREAD", self.port+1)

            tcpServer.bind((HOST, self.port+1))
            tcpServer.listen()
            print('SERVER WORKER: server worker listening')
            sock2, addr = tcpServer.accept()
            # start active and passive sockets at server worker node
            self.function(sock2, self.sock, self.port, self.s_to_sw, self.sw_to_s)
            # server worker node should try to read out messeges from the queue it shares with main server node
            #while True:
             #   msg = self.sw_to_s.get()
              #  print(msg)
                #msg = 'now server worker talk to server node'

                #self.server_queue.put(msg)

