#!/usr/bin/python
#import multiconn-server

import threading
import socket

HOST = '127.0.0.1'
TCP_PORT = 2005

class node( threading.Thread):
    #another queue thatwill link to the user intreface
    def __init__(self, sock, port, queue, task):
        threading.Thread.__init__(self)
        self.queue = queue
        self.port = port
        self.sock= sock
        self.task = task
        
    def run(self):
        self.task(self.sock,self.queue)

class server_worker(threading.Thread):
    def __init__(self, active_node, passive_node):
        threading.Thread.__init__(self)
        self.active_node = active_node
        self.passive_node = passive_node


    def run(self):
        self.passive_node.start()
#self.server_queue.put(msg)
