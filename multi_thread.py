#!/usr/bin/python
#import multiconn-server

import threading


class activeSocket( threading.Thread):
    #another queue thatwill link to the user intreface
    def __init__(self,port, queue, function):
        threading.Thread.__init__(self)
        self.queue = queue
        self.port = port
        self.function = function

    def run(self):
        while True:
            self.function()



class passiveSocket(threading.Thread):
    def __init__(self, port, queue, function):
        threading.Thread.__init__(self)
        self.queue = queue
        self.port = port
        self.function = function

    def run(self):
        while True:
            #depending on the output you put something on the queeu or you don't
            self.function()



class serverWorker(threading.Thread):
    def __init__(self, port, queue, function):
        threading.Thread.__init__(self)
        self.queue = queue
        self.port = port
        self.function = function


    def run(self):
        while True:
            # depending on the output you put something on the queeu or you don't
            self.function()




