#!/usr/bin/python
#import multiconn-server

import threading
import socket


class activeSocket( threading.Thread):
    #another queue thatwill link to the user intreface
    def __init__(self,port, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.port = port
        #self.function = function
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, TCP_PORT))

    def run(self):
        print('created active socket')
        # this one is just writing
        msg = 'sending msg from active socket'
        self.send(msg.encode())


class passiveSocket(threading.Thread):
    def __init__(self, sock, port, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.port = port
        self.sock = sock
        #self.function = function

    def run(self):
            print('created passive socket')
            recv_data = self.sock.recv(1024).decode()
            print(recv_data)

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
            # start active and passive sockets at server worker node
            self.function(self.sock, self.port, self.active_thread_queue, self.passive_thread_queue)
            # server worker node should try to read out messeges from the queue it shares with main server node
            while True:
                msg = self.server_queue.get()
                print(msg)
                #msg = 'now server worker talk to server node'

                #self.server_queue.put(msg)

