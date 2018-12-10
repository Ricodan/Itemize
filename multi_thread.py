#!/usr/bin/python
#import multiconn-server

import threading
import time
import socket
import selectors


exitFlag = 0

class eventThread (threading.Thread):
   def __init__(self, threadID, name, sel, host, port):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.sel = sel

   def run(self):
        listening_socket(host, port,  sel)
        print("Starting " + self.name)
        print_time(self.name, 5, self.counter)
        print("Exiting " + self.name)



def print_time(threadName, counter, delay):
   while counter:
      if exitFlag:
         threadName.exit()
      time.sleep(delay)
      print ("%s: %s" % (threadName, time.ctime(time.time())))
      counter -= 1

# Create new threads
thread1 = eventThread(1, "Thread-1", 1)
thread2 = eventThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()

print("Exiting Main Thread" )


def listening_socket(host, port, sel):
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind((host, port))
    lsock.listen()
    print("listening on", (host, port))
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)
    # we have registrered the lsock as read
    # this is a socket that only reads
